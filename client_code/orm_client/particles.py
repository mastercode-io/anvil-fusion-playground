# MIT License
#
# Copyright (c) 2020 The Anvil ORM project team members listed at
# https://github.com/anvilistas/anvil-orm/graphs/contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# This software is published at # https://github.com/anvilistas/anvil-orm
import sys
from anvil import *
import anvil.server
import anvil.users
import anvil.js
from ..app.constants import *
from .lib import *
from . import enumerations as enums

import datetime

__version__ = "1.3.01"

FIELD_TO_COLUMN = {
    UID_FIELD: 'string',
    SINGLE_LINE_FIELD: 'string',
    MULTI_LINE_FIELD: 'string',
    NUMBER_FIELD: 'number',
    DECIMAL_FIELD: 'number',
    CURRENCY_FIELD: 'number',
    DATE_FIELD: 'date',
    DATETIME_FIELD: 'datetime',
    TIME_FIELD: 'datetime',
    BOOLEAN_FIELD: 'boolean',
    EMAIL_FIELD: 'string',
    ADDRESS_FIELD: 'simpleObject',
    HYPERLINK_FIELD: 'simpleObject',
    SIGNATURE_FIELD: 'string',
    OBJECT_FIELD: 'simpleObject',
    UPLOAD_FIELD: 'simpleObject',
    MEDIA_FIELD: 'media',
    ENUM_SINGLE_FIELD: 'string',
    ENUM_MULTI_FIELD: 'simpleObject',
}


# TABLE_COLUMN = Enumeration(FIELD_TO_COLUMN)


class Attribute:
    """A class to represent an attribute of a model object class.
    Attributes are persisted as columns on the class's relevant data table
    """

    def __init__(self, field_type=enums.FieldTypes.SINGLE_LINE,
                 label=None,
                 schema=None,
                 required=False,
                 default=None,
                 is_uid=False
                 ):
        self.field_type = field_type
        self.label = label
        self.schema = schema
        self.required = required
        self.default = default
        self.is_uid = is_uid

    def props(self):
        return {'field_type': self.field_type, 'required': self.required,
                'default': self.default, 'is_uid': self.is_uid, 'schema': self.schema}


class AttributeValue:
    """A class to represent the instance value of an attribute."""

    def __init__(self, name, value, title=None):
        self.name = name
        self.value = value
        self.title = title or name.title()

    def to_dict(self):
        return {"name": self.name, "value": self.value, "title": self.title}


class Relationship:
    """A class to represent a relationship between two model object classes.
    These are persisted as data tables linked columns.
    """

    def __init__(
            self, class_name, required=False, with_many=False, cross_reference=None
    ):
        self.field_type = enums.FieldTypes.RELATIONSHIP
        self.class_name = class_name
        self.required = required
        self.default = None
        if with_many:
            self.default = []
        self.with_many = with_many
        self.cross_reference = cross_reference

    @property
    def cls(self):
        return getattr(sys.modules[self.__module__], self.class_name)


class Computed:
    """A class to represent the computed property of a model object."""

    def __init__(self, depends_on, compute_func, field_type=enums.FieldTypes.SINGLE_LINE):
        self.required = False
        self.field_type = field_type
        self._depends_on = depends_on
        self._compute_func = compute_func

    @property
    def depends_on(self):
        return self._depends_on

    def compute(self, cls, args, grid_view=False):
        # print('compute', cls, args)
        value = getattr(cls, self._compute_func)(args)
        if grid_view and isinstance(value, datetime.datetime) or isinstance(value, datetime.date):
            value = anvil.js.window.Date(int(value.strftime('%s')) * 1000)
        return value


class ModelSearchResultsIterator:
    """A paging iterator over the results of a search cached on the server"""

    def __init__(self, class_name, module_name, rows_id, page_length, max_depth=None):
        self.class_name = class_name
        self.module_name = module_name
        self.rows_id = rows_id
        self.page_length = page_length
        self.next_page = 0
        self.is_last_page = False
        self.max_depth = max_depth
        self.iterator = iter([])

    def __next__(self):
        try:
            return next(self.iterator)
        except StopIteration:
            if self.is_last_page:
                raise
            results, self.is_last_page = anvil.server.call(
                "fetch_objects",
                self.class_name,
                self.module_name,
                self.rows_id,
                self.next_page,
                self.page_length,
                self.max_depth,
            )
            self.iterator = iter(results)
            self.next_page += 1
            return self.__next__()


