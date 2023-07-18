# Static and dynamic enumerations
from .lib import *
from ..app.lib import *
from ..app.constants import *


MODEL_MODULE_NAME = 'practiceMANAGER_SF.orm_client.model'


# Model types
MODEL_TYPES = {
    'system': 'system',
    'data': 'data',
}
ModelTypes = Enumeration(MODEL_TYPES)


# Field types
FIELD_TYPES = {
    'uid': {
        'ColumnType': 'string',
        'InputType': 'TextInput',
        'GridType': 'string',
        'GridFormat': '',
    },
    'single_line': {
        'ColumnType': 'string',
        'InputType': 'TextInput',
        'GridType': 'string',
        'GridFormat': '',
    },
    'multi_line': {
        'ColumnType': 'string',
        'InputType': 'MultiLineInput',
        'GridType': 'string',
        'GridFormat': '',
    },
    'number': {
        'ColumnType': 'number',
        'InputType': 'NumberInput',
        'GridType': 'number',
        'GridFormat': '',
    },
    'decimal': {
        'ColumnType': 'number',
        'InputType': 'NumberInput',
        'GridType': 'number',
        'GridFormat': 'N2',
    },
    'currency': {
        'ColumnType': 'number',
        'InputType': 'NumberInput',
        'GridType': 'number',
        'GridFormat': 'C2',
    },
    'date': {
        'ColumnType': 'date',
        'InputType': 'DateInput',
        'GridType': 'date',
        'GridFormat': 'dd/MM/yyyy',
    },
    'datetime': {
        'ColumnType': 'datetime',
        'InputType': 'DateTimeInput',
        'GridType': 'datetime',
        'GridFormat': 'dd/MM/yyyy hh:mm',
    },
    'time': {
        'ColumnType': 'datetime',
        'InputType': 'TimeInput',
        'GridType': 'datetime',
        'GridFormat': 'hh:mm',
    },
    'boolean': {
        'ColumnType': 'boolean',
        'InputType': 'CheckboxInput',
        'GridType': 'boolean',
        'GridFormat': '',
    },
    'email': {
        'ColumnType': 'string',
        'InputType': 'TextInput',
        'GridType': 'string',
        'GridFormat': '',
    },
    'address': {
        'ColumnType': 'simpleObject',
        'InputType': 'AddressInput',
        'GridType': 'string',
        'GridFormat': '',
    },
    'hyperlink': {
        'ColumnType': 'simpleObject',
        'InputType': 'HyperlinkInput',
        'GridType': 'string',
        'GridFormat': '',
    },
    'signature': {
        'ColumnType': 'string',
        'InputType': 'SignatureInput',
        'GridType': 'string',
        'GridFormat': '',
    },
    'object': {
        'ColumnType': 'simpleObject',
        'InputType': 'MultiLineInput',
        'GridType': 'string',
        'GridFormat': '',
    },
    'media': {
        'ColumnType': 'media',
        'InputType': 'FileUploadInput',
        'GridType': 'media',
        'GridFormat': '',
    },
    'file_upload': {
        'ColumnType': 'simpleObject',
        'InputType': 'FileUploadInput',
        'GridType': 'string',
        'GridFormat': '',
    },
    'enum_single': {
        'ColumnType': 'string',
        'InputType': 'DropdownInput',
        'GridType': 'string',
        'GridFormat': '',
    },
    'enum_multi': {
        'ColumnType': 'simpleObject',
        'InputType': 'DropdownInput',
        'GridType': 'string',
        'GridFormat': '',
    },
    'relationship': {
        'ColumnType': 'link',
        'InputType': 'DropdownInput',
        'GridType': 'string',
        'GridFormat': '',
    },
}
FieldTypes = Enumeration(FIELD_TYPES)

# App model list for enumerations
ENUM_MODEL_LIST = {
    'Activity': {'model': 'Activity', 'name_field': 'name'},
    'BankAccount': {'model': 'BankAccount', 'name_field': 'account_type.name'},
    'BankAccountType': {'model': 'BankAccountType', 'name_field': 'name'},
    'Branch': {'model': 'Branch', 'name_field': 'name'},
    'CaseStage': {'model': 'CaseStage', 'name_field': 'name'},
    'CaseStatus': {'model': 'CaseStatus', 'name_field': 'name'},
    'CauseOfAction': {'model': 'CauseOfAction', 'name_field': 'cause_of_action'},
    'ContactGroup': {'model': 'ContactGroup', 'name_field': 'name'},
    'ContactRole': {'model': 'ContactRole', 'name_field': 'name'},
    'EntityType': {'model': 'EntityType', 'name_field': 'name'},
    'FeeType': {'model': 'FeeType', 'name_field': 'name'},
    'LeadSource': {'model': 'LeadSource', 'name_field': 'name'},
    'PracticeArea': {'model': 'PracticeArea', 'name_field': 'name'},
    'StaffGroup': {'model': 'StaffGroup', 'name_field': 'name'},
    'StaffPayType': {'model': 'StaffPayType', 'name_field': 'name'},
    'TypeOfAction': {'model': 'TypeOfAction', 'name_field': 'name'},
}
Models = {}


def init_model_enumerations():

    for model, props in ENUM_MODEL_LIST.items():
        view_config = {
            'model': props['model'],
            'columns': [{'name': props['name_field']}],
        }
        cls = getattr(sys.modules[MODEL_MODULE_NAME], view_config['model'])
        search_queries = props['search_queries'] if 'search_queries' in props else []
        filters = props['filters'] if 'filters' in props else {}
        ENUM_MODEL_LIST[model]['options'] = cls.get_grid_view(view_config, search_queries, filters)
        if props['name_field'] != 'name':
            name_field = props['name_field'].split('.', 1)[0]
            for option in ENUM_MODEL_LIST[model]['options']:
                option['name'] = option[name_field]

    return DotDict(ENUM_MODEL_LIST)
