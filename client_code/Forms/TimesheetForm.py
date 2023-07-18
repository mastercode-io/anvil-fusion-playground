from .BaseForm import BaseForm, POPUP_WIDTH_COL2
from .BaseInput import *
from ..app import constants
from ..orm_client.model import Staff

from datetime import datetime, timedelta


class TimesheetForm(BaseForm):
    def __init__(self, **kwargs):
        print('TimesheetForm')

        self.staff = LookupInput(name='staff', label='Staff', model='Staff', text_field='full_name',
                                 value=constants.pm_logged_user['staff'])
        self.clock_in_time = DateTimeInput(name='clock_in_time', label='Clock In Time', value=datetime.now(),
                                           on_change=self.calc_earned_pay)
        self.clock_out_time = DateTimeInput(name='clock_out_time', label='Clock Out Time',
                                            on_change=self.calc_earned_pay)
        self.hours_worked = NumberInput(name='hours_worked', label='Hours Worked', enabled=False)
        self.earned_pay = NumberInput(name='earned_pay', label='Earned Pay', enabled=False)
        self.approved = CheckboxInput(name='approved', label='Approved')
        self.approved_by = LookupInput(name='approved_by', label='Approved By', model='Staff', text_field='full_name')

        sections = [
            {'name': '_', 'rows': [
                [self.staff],
                [self.clock_in_time, self.hours_worked],
                [self.clock_out_time, self.earned_pay],
                [self.approved_by, self.approved],
            ]}
        ]

        super().__init__(model='Timesheet', sections=sections, width=POPUP_WIDTH_COL2, **kwargs)

    def form_open(self, args):
        super().form_open(args)

    def calc_earned_pay(self, args):
        if self.clock_in_time.value is not None and self.clock_out_time.value is not None:
            if args['name'] == 'clock_out_time':
                if self.clock_out_time.value <= self.clock_in_time.value:
                    self.clock_out_time.value = self.clock_in_time.value + timedelta(hours=1)
            self.hours_worked.value = (self.clock_out_time.value - self.clock_in_time.value).total_seconds() / 3600
        if self.hours_worked.value is not None and self.staff.value['pay_type'].lower() == 'hourly':
            self.earned_pay.value = self.hours_worked.value * self.staff.value['pay_rate']
        else:
            self.earned_pay.value = None
