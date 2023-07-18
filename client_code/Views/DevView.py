import anvil.js
from anvil.js.window import ej, jQuery

from .. import app
from ..app.constants import *
from ..orm_client.model import *
from ..Views import *
from .. import Forms


class DevView(BaseGridView):
    def __init__(self, **kwargs):
        print('DevView')
        config = {'model': 'Client'}

        {'field': '', 'label': '', 'type': 'relation', 'ref_model': '', 'ref_field': ''},
        {'field': '', 'label': '', 'type': 'relation', 'ref_model': '', 'ref_field': '', 'width': 150},
        {'field': '', 'label': '', 'type': SINGLE_LINE_FIELD},
        {'field': '', 'label': '', 'type': SINGLE_LINE_FIELD, 'width': 150},

        # client_name = Attribute(field_type=orm.SINGLE_LINE_FIELD)
        # is_individual = Attribute(field_type=orm.BOOLEAN_FIELD)
        # contact = Relationship('Contact')
        # entity = Relationship('Entity')

        columns = [
            {'name': 'client_name', 'label': 'Client Name', 'type': SINGLE_LINE_FIELD},
            {'name': 'is_individual', 'label': 'Individual', 'type': BOOLEAN_FIELD},
            {'name': 'contact', 'label': 'Contact', 'type': 'relation', 'ref_model': 'Contact', 'ref_field': 'name'},
            {'name': 'entity', 'label': 'Entity', 'type': 'relation', 'ref_model': 'Entity', 'ref_field': 'name'},
        ]
        config['columns'] = columns
        self.config = config.copy()

        super().__init__(title='Dev View', view_config=config, **kwargs)

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value