@anvil.server.serializable_type
class ModelSearchResults:
    """A class to provide lazy loading of search results"""

    def __init__(
            self, class_name, module_name, rows_id, page_length, max_depth, length
    ):
        self.class_name = class_name
        self.module_name = module_name
        self.rows_id = rows_id
        self.page_length = page_length
        self.max_depth = max_depth
        self._length = length

    def __len__(self):
        return self._length

    def __iter__(self):
        return ModelSearchResultsIterator(
            self.class_name,
            self.module_name,
            self.rows_id,
            self.page_length,
            self.max_depth,
        )


def attribute_props(self, name):
    """A factory function to pass Attribute properties"""
    attr = getattr(self, name, None)
    return attr.props()


def attribute_value(self, name, title=None):
    """A factory function to generate AttributeValue instances"""
    value = getattr(self, name, None)
    return AttributeValue(name=name, value=value, title=title)


def _constructor(attributes, relationships, computes):
    """A function to return the __init__ function for the eventual model class"""
    # We're just merging dicts here but skulpt doesn't support the ** operator
    members = attributes.copy()
    members.update(relationships)
    members.update(computes)

    def init(self, **kwargs):
        self.uid = kwargs.pop("uid", None)

        # Check that we've received arguments for all required members
        required_args = [name for name, member in members.items() if member.required]
        for name in required_args:
            if name not in kwargs:
                raise ValueError(f"No argument provided for required {name}")

        # Check that the arguments received match the model and set the instance attributes if so
        for name, value in kwargs.items():
            if name not in members:
                raise ValueError(
                    f"{type(self).__name__}.__init__ received an invalid argument: '{name}'"
                )
            else:
                setattr(self, name, value)

        for name, computed in computes.items():
            args = {dep: getattr(self, dep) for dep in computed.depends_on}
            setattr(self, name, computed.compute(self.__class__, args))

        # Set the default instance attributes for optional members missing from the arguments
        for name, member in members.items():
            if name not in kwargs:
                value = member.default if hasattr(member, 'default') else None
                setattr(self, name, value)

    return init


def _equivalence(self, other):
    """A function to assert equivalence between client and server side copies of model
    instances"""
    return type(self) == type(other) and self.uid == other.uid


def _getitem(self, key):
    """A function to provide dict like indexing"""
    # print("getitem", key)
    return getattr(self, key, None)


def _setitem(self, key, value):
    setattr(self, key, value)


def _update(self, attrs):
    for key, value in attrs.items():
        setattr(self, key, value)


def _from_row(unique_identifier, attributes, relationships, computes):
    """A factory function to generate a model instance from a data tables row."""

    @classmethod
    def instance_from_row(cls, row, cross_references=None, max_depth=None, depth=0):
        if anvil.server.context.type == "client":
            raise TypeError(
                "_from_row is a server side function and cannot be called from client code"
            )

        if row is None:
            return None

        if cross_references is None:
            cross_references = set()

        attrs = dict(row)
        # print("row", row)
        # print("attrs", attrs)
        attrs = {
            key: value
            for key, value in attrs.items()
            if key in attributes or key == "uid"
        }
        if "uid" not in attrs:
            attrs["uid"] = attrs[unique_identifier]

        for name, relationship in relationships.items():
            xref = None
            attrs[name] = None

            if relationship.cross_reference is not None:
                xref = (cls.__name__, attrs["uid"], name)

            if xref is not None and xref in cross_references:
                break

            if xref is not None:
                cross_references.add(xref)

            if max_depth is None or depth < max_depth:
                if not relationship.with_many:
                    attrs[name] = relationship.cls._from_row(
                        row[name], cross_references, max_depth, depth + 1
                    )
                else:
                    attrs[name] = []
                    if row[name]:
                        attrs[name] = [
                            relationship.cls._from_row(
                                member, cross_references, max_depth, depth + 1
                            )
                            for member in row[name]
                        ]

        for name, computed in computes.items():
            args = {dep: attrs[dep] for dep in computed.depends_on}
            attrs[name] = computed.compute(cls, args)
            # attrs.update(args)

        return cls(**attrs)

    return instance_from_row


