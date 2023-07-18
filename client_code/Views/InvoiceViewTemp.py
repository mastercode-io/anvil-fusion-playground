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
    config = {'model': 'Invoice'}


    # {'field': '', 'label': '', 'type': 'relation', 'ref_model': '', 'ref_field': ''},
    # {'field': '', 'label': '', 'type': 'relation', 'ref_model': '', 'ref_field': '', 'width': 150},
    # {'field': '', 'label': '', 'type': SINGLE_LINE_FIELD},
    # {'field': '', 'label': '', 'type': SINGLE_LINE_FIELD, 'width': 150},
    
    # invoice_number = Attribute(field_type=orm.NUMBER_FIELD)
    # case = Relationship('Case')
    # bill_to = Relationship('Contact')
    # fee_type = Relationship('FeeType')
    # total = Attribute(field_type=orm.CURRENCY_FIELD)
    # balance_due = Attribute(field_type=orm.CURRENCY_FIELD)
    # invoice_status = Attribute(field_type=orm.SINGLE_LINE_FIELD)
  
    columns = [
      {'field': 'invoice_number', 'label': 'Invoice Number', 'type': SINGLE_LINE_FIELD},
      {'field': 'case', 'label': 'Case', 'type': 'relation', 'ref_model': 'Case', 'ref_field': 'case_name'},
      {'field': 'bill_to', 'label': 'Bill To', 'type': 'relation', 'ref_model': 'Contact', 'ref_field': 'name'},
      {'field': 'fee_type', 'label': 'Fee Type', 'type': 'relation', 'ref_model': 'FeeType', 'ref_field': 'name'},
      {'field': 'total', 'label': 'Total', 'type': CURRENCY_FIELD},
      {'field': 'balance_due', 'label': 'Balance Due', 'type': CURRENCY_FIELD},
      {'field': 'invoice_status', 'label': 'Status', 'type': SINGLE_LINE_FIELD},
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
