from ..orm_client.model import *
from .BaseForm import BaseForm, POPUP_WIDTH_COL2
from .BaseInput import *

# payment method options
PAYMENT_METHOD_CARD = 'Card'
PAYMENT_METHOD_CASH = 'Cash'
PAYMENT_METHOD_CHECK = 'Check'
PAYMENT_METHOD_DIRECT_DEPOSIT = 'Direct Deposit'
PAYMENT_METHOD_WIRE_TRANSFER = 'Wire Transfer'
PAYMENT_METHOD_OPTIONS = [
    PAYMENT_METHOD_CARD,
    PAYMENT_METHOD_CASH,
    PAYMENT_METHOD_CHECK,
    PAYMENT_METHOD_DIRECT_DEPOSIT,
    PAYMENT_METHOD_WIRE_TRANSFER,
]

# payment status options
PAYMENT_STATUS_SUCCESS = 'Card'
PAYMENT_STATUS_REFUND = 'Cash'
PAYMENT_STATUS_CHARGEBACK = 'Check'
PAYMENT_STATUS_OPTIONS = [
    PAYMENT_STATUS_SUCCESS,
    PAYMENT_STATUS_REFUND,
    PAYMENT_STATUS_CHARGEBACK,
]


class PaymentForm(BaseForm):
    def __init__(self, **kwargs):
        print('PaymentForm')
        self.case = LookupInput(name='case', label='Case', model='Case', text_field='case_name')
        self.invoice = LookupInput(name='invoice', label='Invoice', model='Invoice', text_field='invoice_number')
        self.bank_account = LookupInput(model='BankAccount', name='bank_account', label='Bank Account')
        self.amount = NumberInput(name='amount', label='Amount')
        self.payment_method = DropdownInput(name='payment_method', label='Payment Method', select='single',
                                            options=PAYMENT_METHOD_OPTIONS)
        self.payment_time = DateTimeInput(name='payment_time', label='Payment Time')
        self.status = DropdownInput(name='status', label='Status', select='single', options=PAYMENT_STATUS_OPTIONS)

        sections = [
            {'name': '_', 'rows': [
                [self.bank_account, self.case],
                [self.payment_method, self.invoice],
                [self.amount, None],
                [self.payment_time, self.status],
            ]}
        ]

        super().__init__(model='Payment', sections=sections, width=POPUP_WIDTH_COL2, **kwargs)
