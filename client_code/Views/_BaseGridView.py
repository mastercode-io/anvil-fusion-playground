import anvil.server
import anvil.js
from anvil.js.window import ej, jQuery

from .. import app
from ..app.constants import *
from ..orm_client.model import *
from ..orm_client import enumerations as enums
from .. import Forms

import string
import uuid
import json
import sys
from datetime import datetime

GRID_DEFAULT_FILTER_SETTINGS = {'type': 'Menu'}
GRID_DEFAULT_TOOLBAR_ITEMS = ['Add', 'Edit', 'Delete', 'Search']
GRID_DEFAULT_MODES = ['Sort', 'Filter', 'InfiniteScroll', 'Toolbar', 'Edit', 'ForeignKey']
GRID_MODE_TO_SWITCH = {
    'Sort': 'allowSorting',
    'Filter': 'allowFiltering',
    'Group': 'allowGrouping',
    'Page': 'allowPaging',
    'InfiniteScroll': 'enableInfiniteScrolling',
    'ExcelExport': 'allowExcelExport',
    'PdfExport': 'allowPdfExport',
    'Reorder': 'allowReordering',
    'Resize': 'allowResizing',
    'RowDD': 'allowRowDragAndDrop',
    'Selection': 'allowSelection',
}
GRID_DEFAULT_EDIT_SETTINGS = {
    'allowAdding': True,
    'allowEditing': True,
    'allowDeleting': True,
    'mode': 'Dialog',
    'allowEditOnDblClick': True,
    'showConfirmDialog': True,
    'showDeleteConfirmDialog': True,
    'allowScrolling': True
}
GRID_HEIGHT_OFFSET = 65
GRID_DEFAULT_COLUMN_WIDTH = 150


