from ..orm_client.model import Contact, ContactGroup, Entity
from .. import Forms
from .BaseForm import BaseForm, POPUP_WIDTH_COL3
from .BaseInput import *
from .ComboInput import ComboInput


class ContactForm(BaseForm):

    def __init__(self, **kwargs):
        print('ContactForm')
        self.first_name = TextInput(name='name', label='Contact Name', save=False)
        self.last_name = TextInput(name='last_name', label='Last Name', save=False)
        self.contact_group = LookupInput(model='ContactGroup', name='contact_group', label='Contact Group',
                                         add_item_label='Add Group', add_item_model='ContactGroup',
                                         add_item_form=BaseForm)
        self.entity = LookupInput(name='entity', label='Entity', model='Entity', text_field='name',
                                  add_item_label='Add Entity', add_item_form=Forms.EntityForm)
        self.email = TextInput(name='email', label='Email')
        self.mobile_phone = TextInput(name='mobile_phone', label='Mobile Phone')
        self.work_phone = TextInput(name='work_phone', label='Work Phone')
        self.title_position = TextInput(name='title_position', label='Title / Position')

        self.personal_details = ComboInput(name='personal_details', model='Contact')
        self.address = ComboInput(name='address', model='Contact')
        self.employment = ComboInput(name='employment', model='Contact')
        self.criminal_history = ComboInput(name='criminal_history', model='Contact', cols=2)
        self.additional_info = ComboInput(name='additional_info', label='Additional Information', model='Contact')

        sections = [
            {'name': '_', 'rows': [
                [self.first_name, self.last_name],
                [self.email, self.contact_group],
                [self.mobile_phone, self.entity],
                [self.work_phone, self.title_position],
                [self.personal_details, self.address],
                [self.employment, self.additional_info],
                [self.criminal_history]
            ]}
        ]

        super().__init__(model='Contact', sections=sections, width=POPUP_WIDTH_COL3, **kwargs)
