from .. import Forms
from .BaseForm import *
from .BaseInput import *
from .ContactForm import *

FEE_TYPE_RETAINER = ('Flat Fee', 'Hourly', 'Hybrid Flat/Hourly', 'Hybrid Flat/Contingency')
FEE_TYPE_LITIGATION = ('Contingency', 'Hybrid Flat/Contingency', 'Hybrid Hourly/Contingency')


class CaseForm(BaseForm):

    def __init__(self, **kwargs):

        print('CaseForm')
        self.auto_generate_case_name = CheckboxInput(name='auto_generate_case_name', label='Auto Generate Case Name',
                                                     save=False)
        self.case_name = TextInput(name='case_name', label='Case Name')
        self.assigned_attorneys = LookupInput(name='assigned_attorneys', label='Assigned Attorneys', select='multi',
                                              model='Staff', text_field='full_name')
        self.practice_area = LookupInput(name='practice_area', label='Practice Area', model='PracticeArea')
        self.case_stage = LookupInput(name='case_stage', label='Case Stage', model='CaseStage')
        self.cause_of_action = LookupInput(name='cause_of_action', label='Cause(s) of Action', model='CauseOfAction',
                                           select='multi')
        self.statute_of_limitations = DateInput(name='statute_of_limitations', label='SOL')
        self.add_statute_of_limitations = CheckboxInput(name='add_statute_of_limitations',
                                                        label='Add Statute of Limitations', save=False,
                                                        on_change=self.add_sol)
        self.court = LookupInput(name='court', label='Court', model='Entity', text_field='name',
                                 add_item_label='Add Court', add_item_form=Forms.EntityForm)
        self.department = LookupInput(name='department', label='Department', model='Contact', text_field='entity.name',
                                      add_item_label='Add Judge', add_item_form=Forms.ContactForm)
        self.case_number = TextInput(name='case_number', label='Case Number')
        self.incident_date = DateInput(name='incident_date', label='Incident Date')
        self.incident_location = TextInput(name='incident_location', label='Incident Location')
        self.case_description = MultiLineInput(name='case_description', label='Case Description', rows=5)
        self.clients = LookupInput(name='clients', label='Client(s)', model='Client', text_field='client_name',
                                   select='multi', add_item_label='Add Client', add_item_form=Forms.ClientForm)
        self.contacts = LookupInput(name='contacts', label='Contacts', model='Contact', text_field='full_name',
                                    select='multi', add_item_label='Add Contact', add_item_form=Forms.ContactForm)
        self.staff = LookupInput(name='staff', label='Staff', model='Staff', text_field='full_name', select='multi')
        self.share_case_information_with = LookupInput(name='share_case_information_with',
                                                       label='Share case information with',
                                                       model='Contact', text_field='full_name')
        self.lead = LookupInput(name='lead', label='Lead', model='Lead', text_field='case_name')
        self.fee_type = LookupInput(name='fee_type', label='Fee Type', model='FeeType', on_change=self.fee_type_change)
        # self.fee_type = LookupInput(name='fee_type', label='Fee Type', model='FeeType')
        self.flat_fee_retainer = NumberInput(name='flat_fee_retainer', label='Flat Fee Retainer')
        self.hourly_retainer = NumberInput(name='hourly_retainer', label='Hourly Retainer')
        self.pre_litigation_rate = NumberInput(name='pre_litigation_rate', label='Pre Litigation Rate')
        self.litigation_rate = NumberInput(name='litigation_rate', label='Litigation Rate')
        self.trial_included = CheckboxInput(name='trial_included', label='Trial Included')
        self.hours_limited_on_retainer = CheckboxInput(name='hours_limited_on_retainer',
                                                       label='Hours Limited on Retainer', save=False,
                                                       on_change=self.limit_retainer)
        self.retainer_hours_limit = NumberInput(name='retainer_hours_limit', label='Retainer Hours Limit')
        self.investigator_included = CheckboxInput(name='investigator_included', label='Investigator Included',
                                                   save=False, on_change=self.include_investigator)
        self.investigator_budget = NumberInput(name='investigator_budget', label='Investigator Budget')
        self.record_seal_expungement = CheckboxInput(name='record_seal_expungement',
                                                     label='Record Seal/Expungement Included')

        tabs = [
            {'name': 'case_details', 'label': 'Case Details', 'sections': [
                {'name': 'case_info', 'label': 'Case Information', 'rows': [
                    [self.auto_generate_case_name, None, None],
                    [self.case_name, self.cause_of_action, self.clients],
                    [self.case_number, self.practice_area, self.court],
                    [self.case_stage, self.incident_date, self.department],
                    [None, self.incident_location, self.assigned_attorneys],
                ]},
                {'name': '_', 'cols': [
                    [
                        self.add_statute_of_limitations,
                        self.statute_of_limitations,
                    ],
                    [
                        self.case_description
                    ],
                    [
                        self.staff,
                        self.share_case_information_with,
                        self.lead,
                    ],
                ]},
                {'name': 'case_contacts', 'label': 'Case Contacts', 'rows': [
                    [self.contacts, None],
                ]},
            ]},
            {'name': 'billing', 'label': 'Billing', 'sections': [
                {'name': 'billing_details', 'label': 'Billing Details', 'cols': [
                    [
                        self.fee_type,
                        self.flat_fee_retainer,
                        self.hourly_retainer,
                        self.pre_litigation_rate,
                        self.litigation_rate,
                    ],
                    [
                        self.trial_included,
                        self.hours_limited_on_retainer,
                        self.retainer_hours_limit,
                        self.investigator_included,
                        self.investigator_budget,
                        self.record_seal_expungement,
                    ],
                ]},
            ]},
        ]

        super().__init__(model='Case', tabs=tabs, width=POPUP_WIDTH_COL3, **kwargs)
        self.fullscreen = True

    def form_open(self, args):
        super().form_open(args)
        try:
            if self.data is None or self.data == {}:
                self.case_name.enabled = False
                self.auto_generate_case_name.value = True
                self.statute_of_limitations.hide()
                self.flat_fee_retainer.hide()
                self.retainer_hours_limit.hide()
                self.investigator_budget.hide()
                self.pre_litigation_rate.hide()
                self.litigation_rate.hide()
            # else:
            #     self.generate_case_name(None)
            #     self.limit_retainer(None)
            #     self.include_investigator(None)
            #     self.fee_type_change(None)
            #     if self.statute_of_limitations.value is not None:
            #         self.add_statute_of_limitations.value = True
            #         self.statute_of_limitations.show()
            #     else:
            #         self.statute_of_limitations.hide()
        except Exception as e:
            print(e.__traceback__)

    # auto_generate_case_name on_change handler
    def generate_case_name(self, args):
        if self.auto_generate_case_name.value is True:
            self.case_name.enabled = False
            self.case_name.value = 'AutoGenerated'
        else:
            self.case_name.enabled = True

    # add_statute_of_limitations on_change handler
    def add_sol(self, args):
        if self.add_statute_of_limitations.value is True:
            self.statute_of_limitations.show()
        else:
            self.statute_of_limitations.hide()
            self.statute_of_limitations.value = None

    # hours_limited_on_retainer on_change handler
    def limit_retainer(self, args):
        if self.hours_limited_on_retainer.value is True:
            self.retainer_hours_limit.show()
        else:
            self.retainer_hours_limit.hide()
            self.retainer_hours_limit.value = None

    # investigator_included on_change handler
    def include_investigator(self, args):
        if self.investigator_included.value is True:
            self.investigator_budget.show()
        else:
            self.investigator_budget.hide()
            self.investigator_budget.value = None

    # fee_type on_change handler
    def fee_type_change(self, args):
        if self.fee_type.value is None:
            self.flat_fee_retainer.hide()
            self.flat_fee_retainer.value = None
            self.pre_litigation_rate.hide()
            self.pre_litigation_rate.value = None
            self.litigation_rate.hide()
            self.litigation_rate.value = None
        else:
            if self.fee_type.value['name'] in FEE_TYPE_RETAINER:
                self.flat_fee_retainer.show()
            else:
                self.flat_fee_retainer.hide()
                self.flat_fee_retainer.value = None
            if self.fee_type.value['name'] in FEE_TYPE_LITIGATION:
                self.pre_litigation_rate.show()
                self.litigation_rate.show()
                # print('else', self.fee_type.value['name'])
            else:
                self.pre_litigation_rate.hide()
                self.pre_litigation_rate.value = None
                self.litigation_rate.hide()
                self.litigation_rate.value = None