@classmethod
def _get(cls, uid, max_depth=None):
    """Provide a method to fetch an object from the server"""
    return anvil.server.call("get_object", cls.__name__, cls.__module__, uid, max_depth)


@classmethod
def _get_by(cls, prop, value, max_depth=None):
    """Provide a method to fetch an object from the server"""
    return anvil.server.call("get_object_by", cls.__name__, cls.__module__, prop, value, max_depth)


@classmethod
def _search(
        cls,
        page_length=100,
        max_depth=None,
        server_function=None,
        with_class_name=True,
        **search_args,
):
    """Provides a method to retrieve a set of model instances from the server"""
    _server_function = server_function or "basic_search"
    results = anvil.server.call(
        _server_function,
        cls.__name__,
        cls.__module__,
        page_length,
        max_depth,
        with_class_name,
        **search_args,
    )
    return results


def get_col_value(cls, data, col):
    if '.' not in col:
        if col not in cls._computes:
            # print(col, data)
            value = data[col] if not isinstance(data, list) else [row[col] for row in data]
        else:
            value = cls._computes[col].compute(cls, data, grid_view=True) if not isinstance(data, list) \
                else [cls._computes[col].compute(cls, x, grid_view=True) for x in data]
        if isinstance(value, list):
            value = ', '.join(value)

        parent = col
    else:
        parent, col = col.split('.', 1)
        value = data[parent]
        if value is not None:
            if parent in cls._attributes:
                value = data[parent][col]
            else:
                rel = getattr(sys.modules[cls.__module__], cls._relationships[parent].class_name)
                value, _ = get_col_value(rel, data[parent], col)

    if isinstance(value, (datetime.date, datetime.datetime)):
        value = anvil.js.window.Date(int(value.strftime('%s')) * 1000)
    value = value or ''
    return value, parent


def _get_row_view(self, columns, include_row=True):
    row_view = {'uid': self.uid if self.uid else ''}
    for col in columns:
        if not col.get('no_data', False):
            value, field = get_col_value(self.__class__, self, col['name'])
            row_view[field] = value
    if include_row:
        row_view['row'] = self.get(self.uid) if self.uid else None
    return row_view


@classmethod
def _get_grid_view(cls, view_config, search_queries=None, filters=None, include_rows=False):
    """Provides a method to retrieve a set of model instances from the server"""
    search_queries = search_queries or []
    filters = filters or {}
    column_names = [col['name'] for col in view_config['columns'] if not col.get('no_data', False)]
    if 'uid' not in column_names:
        column_names.insert(0, 'uid')
    rows = anvil.server.call(
        "fetch_view",
        cls.__name__,
        cls.__module__,
        column_names,
        search_queries,
        filters,
    )

    results = []
    for row in rows:
        grid_row = {}
        for col in column_names:
            value, field = get_col_value(cls, row, col)
            grid_row[field] = value
        if include_rows:
            grid_row['row'] = row
        results.append(grid_row)

    return results


def _save(self, audit=True):
    """Provides a method to persist an instance to the database"""
    # return anvil.server.call("save_object", self, audit)
    instance = anvil.server.call("save_object", self, audit)
    if self.uid is None:
        self.uid = instance.uid
    return instance


def _delete(self, audit=True):
    """Provides a method to delete an instance from the database"""
    anvil.server.call("delete_object", self, audit)


