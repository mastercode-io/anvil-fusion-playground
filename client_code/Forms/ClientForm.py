from .BaseForm import BaseForm, POPUP_WIDTH_COL3
from .BaseInput import *
from ..orm_client.model import Contact, Entity


class ClientForm(BaseForm):
    def __init__(self, **kwargs):
        self.is_individual = CheckboxInput(name='is_individual', label='Client is an individual', value=True,
                                           enabled=False, on_change=self.show_client_details)
        self.client_name = TextInput(name='client_name', label='Client Name')
        self.contact = LookupInput(name='contact', label='Contact', model='Contact', text_field='full_name')
        self.entity = LookupInput(name='entity', label='Entity', model='Entity', text_field='name',
                                  on_change=self.entity_select)

        sections = [
            {'name': 'client_info', 'rows': [
                [self.is_individual],
                [self.client_name],
                [self.contact],
                [self.entity],
            ]},
        ]

        super().__init__(model='Client', sections=sections, width=POPUP_WIDTH_COL3, **kwargs)

    def form_open(self, args):
        super().form_open(args)
        self.contact.hide()
        self.entity.hide()
        self.show_client_details(None)

    def show_client_details(self, args):
        if self.is_individual.value is True:
            self.contact.show()
            self.entity.hide()
            self.entity.value = None
        else:
            self.entity.show()
            self.contact.hide()
            self.contact.value = None

    def contact_select(self, args):
        self.client_name.value = self.contact.value['name'] if self.contact.value is not None else None

    def entity_select(self, args):
        self.client_name.value = self.entity.value['name'] if self.entity.value is not None else None
