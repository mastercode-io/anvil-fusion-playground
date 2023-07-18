from .BaseForm import *
from .BaseInput import *
from ..app import constants
from ..orm_client.model import Case, Staff

from datetime import datetime, date


class TimeEntryForm(BaseForm):

    def __init__(self, **kwargs):

        self.case = LookupInput(name='case', label='Case', model='Case', text_field='case_name')
        self.staff = LookupInput(name='staff', label='Staff', model='Staff', text_field='full_name',
                                 value=constants.pm_logged_user['staff'])
        self.activity = LookupInput(model='Activity', name='activity', label='Activity')
        self.billable = CheckboxInput(name='billable', label='This time entry is billable', label_position='After',
                                      value=True)
        self.description = MultiLineInput(name='description', label='Description')
        self.date = DateInput(name='date', label='Entry Date', value=date.today())
        self.rate = NumberInput(name='rate', label='Rate', on_change=self.total_calc)
        self.rate_type = RadioButtonInput(name='rate_type', label='Rate type', direction='horizontal',
                                          options=[{'value': 'Per hour'}, {'value': 'Flat'}],
                                          value='Per hour', on_change=self.total_calc)
        self.duration = NumberInput(name='duration', label='Duration (hours)', on_change=self.total_calc)
        self.total = NumberInput(name='total', label='Total', float_label=True)

        sections = [
            {'name': '_', 'rows': [
                [self.date, self.case],
                [self.activity, self.staff],
                [self.description],
                [self.rate, self.duration],
                [self.rate_type, self.billable],
                [self.total],
            ]}
        ]

        super().__init__(model='TimeEntry', sections=sections, width=POPUP_WIDTH_COL3, **kwargs)

    def form_open(self, args):
        super().form_open(args)
        self.total.hide()

    def total_calc(self, args):
        if args['name'] == 'rate_type':
            if self.rate_type.value == 'Flat':
                self.total.value = self.rate.value
                self.duration.value = None
                self.duration.enabled = False
            else:
                self.duration.enabled = True
                if self.rate.value is not None and self.duration.value is not None:
                    self.total.value = round((self.rate.value * self.duration.value), 2)
                else:
                    self.total.value = None
        if args['name'] == 'rate':
            if self.rate_type.value == 'Per hour':
                if self.rate.value is not None and self.duration.value is not None:
                    self.total.value = round((self.rate.value * self.duration.value), 2)
            else:
                self.total.value = self.rate.value
        if args['name'] == 'duration':
            if self.rate_type.value == 'Per hour':
                if self.rate.value is not None and self.duration.value is not None:
                    self.total.value = round((self.rate.value * self.duration.value), 2)
            else:
                self.total.value = self.rate.value
