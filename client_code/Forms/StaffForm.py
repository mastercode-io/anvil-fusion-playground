from ..orm_client.model import *
from .BaseForm import BaseForm, POPUP_WIDTH_COL3
from .BaseInput import *

PM_PAYMENT_TYPE_LIST = [
    {'uid': 'hourly', 'name': 'Hourly'},
    {'uid': 'salary', 'name': 'Salary'},
]
PM_STATE_LIST = [
    {'uid': 'AL', 'name': 'Alabama'},
    {'uid': 'AK', 'name': 'Alaska'},
    {'uid': 'AZ', 'name': 'Arizona'},
    {'uid': 'AR', 'name': 'Arkansas'},
    {'uid': 'CA', 'name': 'California'},
    {'uid': 'CO', 'name': 'Colorado'},
    {'uid': 'CT', 'name': 'Connecticut'},
    {'uid': 'DE', 'name': 'Delaware'},
    {'uid': 'DC', 'name': 'District Of Columbia'},
    {'uid': 'FL', 'name': 'Florida'},
    {'uid': 'GA', 'name': 'Georgia'},
    {'uid': 'HI', 'name': 'Hawaii'},
    {'uid': 'ID', 'name': 'Idaho'},
    {'uid': 'IL', 'name': 'Illinois'},
    {'uid': 'IN', 'name': 'Indiana'},
    {'uid': 'IA', 'name': 'Iowa'},
    {'uid': 'KS', 'name': 'Kansas'},
    {'uid': 'KY', 'name': 'Kentucky'},
    {'uid': 'LA', 'name': 'Louisiana'},
    {'uid': 'ME', 'name': 'Maine'},
    {'uid': 'MD', 'name': 'Maryland'},
    {'uid': 'MA', 'name': 'Massachusetts'},
    {'uid': 'MI', 'name': 'Michigan'},
    {'uid': 'MN', 'name': 'Minnesota'},
    {'uid': 'MS', 'name': 'Mississippi'},
    {'uid': 'MO', 'name': 'Missouri'},
    {'uid': 'MT', 'name': 'Montana'},
    {'uid': 'NE', 'name': 'Nebraska'},
    {'uid': 'NV', 'name': 'Nevada'},
    {'uid': 'NH', 'name': 'New Hampshire'},
    {'uid': 'NJ', 'name': 'New Jersey'},
    {'uid': 'NM', 'name': 'New Mexico'},
    {'uid': 'NY', 'name': 'New York'},
    {'uid': 'NC', 'name': 'North Carolina'},
    {'uid': 'ND', 'name': 'North Dakota'},
    {'uid': 'OH', 'name': 'Ohio'},
    {'uid': 'OK', 'name': 'Oklahoma'},
    {'uid': 'OR', 'name': 'Oregon'},
    {'uid': 'PA', 'name': 'Pennsylvania'},
    {'uid': 'RI', 'name': 'Rhode Island'},
    {'uid': 'SC', 'name': 'South Carolina'},
    {'uid': 'SD', 'name': 'South Dakota'},
    {'uid': 'TN', 'name': 'Tennessee'},
    {'uid': 'TX', 'name': 'Texas'},
    {'uid': 'UT', 'name': 'Utah'},
    {'uid': 'VT', 'name': 'Vermont'},
    {'uid': 'VA', 'name': 'Virginia'},
    {'uid': 'WA', 'name': 'Washington'},
    {'uid': 'WV', 'name': 'West Virginia'},
    {'uid': 'WI', 'name': 'Wisconsin'},
    {'uid': 'WY', 'name': 'Wyoming'},
]
PM_GENDER_LIST = [
    {'uid': 'male', 'name': 'Male'},
    {'uid': 'female', 'name': 'Female'},
    {'uid': 'other', 'name': 'Other'},
]
PM_RACE_LIST = [
    {'uid': 'american_indian', 'name': 'American Indian or Alaska Native'},
    {'uid': 'asian', 'name': 'Asian'},
    {'uid': 'black', 'name': 'Black or African American'},
    {'uid': 'hispanic', 'name': 'Hispanic or Latino'},
    {'uid': 'hawaiian', 'name': 'Native Hawaiian or Other Pacific Islander'},
    {'uid': 'caucasian', 'name': 'Caucasian'},
    {'uid': 'other', 'name': 'Other'},
]
PM_EMPLOYMENT_STATUS_LIST = [
    {'uid': 'active', 'name': 'Active'},
    {'uid': 'inactive', 'name': 'Inactive'},
]