class BaseGridView:
    def __init__(self,
                 container_id=None,
                 view_name=None,
                 view_config=None,
                 model=None,
                 title=None
                 ):

        self.grid_height = None
        self.grid_el_id = None
        self.container_id = container_id
        self.container_el = None
        self.model = model

        print('BaseGridView')
        if view_name is not None or view_config is not None:
            if view_config is not None:
                self.view_config = view_config
            else:
                view_obj = appGridViews.get_by('name', view_name)
                self.view_config = json.loads(view_obj['config'].replace("'", "\""))
            # print(self.view_config)
            # print(view_name, view_config)
            self.model = self.view_config['model']
            self.grid_class = getattr(sys.modules[__name__], self.model)
            grid_columns = []
            for column in self.view_config['columns']:
                if column['type'] == 'button':
                    grid_column = {
                        'headerText': column['label'],
                        'template': '<div id="cell-button"></div>',
                        'width': column['width'] if 'width' in column else GRID_DEFAULT_COLUMN_WIDTH,
                    }
                else:
                    grid_column = {
                        'field': column['field'],
                        'headerText': column['label'],
                        'textAlign': 'Left',
                        'customAttributes': {'class': 'align-top'},
                        'width': column['width'] if 'width' in column else GRID_DEFAULT_COLUMN_WIDTH,
                        'valueAccessor': self.format_value,
                    }
                    if column['type'] == 'relation':
                        grid_column['field'] += '_uid'
                        grid_column['type'] = 'string'
                        grid_column['relation'] = {
                            'field': column['field'],
                            'model': column['ref_model'],
                            'value': column['ref_field'],
                            'key': 'uid',
                        }
                    else:
                        grid_column['type'] = FIELD_TO_GRID[column['type']]
                        grid_column['format'] = column['format'] if 'format' in column else self.format_column(
                            column['type'])
                        # grid_column['valueAccessor'] = self.format_value
                        grid_column['displayAsCheckBox'] = True if column['type'] == BOOLEAN_FIELD else False
                grid_columns.append(grid_column)
            self.grid_view = {'config': self.view_config}
            self.grid_view['config']['columns'] = grid_columns

        else:
            self.grid_view = {'config': {}}
            self.grid_class = getattr(sys.modules[__name__], self.model)

        # configure Grid control
        self.grid_title = title if title is not None else app.lib.camel_to_title(self.model)
        self.grid_config = {}
        self.grid_data = []
        self.db_data = {}

        # configure grid columns
        if 'columns' not in self.grid_view['config']:
            grid_columns = []
            # attribute fields
            for attr, attr_props in self.grid_class._attributes.items():
                grid_columns.append({
                    'field': attr,
                    'headerText': string.capwords(attr.replace("_", " ")),
                    'textAlign': 'Left',
                    'customAttributes': {'class': 'align-top'},
                    # 'type': FIELD_TO_GRID[attr_props.field_type],
                    # 'format': self.format_column(attr_props.field_type),
                    # 'displayAsCheckBox': True if attr_props.field_type == BOOLEAN_FIELD else False,
                    'type': attr_props.field_type.GridType,
                    'format': self.format_column(attr_props.field_type),
                    'displayAsCheckBox': attr_props.field_type == enums.FieldTypes.BOOLEAN,
                    'valueAccessor': self.format_value,
                    'width': 150,
                })
            # relationship (link) fields
            for ref in self.grid_class._relationships.keys():
                ref_class = self.grid_class._relationships[ref].__dict__['class_name']
                if ref_class is not 'Tenant':
                    ref_attrs = getattr(sys.modules[__name__], ref_class)._attributes
                    if not ref_attrs:
                        ref_attrs = getattr(sys.modules[__name__], ref_class)._relationships
                    ref_title = [*ref_attrs.keys()][0]
                    grid_columns.append({
                        'field': f"{ref}_uid",
                        'headerText': string.capwords(ref.replace("_", " ")),
                        'textAlign': 'Left',
                        'customAttributes': {'class': 'align-top'},
                        'type': 'string',
                        'width': 150,
                        'relation': {
                            'field': ref,
                            'model': ref_class,
                            'key': 'uid',
                            'value': ref_title
                        }
                    })
            self.grid_view['config'] = {'columns': grid_columns}

        self.grid_config['columns'] = self.grid_view['config']['columns']

        # get reference fields data
        self.db_ref_data = {}
        for field in self.grid_config['columns']:
            if 'relation' in field:
                field['foreignKeyField'] = field['relation']['key']
                field['foreignKeyValue'] = field['relation']['value']
                field_class = getattr(sys.modules[__name__], field['relation']['model'])
                ref_data = {obj['uid']: obj for obj in field_class.search()}
                self.db_ref_data[field['relation']['model']] = ref_data
                field_data = [obj.to_grid() for obj in ref_data.values()]
                field['dataSource'] = field_data
                # print(field['headerText'], field_data)
        self.grid_config['columns'].append({'field': 'uid', 'isPrimaryKey': True, 'visible': False})
        # print('Grid columns', self.grid_config['columns'])

        # attach grid data source
        self.grid_config['dataSource'] = self.grid_data

        # configure grid settings
        if 'modes' not in self.grid_view['config']:
            self.grid_view['config']['modes'] = GRID_DEFAULT_MODES
        for grid_mode in self.grid_view['config']['modes']:
            ej.grids.Grid.Inject(ej.grids[grid_mode])
            if grid_mode in GRID_MODE_TO_SWITCH and GRID_MODE_TO_SWITCH[grid_mode]:
                self.grid_config[GRID_MODE_TO_SWITCH[grid_mode]] = True
        if 'Page' in self.grid_view['config']['modes']:
            self.grid_config['pageSettings'] = {'pageSize': self.grid_view['config']['pageSize']}
        if 'Edit' in self.grid_view['config']['modes']:
            self.grid_config['editSettings'] = self.grid_view['config']['editSettings'] if 'editSettings' in \
                self.grid_view['config'] else GRID_DEFAULT_EDIT_SETTINGS
        if 'Toolbar' in self.grid_view['config']['modes']:
            self.grid_config['toolbar'] = self.grid_view['config']['toolbar'] if 'toolbar' in self.grid_view[
                'config'] else GRID_DEFAULT_TOOLBAR_ITEMS
        if 'Filter' in self.grid_view['config']['modes']:
            self.grid_config['filterSettings'] = GRID_DEFAULT_FILTER_SETTINGS
        self.grid_config['showColumnMenu'] = True
        self.grid_config['allowTextWrap'] = True
        # self.grid_config['enableStickyHeader'] = True
        self.grid_config['width'] = '100%'
        self.grid_config['height'] = '100%'

        # attach grid event handlers
        self.grid_config['actionComplete'] = self.action_event_handler
        self.grid_config['queryCellInfo'] = self.query_cell_info
        self.grid_config['recordClick'] = self.record_click

        # create Grid control
        self.grid = ej.grids.Grid(self.grid_config)
        # print('Grid config\n', json.dumps(self.grid_config['columns']))

    @staticmethod
    def format_column(field_type):
        format_string = ''
        if field_type == enums.FieldTypes.DATE:
            format_string = 'dd/MM/yyyy'
        elif field_type == enums.FieldTypes.DATETIME:
            format_string = 'dd/MM/yyyy hh:mm'
        elif field_type == enums.FieldTypes.TIME:
            format_string = 'hh:mm'
        elif field_type == enums.FieldTypes.CURRENCY:
            format_string = 'C2'
        elif field_type == enums.FieldTypes.DECIMAL:
            format_string = 'N2'
        return format_string

    @staticmethod
    def format_value(field, data, column):
        # print('valueAccessor', field, data)
        # print('value', data[field])
        return data[field] if data[field] is not None else ''

    # get Grid data and refresh the view
    def form_show(self, **event_args):
        try:
            self.db_data = {obj['uid']: obj for obj in self.grid_class.search()}
            # print(self.grid_class, self.db_data)
            self.grid_data = [obj.to_grid() for obj in self.db_data.values()]
            # print('Grid data\n', json.dumps(self.grid_data), '\n')
            self.grid['dataSource'] = self.grid_data
            # print('Grid data source\n', self.grid.dataSource, '\n')
            self.grid_el_id = uuid.uuid4()
            self.container_el = jQuery(f"#{self.container_id}")[0]
            self.grid_height = self.container_el.offsetHeight - GRID_HEIGHT_OFFSET
            self.container_el.innerHTML = f'\
               <div id="pm-grid-container" style="height:{self.grid_height}px;">\
                 <div class="pm-gridview-title">{self.grid_title}</div>\
                 <div id="{self.grid_el_id}"></div>\
               </div>'
            self.grid.appendTo(jQuery(f"#{self.grid_el_id}")[0])
        except Exception as e:
            print('Error in Grid form_show', e)

    def destroy(self):
        self.grid.destroy()
        if self.container_el is not None:
            self.container_el.innerHTML = ''

    def query_cell_info(self, args):
        el = args.cell.querySelector('#cell-button')
        button = ej.buttons.Button({'content': 'Click'})
        button.appendTo(el)

    def record_click(self, args):
        if args.target.id == 'cell-button':
            print(args.rowIndex, args.rowData)

    def action_event_handler(self, event_args):
        print('actionComplete')
        # print(event_args['requestType'])
        # open form to add or edit a record
        if event_args['requestType'] in ('beginEdit', 'add'):
            event_args.dialog.close()
            form_action = 'add' if event_args['requestType'] == 'add' else 'edit'
            if event_args['requestType'] == 'beginEdit':
                row_data = self.grid_data[event_args['rowIndex']]
                row_data['obj'] = self.db_data[row_data['uid']]
            else:
                row_data = None
            print('Dialog form: ', f"Forms.{self.model}Form")
            try:
                edit_form_class = getattr(sys.modules[f"{APP_NAME}.Forms"], f"{self.model}Form")
                print("EDIT FORM CLASS")
                print(edit_form_class)
                edit_dialog = edit_form_class(data=row_data, action=form_action, update_source=self.update_grid,
                                              target=self.container_id)
            except Exception as e:
                print('Exception', e)
                edit_dialog = Forms.BaseForm(model=self.model, data=row_data, action=form_action,
                                             update_source=self.update_grid, target=self.container_id)
            event_args.dialog = edit_dialog.form
            edit_dialog.form_show()

        # delete a record(s)
        if event_args['requestType'] == 'delete':
            for data_row in event_args['data']:
                data_obj = self.db_data[data_row['uid']]
                data_obj.delete()
                self.db_data.pop(data_row['uid'], None)
            self.grid.refresh()

    def update_grid(self, data_row):
        if data_row['uid'] in self.db_data.keys():
            for i, grid_row in enumerate(self.grid_data):
                if grid_row['uid'] == data_row['uid']:
                    self.grid_data[i] = data_row.to_grid()
        else:
            self.grid_data.insert(0, data_row.to_grid())
        self.db_data[data_row['uid']] = data_row
        self.grid['dataSource'] = self.grid_data
        self.grid.refresh()
