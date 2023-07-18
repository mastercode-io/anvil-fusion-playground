from ..orm_client.model import *
from .BaseForm import BaseForm, POPUP_WIDTH_COL2
from .BaseInput import *

import datetime


class TaskForm(BaseForm):
    def __init__(self, **kwargs):

        print('TaskForm')

        self.activity = LookupInput(model='Activity', name='activity', label='Task Name')
        self.notes = MultiLineInput(name='notes', label='Notes', rows=5)
        self.priority = DropdownInput(name='priority', label='Priority', options=['Normal', 'High'])
        self.assigned_staff = LookupInput(name='assigned_staff', label='Assigned Staff', select='multi',
                                          model='Staff', text_field='full_name')
        self.case = LookupInput(name='case', label='Case', select='single',
                                model='Case', text_field='case_name')
        self.documents = FileUploadInput(name='documents', label='Documents', float_label=True, save=False)
        self.due_date = DateInput(name='due_date', label='Due Date', value=datetime.date.today())
        self.no_due_date = CheckboxInput(name='no_due_date', label='No due date', save=False,
                                         on_change=self.no_due_date_toggle)
        self.no_case = CheckboxInput(name='no_case', label='Task is not related to case', save=False,
                                     on_change=self.no_case_toggle)

        sections = [
            {'name': '_', 'cols': [
                [
                    self.activity,
                    self.priority,
                    self.assigned_staff
                ],
                [
                    self.notes
                ]
            ]},
            {'name': '_', 'rows': [
                [self.no_due_date, self.no_case],
                [self.due_date, self.case],
                [self.documents]
            ]}
        ]

        super().__init__(model='Task', sections=sections, width=POPUP_WIDTH_COL2, **kwargs)

    def form_open(self, args):
        super().form_open(args)
        if self.priority.value is None:
            self.priority.value = 'Normal'
        if self.activity.value is not None:
            if self.case.value is None:
                self.case.enabled = False
                self.no_case.value = True
            if self.due_date.value is None:
                self.due_date.enabled = False
                self.no_due_date = True

    def no_due_date_toggle(self, args):
        if self.no_due_date.value is True:
            self.due_date.value = None
            self.due_date.enabled = False
        else:
            self.due_date.enabled = True

    def no_case_toggle(self, args):
        if self.no_case.value is True:
            self.case.value = None
            self.case.enabled = False
        else:
            self.case.enabled = True