def _to_json(self):
    json_dict = {'uid': self['uid']}
    for attr in self._attributes:
        json_dict[attr] = self[attr]
    for prop in self._properties:
        json_dict[prop] = self[prop]
    for ref in self._relationships:
        if self[ref] is not None:
            if isinstance(self[ref], list):
                json_dict[ref] = [ref_obj.to_json() for ref_obj in self[ref]]
                json_dict[f'{ref}_uid'] = [ref_dict['uid'] for ref_dict in json_dict[ref]]
            else:
                json_dict[ref] = self[ref].to_json()
                json_dict[f'{ref}_uid'] = json_dict[ref]['uid']
        else:
            json_dict[ref] = None
            json_dict[f'{ref}_uid'] = None
    return json_dict


def _to_grid(self):
    grid_dict = {'uid': self['uid']}
    for attr, attr_props in self._attributes.items():
        # grid_field = FIELD_TO_GRID[attr_props.field_type]
        grid_field = attr_props.field_type.GridType
        if grid_field == 'date' or grid_field == 'datetime':
            if self[attr] is not None:
                epoch = int(self[attr].strftime('%s')) * 1000
                grid_value = anvil.js.window.Date(epoch)
            else:
                grid_value = None
        else:
            grid_value = self[attr]
        grid_dict[attr] = grid_value
    for prop in self._properties:
        grid_dict[prop] = self[prop]
    for ref in self._relationships:
        if self[ref] is not None:
            if isinstance(self[ref], list):
                grid_dict[ref] = [ref_obj.to_grid() for ref_obj in self[ref]]
                grid_dict[f'{ref}_uid'] = [ref_dict['uid'] for ref_dict in grid_dict[ref]]
            else:
                grid_dict[ref] = self[ref].to_grid()
                grid_dict[f'{ref}_uid'] = grid_dict[ref]['uid']
        else:
            grid_dict[ref] = None
            grid_dict[f'{ref}_uid'] = None
    return grid_dict


def model_type(cls):
    """A decorator to provide a usable model class"""
    class_members = {
        key: value for key, value in cls.__dict__.items() if not key.startswith("__")
    }
    attributes = {
        key: value
        for key, value in class_members.items()
        if isinstance(value, Attribute)
    }
    unique_identifier = "uid"
    unique_identifiers = [key for key, value in attributes.items() if value.is_uid]
    if unique_identifiers:
        if len(unique_identifiers) > 1:
            raise AttributeError("Multiple unique identifiers defined")
        else:
            unique_identifier = unique_identifiers[0]

    relationships = {
        key: value
        for key, value in class_members.items()
        if isinstance(value, Relationship)
    }
    for relationship in relationships.values():
        relationship.__module__ = cls.__module__

    computes = {
        key: value
        for key, value in class_members.items()
        if isinstance(value, Computed)
    }

    methods = {key: value for key, value in class_members.items() if callable(value)}
    class_attributes = {
        key: value
        for key, value in class_members.items()
        if not isinstance(value, (Attribute, Relationship, Computed))
    }

    class_properties = {
        key: value
        for key, value in class_members.items()
        if isinstance(value, property)
    }

    members = {
        "__module__": cls.__module__,
        "__init__": _constructor(attributes, relationships, computes),
        "__eq__": _equivalence,
        "__getitem__": _getitem,
        "__setitem__": _setitem,
        "_attributes": attributes,
        "_relationships": relationships,
        "_computes": computes,
        "_properties": class_properties,
        "_from_row": _from_row(unique_identifier, attributes, relationships, computes),
        "_unique_identifier": unique_identifier,
        "_model_type": class_members['model_type'] if 'model_type' in class_members else DATA_MODEL,
        "update_capability": None,
        "delete_capability": None,
        "search_capability": None,
        "attribute_props": attribute_props,
        "attribute_value": attribute_value,
        "get": _get,
        "get_by": _get_by,
        "search": _search,
        "get_grid_view": _get_grid_view,
        "get_row_view": _get_row_view,
        "update": _update,
        "save": _save,
        "expunge": _delete,
        "delete": _delete,
        "to_json": _to_json,
        "to_grid": _to_grid,
        # "is_data_model": True,
    }
    members.update(methods)
    members.update(class_attributes)

    model = type(cls.__name__, (object,), members)
    return anvil.server.portable_class(model)