class StaffForm(BaseForm):
    def __init__(self, **kwargs):
        print('StaffForm')
        # generale information
        self.branch = LookupInput(model='Branch', name='branch', label='Branch')
        self.first_name = TextInput(name='first_name', label='First Name')
        self.last_name = TextInput(name='last_name', label='Last Name')
        self.staff_group = LookupInput(model='StaffGroup', name='staff_group', label='Staff Group')
        self.user_name = TextInput(name='user_name', label='User Name')
        self.work_email = TextInput(name='work_email', label='Work Email')
        self.work_phone = TextInput(name='work_phone', label='Work Phone')
        self.extension = TextInput(name='extension', label='Extension')
        # compensation
        self.pay_type = DropdownInput(name='pay_type', label='Pay Type', options=PM_PAYMENT_TYPE_LIST)
        self.pay_rate = NumberInput(name='pay_rate', label='Pay Rate')
        self.mileage_reimbursement = NumberInput(name='mileage_reimbursement', label='Mileage Reimbursement')
        self.enable_overtime = CheckboxInput(name='enable_overtime', label='Enable Overtime', value=True,
                                             on_change=self.field_rules)
        self.overtime_rate = NumberInput(name='overtime_rate', label='Overtime Rate')
        self.weekly_base_hours = NumberInput(name='weekly_base_hours', label='Weekly Base Hours')
        self.enable_break_time_deduction = CheckboxInput(name='enable_break_time_deduction',
                                                         label='Enable Break Time Deduction', value=True,
                                                         on_change=self.field_rules)
        self.break_time_hour_base = NumberInput(name='break_time_hour_base', label='Break Time Hour Base')
        self.break_time_rate = NumberInput(name='break_time_rate', label='Break Time Rate')
        self.enable_performance_incentives = CheckboxInput(name='enable_performance_incentives',
                                                           label='Enable Performance ', value=True,
                                                           on_change=self.field_rules)
        self.intake_performance_incentive = NumberInput(name='intake_performance_incentive',
                                                        label='Intake Performance ')
        self.override_incentive = NumberInput(name='override_incentive', label='Override Incentive')
        self.manager_incentive = NumberInput(name='manager_incentive', label='Manager Incentive')
        self.referral_incentive = NumberInput(name='referral_incentive', label='Referral Incentive')
        # employment
        self.employment_status = DropdownInput(name='employment_status', label='Employment Status',
                                               options=PM_EMPLOYMENT_STATUS_LIST, value='active')
        self.hire_date = DateInput(name='hire_date', label='Hire Date')
        self.leave_date = DateInput(name='leave_date', label='Leave Date')
        self.manager = LookupInput(name='manager', label='Manager', model='Staff', text_field='full_name')
        self.bar_number = TextInput(name='bar_number', label='Bar Number')
        self.bar_state = DropdownInput(name='bar_state', label='Bar State', options=PM_STATE_LIST)
        self.bar_admission = DateInput(name='bar_admission', label='Bar Admission')
        # personal information
        self.date_of_birth = DateInput(name='date_of_birth', label='Date of Birth')
        self.personal_phone = TextInput(name='personal_phone', label='Personal Phone')
        self.personal_email = TextInput(name='personal_email', label='Personal Email')
        self.personal_address = MultiLineInput(name='personal_address', label='Personal Address', rows=4)
        self.personal_ssn = TextInput(name='personal_ssn', label='Personal SSN')
        self.personal_gender = DropdownInput(name='personal_gender', label='Personal Gender', options=PM_GENDER_LIST)
        self.personal_race = DropdownInput(name='personal_race', label='Personal Race', options=PM_RACE_LIST)
        self.bank_name = TextInput(name='bank_name', label='Bank Name')
        self.bank_routing_number = TextInput(name='bank_routing_number', label='Bank Routing Number')
        self.bank_account_number = TextInput(name='bank_account_number', label='Bank Account Number')
        self.emergency_contact_name = TextInput(name='emergency_contact_name', label='Emergency Contact Name')
        self.emergency_contact_phone = TextInput(name='emergency_contact_phone', label='Emergency Contact Phone')
        self.emergency_contact_email = TextInput(name='emergency_contact_email', label='Emergency Contact Email')
        self.emergency_contact_address = MultiLineInput(name='emergency_contact_address',
                                                        label='Emergency Contact Address', rows=4)

        tabs = [
            {'name': 'general_information', 'label': 'General Information', 'sections': [
                {'name': '_', 'rows': [
                    [self.first_name, self.branch],
                    [self.last_name, self.staff_group],
                    [self.work_email, self.user_name],
                    [self.work_phone, None],
                    [self.extension, None],
                ]},
                {'name': 'employment', 'label': 'Employment', 'rows': [
                    [self.employment_status, self.bar_number],
                    [self.hire_date, self.bar_state],
                    [self.leave_date, self.bar_admission],
                    [self.manager, None],
                ]}
            ]},
            {'name': 'compensation', 'label': 'Compensation', 'sections': [
                {'name': 'compensation', 'label': 'Compensation', 'cols': [
                    [
                        self.pay_type,
                        self.pay_rate,
                        self.mileage_reimbursement,
                        self.enable_performance_incentives,
                        self.intake_performance_incentive,
                        self.override_incentive,
                        self.manager_incentive,
                    ],
                    [
                        self.enable_overtime,
                        self.overtime_rate,
                        self.weekly_base_hours,
                        self.enable_break_time_deduction,
                        self.break_time_rate,
                        self.break_time_hour_base,
                    ]
                ]},
                {'name': 'direct_deposit', 'label': 'Direct Deposit', 'cols': [
                    [self.bank_name, self.bank_routing_number, self.bank_account_number],
                    [],
                ]},
            ]},
            {'name': 'personal_information', 'label': 'Personal Information', 'sections': [
                {'name': '_', 'cols': [
                    [
                        self.personal_phone,
                        self.personal_email,
                        self.personal_address,
                    ],
                    [
                        self.date_of_birth,
                        self.personal_gender,
                        self.personal_race,
                        self.personal_ssn,
                    ]
                ]},
                {'name': 'emergency_contact', 'label': 'Emergency Contact', 'cols': [
                    [
                        self.emergency_contact_name,
                        self.emergency_contact_phone,
                        self.emergency_contact_email,
                    ],
                    [
                        self.emergency_contact_address,
                    ]
                ]}
            ]},
        ]

        super().__init__(model='Staff', tabs=tabs, width=POPUP_WIDTH_COL3, **kwargs)
        self.fullscreen = True

    def field_rules(self, args):
        if args['name'] == 'enable_overtime':
            if self.enable_overtime.value is True:
                self.overtime_rate.show()
                self.weekly_base_hours.show()
            else:
                self.overtime_rate.hide()
                self.weekly_base_hours.hide()
                self.overtime_rate.value = None
                self.weekly_base_hours.value = None
        elif args['name'] == 'enable_break_time_deduction':
            if self.enable_break_time_deduction.value is True:
                self.break_time_rate.show()
                self.break_time_hour_base.show()
            else:
                self.break_time_rate.hide()
                self.break_time_hour_base.hide()
                self.break_time_rate.value = None
                self.break_time_hour_base.value = None
        elif args['name'] == 'enable_performance_incentives':
            if self.enable_performance_incentives.value is True:
                self.intake_performance_incentive.show()
                self.override_incentive.show()
                self.manager_incentive.show()
            else:
                self.intake_performance_incentive.hide()
                self.override_incentive.hide()
                self.manager_incentive.hide()
                self.intake_performance_incentive.value = None
                self.override_incentive.value = None
                self.manager_incentive.value = None
