from .BaseForm import *
from .BaseInput import *


CONTACT_TYPE = ['Person', 'Entity']


class ContactForm(BaseForm):
  def __init__(self, **kwargs):
    
    contact_group = Relationship('ContactGroup')
    entity = Relationship('Entity')
    name = Attribute(field_type=orm.SINGLE_LINE_FIELD)
    email = Attribute(field_type=orm.SINGLE_LINE_FIELD)
    mobile_phone= Attribute(field_type=orm.SINGLE_LINE_FIELD)
    work_phone = Attribute(field_type=orm.SINGLE_LINE_FIELD)
    title_position = Attribute(field_type=orm.SINGLE_LINE_FIELD)
    
    self.type = RadioButtonInput(name='type', label='Type', direction='horizontal', on_change=self.contact_type_change, 
                                         options=[{'value': 'Person'}, {'value': 'Entity'}], value='Person')
    self.contact_group = DropdownInput(name='contact_group', label='Contact Group', options=CONTACT_GROUP)
    self.name = TextInput(name='name', label='Fullname')
    self.entity_name = TextInput(name='entity_name', label='Entity Name')
    self.email = TextInput(name='entity_name', label='Email')
    self.title_position = TextInput(name='title_position', label='Title / Position')
    self.mobile_phone = TextInput(name='mobile_phone', label='Mobile Phone')
    self.work_phone = TextInput(name='work_phone', label='Work Phone')
    self.alternate_phone = TextInput(name='alternate_phone', label='Alternate Phone')
    self.fax = TextInput(name='fax', label='Fax')
    self.website = TextInput(name='website', label='Website')
    self.address_line_1 = TextInput(name='address_line_1', label='Address Line 1')
    self.address_line_2 = TextInput(name='address_line_2', label='Address Line 2')
    self.city_district = TextInput(name='city_district', label='City District')
    self.state_province = TextInput(name='state_province', label='State Province')
    self.postal_code = TextInput(name='postal_code', label='Postal Code')
    # Court Details
    self.add_court_details = CheckboxInput(label='Court Details', save=False, on_change=self.toggleCourtDetails)
    self.department = TextInput(name='department', label='Department')
    self.courtroom = TextInput(name='courtroom', label='Court Room')
    # Biological Details
    self.add_biological_details = CheckboxInput(label='Biological Details', save=False, on_change=self.toggleBiologicalDetails)
    self.dob = DateInput(name='dob', label='Date of Birth')
    self.ssn = TextInput(name='ssn', label='Social Security Number')
    self.country_of_citizenship = TextInput(name='country_of_citizenship', label='Country of Citizenship')
    self.native_language = TextInput(name='native_language', label='Native Language')
    self.education = TextInput(name='education', label='Education')
    self.employment = TextInput(name='employment', label='Employment')
    self.current_employer = TextInput(name='current_employer', label='Current Employee')
    self.time_with_cur_employer = TextInput(name='time_with_cur_employer', label='Time With Current Employer')
    self.community_service = TextInput(name='community_service', label='Community Service')
    self.family_support = TextInput(name='family_support', label='Family Support')
    self.criminal_history = TextInput(name='criminal_history', label='Criminal History')
    self.desc_of_criminal_history = MultiLineInput(name='desc_of_criminal_history', label='Description of Criminal History')
    self.src_of_funds = TextInput(name='src_of_funds', label='Source of Funds')
    # Custody Details
    self.add_custody_details = CheckboxInput(label='Custody Details', save=False, on_change=self.toggleCustodyDetails)
    self.client_in_custody = TextInput(name='client_in_custody', label='Client in Custody')
    self.jail_prison = TextInput(name='jail_prison', label='Jail Prison')
    self.inmate_id = TextInput(name='inmate_id', label='Inmate ID')
    self.bail_status = TextInput(name='bail_status', label='Bail Status')
    # Linked Records
    self.add_linked_records = CheckboxInput(label='Linked Records', save=False, on_change=self.toggleLinkedRecords)
    self.cases = LookupInput(name='cases', label='Cases', text_field='name', data=[*Case.search()])
    self.entities = LookupInput(name='entities', label='Entities', text_field='entity_name', data=[*Contact.search()])
    
    
    sections = [
      {'name': 'contact_info', 'label': 'Contact Info', 'rows': [
        [self.type], 
        [self.contact_group],
        [self.name],
        [self.entity_name],
        [self.title_position, self.email],
        [self.mobile_phone, self.work_phone],
        [self.alternate_phone, self.website]
      ]},
      {'name': 'address_info', 'label': 'Address', 'rows': [
        [self.address_line_1, self.address_line_2],
        [self.city_district, self.state_province],
        [self.postal_code, self.country]
      ]},
      {'name': 'extra_information', 'label': 'Extra Information', 'rows': [
        [self.add_court_details],
        [self.courtroom],
        [self.department],
        [self.courtroom],
        # Biological details
        [self.add_biological_details],
        [self.dob, self.ssn],
        [self.country_of_citizenship, self.native_language],
        [self.education, self.employment],
        [self.current_employer, self.time_with_cur_employer],
        [self.community_service, self.family_support],
        [self.criminal_history, self.desc_of_criminal_history],
        [self.src_of_funds],
        # Custoday details
        [self.add_custody_details],
        [self.client_in_custody, self.jail_prison],
        [self.inmate_id, self.bail_status],
        # Linked records details
        [self.add_linked_records],
        [self.cases, self.entities]
      ]},
    ]

    super().__init__(model='Contact', sections=sections, width=POPUP_WIDTH_COL2, **kwargs)

    
  def after_open(self):
    if not self.data:
      self.entity_name.hide()
      # Court details
      self.department.hide()
      self.courtroom.hide()
      # Linked Records
      self.cases.hide()
      self.entities.hide()
      # Custody Details
      self.client_in_custody.hide()
      self.jail_prison.hide()
      self.inmate_id.hide()
      self.bail_status.hide()
      # Biological Details
      self.dob.hide()
      self.ssn.hide()
      self.country_of_citizenship.hide()
      self.native_language.hide()
      self.education.hide()
      self.employment.hide()
      self.current_employer.hide()
      self.time_with_cur_employer.hide()
      self.community_service.hide()
      self.family_support.hide()
      self.criminal_history.hide()
      self.desc_of_criminal_history.hide()
      self.src_of_funds.hide()
    else:
      self.toggleBiologicalDetails(None)
      self.toggleCourtDetails(None)
      self.toggleCustodyDetails(None)
      self.toggleLinkedRecords(None)

    
  # auto_generate_case_name on_change handler
  def contact_type_change(self, args):
    if self.type.value == 'Entity':
      self.entity_name.show()
      self.name.hide()
    else:
      self.entity_name.hide()
      self.name.show()

  # Linked records handler
  def toggleLinkedRecords(self, args):
    if self.add_linked_records.value is True:
      self.cases.show()
      self.entities.show()
    else:
      self.cases.hide()
      self.entities.hide()
      self.add_linked_records.value = None
      
  # Custody details handler
  def toggleCustodyDetails(self, args):
    if self.add_custody_details.value is True:
      self.client_in_custody.show()
      self.jail_prison.show()
      self.inmate_id.show()
      self.bail_status.show()
    else:
      self.client_in_custody.hide()
      self.jail_prison.hide()
      self.inmate_id.hide()
      self.bail_status.hide()
      self.add_linked_records.value = None

  # Biological details handler
  def toggleBiologicalDetails(self, args):
    if self.add_biological_details.value is True:
      self.dob.show()
      self.ssn.show()
      self.country_of_citizenship.show()
      self.native_language.show()
      self.education.show()
      self.employment.show()
      self.current_employer.show()
      self.time_with_cur_employer.show()
      self.community_service.show()
      self.family_support.show()
      self.criminal_history.show()
      self.desc_of_criminal_history.show()
      self.src_of_funds.show()
    else:
      self.dob.hide()
      self.ssn.hide()
      self.country_of_citizenship.hide()
      self.native_language.hide()
      self.education.hide()
      self.employment.hide()
      self.current_employer.hide()
      self.time_with_cur_employer.hide()
      self.community_service.hide()
      self.family_support.hide()
      self.criminal_history.hide()
      self.desc_of_criminal_history.hide()
      self.src_of_funds.hide()
      self.add_linked_records.value = None

  # Court details handler
  def toggleCourtDetails(self, args):
    if self.add_court_details.value is True:
      self.department.show()
      self.courtroom.show()
    else:
      self.add_court_details.hide()
      self.department.hide()
      self.courtroom.hide()
      self.add_linked_records.value = None