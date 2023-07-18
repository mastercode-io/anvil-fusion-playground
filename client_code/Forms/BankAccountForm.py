from .BaseForm import *
from .BaseInput import *


class BankAccountForm(BaseForm):
    def __init__(self, **kwargs):
        print('BankAccountForm')
        self.account_type = LookupInput(model='BankAccountType', name='account_type', label='Type', select='single')
        self.bank_name = TextInput(name='bank_name', label='Bank Name')
        self.routing_number = TextInput(name='routing_number', label='Routing Number')
        self.account_number = TextInput(name='account_number', label='Account Number')
        self.account_balance = NumberInput(name='account_balance', label='Account Balance')
        self.payment_link = TextInput(name='payment_link', label='Payment Link')
        self.fractional_routing_number = TextInput(name='fractional_routing_number', label='Fractional Routing Number')
        self.check_start_number = TextInput(name='check_start_number', label='Check Start Number')

        self.account_balance.enabled = False

        fields = [
            self.account_type,
            self.bank_name,
            self.routing_number,
            self.account_number,
            self.account_balance,
            self.payment_link,
            self.fractional_routing_number,
            self.check_start_number,
        ]

        super().__init__(model='BankAccount', fields=fields, width=POPUP_WIDTH_COL1, **kwargs)

    def form_open(self, args):
        super().form_open(args)
        self.account_balance.enabled = False
