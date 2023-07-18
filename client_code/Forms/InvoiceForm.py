from .BaseForm import BaseForm, BaseSubform
from .BaseInput import *
from .ExpenseForm import *
from .PaymentForm import *
from .TimeEntryForm import *

# expense status options
INVOICE_STATUS_DRAFT = 'draft'
INVOICE_STATUS_APPROVED = 'approved'
INVOICE_STATUS_DUE = 'due'
INVOICE_STATUS_PAID = 'paid'
INVOICE_STATUS_VOID = 'void'
INVOICE_STATUS_OPTIONS = [
    INVOICE_STATUS_DRAFT,
    INVOICE_STATUS_APPROVED,
    INVOICE_STATUS_DUE,
    INVOICE_STATUS_PAID,
    INVOICE_STATUS_VOID,
]


class InvoiceForm(BaseForm):
    def __init__(self, **kwargs):
        print('InvoiceForm')
        self.invoice_number = NumberInput(name='invoice_number', label='Invoice Number')
        self.case = LookupInput(name='case', label='Case', midel='Case', text_field='case_name')
        self.bill_to = LookupInput(name='bill_to', label='Bill To', model='Contact', text_field='full_name')
        self.fee_type = LookupInput(model='FeeType', name='fee_type', label='Fee Type')
        self.total = NumberInput(name='total', label='Total')
        self.balance_due = NumberInput(name='balance_due', label='Balance Due')
        self.status = DropdownInput(name='status', label='Status', options=INVOICE_STATUS_OPTIONS)

        payment_fields = [
            DateTimeInput(name='payment_time', label='Payment Time'),
            NumberInput(name='amount', label='Amount'),
            TextInput(name='payment_method', label='Payment Method'),
            TextInput(name='status', label='Status', select='single')
        ]
        self.payments = BaseSubform(name='payments', fields=payment_fields, model='Payment', link_model='Invoice',
                                    link_field='invoice', save=False)

        time_entry_fields = [
            DateInput(name='date', label='Entry Date', ),
            LookupInput(name='staff', label='Staff', model='Staff', text_field='full_name'),
            LookupInput(model='Activity', name='activity', label='Activity'),
            MultiLineInput(name='description', label='Description'),
            CheckboxInput(name='billable', label='This time entry is billable', label_position='After', value=True),
            RadioButtonInput(name='rate_type', label='Rate type', direction='horizontal',
                             options=[{'value': 'Per hour'}, {'value': 'Flat'}]),
            NumberInput(name='rate', label='Rate'),
            NumberInput(name='duration', label='Duration (hours)'),
            NumberInput(name='total', label='Total')
        ]
        self.time_entries = BaseSubform(name='time_entries', fields=time_entry_fields, model='TimeEntry',
                                        link_model='Invoice', link_field='invoice', save=False)

        expense_fields = [
            DateInput(name='date', label='Date'),
            LookupInput(name='staff', label='Staff', model='Staff', text_field='full_name'),
            LookupInput(model='Activity', name='activity', label='Activity'),
            MultiLineInput(name='description', label='Description'),
            NumberInput(name='amount', label='Amount'),
            NumberInput(name='quantity', label='Quantity'),
            NumberInput(name='reduction', label='Reduction'),
            NumberInput(name='total', label='Total'),
            CheckboxInput(name='billable', label='Billable'),
            DropdownInput(name='status', label='Status', select='single', options=EXPENSE_STATUS_OPTIONS)
        ]
        self.expenses = BaseSubform(name='expenses', fields=expense_fields, model='Expense', link_model='Invoice',
                                    link_field='invoice', save=False)

        adjustment_fields = [
            DropdownInput(name='type', label='Type', options=['Add', 'Discount']),
            DropdownInput(name='applied_to', label='Applied To',
                          options=['Flat Fees', 'Time Entries', 'Expenses', 'Sub-Total']),
            MultiLineInput(name='description', label='Description'),
            NumberInput(name='basis', label='Basis'),
            NumberInput(name='adjustment_amount', label='Adjustment $'),
            NumberInput(name='adjustment_percent', label='Adjustment %'),
        ]
        self.adjustments = BaseSubform(name='adjustments', fields=adjustment_fields)

        sections = [
            {'name': '_', 'rows': [
                [self.case, self.fee_type],
                [self.invoice_number, self.total],
                [self.bill_to, self.balance_due],
                [None, self.status],
            ]},
            {'name': 'time_entries', 'label': 'Time Entries', 'rows': [[self.time_entries]]},
            {'name': 'expenses', 'label': 'Expenses', 'rows': [[self.expenses]]},
            {'name': 'adjustments', 'label': 'Adjustments', 'rows': [[self.adjustments]]},
            {'name': 'payments', 'label': 'Payments', 'rows': [[self.payments]]},
        ]

        super().__init__(model='Invoice', sections=sections, width=POPUP_WIDTH_COL3, **kwargs)
        self.fullscreen = True
