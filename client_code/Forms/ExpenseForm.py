from ..orm_client.model import *
from .BaseForm import BaseForm, POPUP_WIDTH_COL2
from .BaseInput import *

import datetime

# expense status options
EXPENSE_STATUS_OPEN = 'Open'
EXPENSE_STATUS_INVOICED = 'Invoiced'
EXPENSE_STATUS_OPTIONS = [
    EXPENSE_STATUS_OPEN,
    EXPENSE_STATUS_INVOICED,
]


class ExpenseForm(BaseForm):
    def __init__(self, **kwargs):
        print('ExpenseForm')
        self.date = DateInput(name='date', label='Date', value=datetime.date.today())
        self.activity = LookupInput(model='Activity', name='activity', label='Activity')
        self.description = MultiLineInput(name='description', label='Description')
        self.amount = NumberInput(name='amount', label='Amount', value=0)
        self.quantity = NumberInput(name='quantity', label='Quantity', value=1)
        self.total = NumberInput(name='total', label='Total')
        self.staff = LookupInput(name='staff', label='Staff', model='Staff', text_field='full_name')
        self.case = LookupInput(name='case', label='Case', model='Case', text_field='case_name')
        self.billable = CheckboxInput(name='billable', label='Billable', value=True)
        self.reduction = NumberInput(name='reduction', label='Reduction')
        self.status = DropdownInput(name='status', label='Status', select='single', options=EXPENSE_STATUS_OPTIONS,
                                    value=EXPENSE_STATUS_OPEN, enabled=False)
        self.receipt_invoice = FileUploadInput(name='receipt_invoice', label='Receipt Invoice', save=False)

        sections = [
            {'name': '_', 'rows': [
                [self.date, self.case],
                [self.activity, self.staff],
                [self.description],
                [self.amount, self.reduction],
                [self.quantity, self.billable],
                [self.receipt_invoice],
                # hidden fields
                [self.total, self.status],
            ]}
        ]

        super().__init__(model='Expense', sections=sections, width=POPUP_WIDTH_COL2, **kwargs)

    def form_open(self, args):
        super().form_open(args)
        self.total.hide()
        self.status.hide()

    def form_save(self, args):
        total = self.amount.value * self.quantity.value
        if self.reduction.value is not None:
            total -= self.reduction.value
        self.total.value = total

        super().form_save(args)
