import anvil.server
from .particles import model_type, Attribute, Relationship, Computed
from . import particles as orm
from . import enumerations as enums

MODEL_MODULE_NAME = 'orm_client.model'


# --------------------------------
# Application object model classes
# --------------------------------
@model_type
class Tenant:
    model_type = enums.ModelTypes.SYSTEM
    name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)


@model_type
class Users:
    model_type = enums.ModelTypes.SYSTEM
    email = Attribute(field_type=enums.FieldTypes.EMAIL)
    enabled = Attribute(field_type=enums.FieldTypes.BOOLEAN)
    last_login = Attribute(field_type=enums.FieldTypes.DATETIME)
    password_hash = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    n_password_failures = Attribute(field_type=enums.FieldTypes.NUMBER)
    confirmed_email = Attribute(field_type=enums.FieldTypes.BOOLEAN)
    signed_up = Attribute(field_type=enums.FieldTypes.DATETIME)


@model_type
class UserProfile:
    name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    title = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)


@model_type
class appAuditLog:
    model_type = enums.ModelTypes.SYSTEM
    table_name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    record_uid = Attribute(field_type=enums.FieldTypes.UID)
    action_type = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    action_time = Attribute(field_type=enums.FieldTypes.DATETIME)
    action_by = Attribute(field_type=enums.FieldTypes.UID)
    previous_state = Attribute(field_type=enums.FieldTypes.OBJECT)
    new_state = Attribute(field_type=enums.FieldTypes.OBJECT)


@model_type
class appErrorLog:
    model_type = enums.ModelTypes.SYSTEM
    component = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    action = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    error_message = Attribute(field_type=enums.FieldTypes.MULTI_LINE)
    error_time = Attribute(field_type=enums.FieldTypes.DATETIME)
    user_uid = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)


@model_type
class appGridViews:
    name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    config = Attribute(field_type=enums.FieldTypes.OBJECT)
    permissions = Attribute(field_type=enums.FieldTypes.OBJECT)


@model_type
class Files:
    name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    mime_type = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    size = Attribute(field_type=enums.FieldTypes.NUMBER)
    meta_info = Attribute(field_type=enums.FieldTypes.OBJECT)
    content = Attribute(field_type=enums.FieldTypes.MEDIA)
    case_uid = Attribute(field_type=enums.FieldTypes.UID)
    link_name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    link_uid = Attribute(field_type=enums.FieldTypes.UID)


# -------------------------
# Data object model classes
# -------------------------
@model_type
class Activity:
    _title = 'name'
    name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)


@model_type
class BankAccount:
    _title = 'account_type'

    account_type = Relationship('BankAccountType')
    bank_name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    routing_number = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    account_number = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    account_balance = Attribute(field_type=enums.FieldTypes.CURRENCY)
    payment_link = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    """Hidden Fields"""
    fractional_routing_number = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    check_start_number = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)


@model_type
class BankAccountType:
    _title = 'name'
    name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)


@model_type
class Branch:
    _title = 'name'

    name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    phone = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    email = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    address = Attribute(field_type=enums.FieldTypes.MULTI_LINE)


@model_type
class Case:
    _title = 'case_name'

    case_name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    assigned_attorneys = Relationship('Staff', with_many=True)
    practice_area = Relationship('PracticeArea')
    case_stage = Relationship('CaseStage')
    cause_of_action = Relationship('CauseOfAction', with_many=True)
    close_date = Attribute(field_type=enums.FieldTypes.DATE)
    """Hidden Fields (should be displayed on Case Dashboard - in order of Case Dashboard template - not the order listed below)"""
    case_status = Relationship('CaseStatus')
    statute_of_limitations = Attribute(field_type=enums.FieldTypes.DATE)
    court = Relationship('Entity')
    department = Relationship('Contact')
    case_number = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    incident_date = Attribute(field_type=enums.FieldTypes.DATE)
    incident_location = Attribute(field_type=enums.FieldTypes.ADDRESS)
    case_description = Attribute(field_type=enums.FieldTypes.MULTI_LINE)
    clients = Relationship('Client', with_many=True)
    contacts = Relationship('Contact', with_many=True)
    staff = Relationship('Staff', with_many=True)
    share_case_information_with = Relationship('Contact')
    lead = Relationship('Lead')
    # billing
    fee_type = Relationship('FeeType')
    flat_fee_retainer = Attribute(field_type=enums.FieldTypes.CURRENCY)
    hourly_retainer = Attribute(field_type=enums.FieldTypes.CURRENCY)
    pre_litigation_rate = Attribute(field_type=enums.FieldTypes.CURRENCY)
    litigation_rate = Attribute(field_type=enums.FieldTypes.CURRENCY)
    trial_included = Attribute(field_type=enums.FieldTypes.BOOLEAN)
    retainer_hours_limit = Attribute(field_type=enums.FieldTypes.NUMBER)
    investigator = Attribute(field_type=enums.FieldTypes.BOOLEAN)
    investigator_budget = Attribute(field_type=enums.FieldTypes.CURRENCY)
    record_seal_expungement = Attribute(field_type=enums.FieldTypes.BOOLEAN)
    # open date - date from created_time field
    """
  The fields below should be relational to Clients - in Creator this information gets populated based on the 
  Group selection of each contact. I don't think we need actual need the fields below - we just need to fetch
  the data to display on the case dashboard.
  """
    # client_in_custody = Attribute(field_type=enums.FieldTypes.BOOLEAN)
    # jail_prison = Relationship('Entity')
    # inmate_id = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    # bail_status = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)


@model_type
class CaseContact:
    _title = 'contact'

    case = Relationship('Case')
    contact = Relationship('Contact')
    role = Relationship('ContactRole')


@model_type
class CaseStage:
    _title = 'name'
    name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)


@model_type
class CaseStatus:
    _title = 'name'
    name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)


@model_type
class CauseOfAction:
    _title = 'cause_of_action'

    type_of_action = Relationship('TypeOfAction')
    statute_id = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    cause_of_action = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    penalty = Attribute(field_type=enums.FieldTypes.MULTI_LINE)


@model_type
class Check:
    _title = 'check_number'

    check_number = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    date = Attribute(field_type=enums.FieldTypes.DATE)
    payee = Relationship('Contact')
    amount = Attribute(field_type=enums.FieldTypes.CURRENCY)
    memo = Attribute(field_type=enums.FieldTypes.MULTI_LINE)
    reference = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    """Hidden Fields and or detail view"""
    bank_account = Relationship('BankAccount')


@model_type
class Client:
    _title = 'client_name'

    client_name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    # need to display group as "Client" if all clients and contacts will be on same report
    # email = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    # mobile_phone= Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    # work_phone = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    # cases = Relationship('Case')
    """Hidden Fields and or detail view"""
    is_individual = Attribute(field_type=enums.FieldTypes.BOOLEAN)
    contact = Relationship('Contact')
    entity = Relationship('Entity')


@model_type
class Contact:
    _title = 'full_name'

    contact_group = Relationship('ContactGroup')
    entity = Relationship('Entity')
    first_name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    last_name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    email = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    mobile_phone = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    work_phone = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    alternate_phone = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    title_position = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    """Hidden Fields and or detail view"""

    personal_details_schema = {
        'dob': Attribute(field_type=enums.FieldTypes.DATE),
        'ssn': Attribute(field_type=enums.FieldTypes.SINGLE_LINE),
        'country_of_citizenship': Attribute(field_type=enums.FieldTypes.ENUM_SINGLE),
        'native_language': Attribute(field_type=enums.FieldTypes.ENUM_SINGLE),
        'education': Attribute(field_type=enums.FieldTypes.ENUM_SINGLE),
    }
    personal_details = Attribute(field_type=enums.FieldTypes.OBJECT, schema=personal_details_schema)

    address_schema = {
        'address_line_1': Attribute(field_type=enums.FieldTypes.SINGLE_LINE),
        'address_line_2': Attribute(field_type=enums.FieldTypes.SINGLE_LINE),
        'city_district': Attribute(field_type=enums.FieldTypes.SINGLE_LINE),
        'state_province': Attribute(field_type=enums.FieldTypes.SINGLE_LINE),
        'postal_code': Attribute(field_type=enums.FieldTypes.SINGLE_LINE),
    }
    address = Attribute(field_type=enums.FieldTypes.OBJECT, schema=address_schema)

    employment_schema = {
        'employment': Attribute(field_type=enums.FieldTypes.SINGLE_LINE),
        'current_employer': Attribute(field_type=enums.FieldTypes.SINGLE_LINE),
        'time_with_current_employer': Attribute(field_type=enums.FieldTypes.SINGLE_LINE,
                                                label='Time with Current Employer'),
    }
    employment = Attribute(field_type=enums.FieldTypes.OBJECT, schema=employment_schema)

    criminal_history_schema = {
        'criminal_history': Attribute(field_type=enums.FieldTypes.SINGLE_LINE),
        'description': Attribute(field_type=enums.FieldTypes.MULTI_LINE),
    }
    criminal_history = Attribute(field_type=enums.FieldTypes.OBJECT, schema=criminal_history_schema)

    additional_info_schema = {
        'family_support': Attribute(field_type=enums.FieldTypes.SINGLE_LINE),
        'source_of_funds': Attribute(field_type=enums.FieldTypes.SINGLE_LINE, label='Source of Funds'),
        'community_service': Attribute(field_type=enums.FieldTypes.SINGLE_LINE),
    }
    additional_info = Attribute(field_type=enums.FieldTypes.OBJECT, schema=additional_info_schema)

    @staticmethod
    def get_full_name(args):
        return f"{args['first_name']} {args['last_name']}"
    full_name = Computed(('first_name', 'last_name'), 'get_full_name')


@model_type
class ContactGroup:
    _title = 'name'
    name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)


@model_type
class ContactRole:
    _title = 'name'
    name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)


@model_type
class Entity:
    _title = 'name'

    name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    entity_type = Relationship('EntityType')
    phone = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    email = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    address = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    website = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    primary_contact = Relationship('Contact')


@model_type
class EntityType:
    _title = 'name'
    name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)


@model_type
class Event:
    _title = 'activity'

    start_time = Attribute(field_type=enums.FieldTypes.DATETIME)
    end_time = Attribute(field_type=enums.FieldTypes.DATETIME)
    case = Relationship('Case')
    activity = Relationship('Activity')
    staff = Relationship('Staff', with_many=True)
    location = Relationship('Entity')
    department = Relationship('Contact')
    client_attendance_required = Attribute(field_type=enums.FieldTypes.BOOLEAN)
    """Hidden Fields and or detail view"""
    no_case = Attribute(field_type=enums.FieldTypes.BOOLEAN)
    notes = Attribute(field_type=enums.FieldTypes.MULTI_LINE)
    documents = Attribute(field_type=enums.FieldTypes.FILE_UPLOAD)
    contact = Relationship('Contact', with_many=True)
    client_update = Attribute(field_type=enums.FieldTypes.BOOLEAN)


@model_type
class Expense:
    _title = 'description'

    date = Attribute(field_type=enums.FieldTypes.DATE)
    activity = Relationship('Activity')
    description = Attribute(field_type=enums.FieldTypes.MULTI_LINE)
    amount = Attribute(field_type=enums.FieldTypes.CURRENCY)
    quantity = Attribute(field_type=enums.FieldTypes.NUMBER)
    total = Attribute(field_type=enums.FieldTypes.CURRENCY)
    staff = Relationship('Staff')
    case = Relationship('Case')
    invoice = Relationship('Invoice')
    """Hidden Fields and or detail view"""
    billable = Attribute(field_type=enums.FieldTypes.BOOLEAN)
    reduction = Attribute(field_type=enums.FieldTypes.NUMBER)
    status = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    receipt_invoice = Attribute(field_type=enums.FieldTypes.FILE_UPLOAD)


@model_type
class FeeType:
    _title = 'name'
    name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)


@model_type
class Invoice:
    _title = 'invoice_number'

    invoice_number = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    case = Relationship('Case')
    bill_to = Relationship('Contact')
    total = Attribute(field_type=enums.FieldTypes.CURRENCY)
    balance_due = Attribute(field_type=enums.FieldTypes.CURRENCY)
    status = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    """Theses fields should be relational to the case and displayed on the invoice template"""
    adjustments = Attribute(field_type=enums.FieldTypes.OBJECT)


@model_type
class Lead:
    _title = 'case_name'

    """We need Kanban style report for leads - I've separated the
  fields below based on a 'card view' and 'detail view' on kanban"""
    """Card View"""
    case_name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    retainer = Attribute(field_type=enums.FieldTypes.CURRENCY)
    """Detail View"""
    lead_status = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    intake_staff = Relationship('Staff', with_many=True)
    lead_source = Relationship('LeadSource')
    referred_by = Relationship('Contact', with_many=True)
    fee_type = Relationship('FeeType')
    trial_included = Attribute(field_type=enums.FieldTypes.BOOLEAN)
    retainer_hour_limit = Attribute(field_type=enums.FieldTypes.DECIMAL)
    investigator_budget = Attribute(field_type=enums.FieldTypes.CURRENCY)
    record_seal_expungement_included = Attribute(field_type=enums.FieldTypes.BOOLEAN)
    practice_area = Relationship('PracticeArea')
    case_stage = Relationship('CaseStage')
    cause_of_action = Relationship('CauseOfAction', with_many=True)
    statute_of_limitations = Attribute(field_type=enums.FieldTypes.DATE)
    court = Relationship('Entity')
    department = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    case_number = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    incident_date = Attribute(field_type=enums.FieldTypes.DATE)
    incident_location = Attribute(field_type=enums.FieldTypes.ADDRESS)
    case_description = Attribute(field_type=enums.FieldTypes.MULTI_LINE)
    contacts = Relationship('Contact', with_many=True)
    # client_details = ... need to discuss


@model_type
class LeadActivity:
    _title = 'activity'

    lead = Relationship('Lead')
    activity = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    due_time = Attribute(field_type=enums.FieldTypes.DATETIME)
    status = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)


@model_type
class LeadSource:
    _title = 'name'
    name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)


@model_type
class Ledger:
    _title = 'transaction_time'
    transaction_time = Attribute(field_type=enums.FieldTypes.DATETIME)


@model_type
class Payment:
    _title = 'amount'

    case = Relationship('Case')
    invoice = Relationship('Invoice')
    bank_account = Relationship('BankAccount')
    amount = Attribute(field_type=enums.FieldTypes.CURRENCY)
    payment_method = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    payment_time = Attribute(field_type=enums.FieldTypes.DATETIME)
    status = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)


@model_type
class PracticeArea:
    _title = 'name'
    name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)


@model_type
class Staff:
    _title = 'full_name'

    branch = Relationship('Branch')
    first_name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    last_name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    staff_group = Relationship('StaffGroup')
    pay_type = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    pay_rate = Attribute(field_type=enums.FieldTypes.CURRENCY)
    work_phone = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    extension = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    mileage_reimbursement = Attribute(field_type=enums.FieldTypes.CURRENCY)
    hire_date = Attribute(field_type=enums.FieldTypes.DATE)
    leave_date = Attribute(field_type=enums.FieldTypes.DATE)
    """Detail View"""
    user_name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    work_email = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    enable_overtime = Attribute(field_type=enums.FieldTypes.BOOLEAN)
    overtime_rate = Attribute(field_type=enums.FieldTypes.CURRENCY)
    weekly_base_hours = Attribute(field_type=enums.FieldTypes.DECIMAL)
    enable_break_time_deduction = Attribute(field_type=enums.FieldTypes.BOOLEAN)
    break_time_hour_base = Attribute(field_type=enums.FieldTypes.DECIMAL)
    break_time_rate = Attribute(field_type=enums.FieldTypes.DECIMAL)
    enable_performance_incentives = Attribute(field_type=enums.FieldTypes.BOOLEAN)
    intake_performance_incentive = Attribute(field_type=enums.FieldTypes.DECIMAL)
    override_incentive = Attribute(field_type=enums.FieldTypes.DECIMAL)
    manager_incentive = Attribute(field_type=enums.FieldTypes.DECIMAL)
    referral_incentive = Attribute(field_type=enums.FieldTypes.DECIMAL)
    employment_status = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    manager = Relationship('Staff')
    bar_number = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    bar_state = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    bar_admission = Attribute(field_type=enums.FieldTypes.DATE)
    date_of_birth = Attribute(field_type=enums.FieldTypes.DATE)
    personal_phone = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    personal_email = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    personal_address = Attribute(field_type=enums.FieldTypes.MULTI_LINE)
    personal_ssn = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    personal_gender = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    personal_race = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    bank_name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    bank_routing_number = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    bank_account_number = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    emergency_contact_name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    emergency_contact_phone = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    emergency_contact_email = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    emergency_contact_address = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)

    @staticmethod
    def get_full_name(args):
        return f"{args['first_name']} {args['last_name']}"

    full_name = Computed(('first_name', 'last_name'), 'get_full_name')


@model_type
class StaffGroup:
    _title = 'name'
    name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)


@model_type
class StaffPayType:
    _title = 'name'
    name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)


@model_type
class Task:
    _title = 'activity'

    case = Relationship('Case')
    activity = Relationship('Activity')
    due_date = Attribute(field_type=enums.FieldTypes.DATE)
    priority = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    assigned_staff = Relationship('Staff', with_many=True)
    notes = Attribute(field_type=enums.FieldTypes.MULTI_LINE)
    """Detail View"""
    documents = Attribute(field_type=enums.FieldTypes.FILE_UPLOAD)


@model_type
class TimeEntry:
    _title = 'activity'

    date = Attribute(field_type=enums.FieldTypes.DATE)
    activity = Relationship('Activity')
    duration = Attribute(field_type=enums.FieldTypes.DECIMAL)
    description = Attribute(field_type=enums.FieldTypes.MULTI_LINE)
    rate = Attribute(field_type=enums.FieldTypes.CURRENCY)
    total = Attribute(field_type=enums.FieldTypes.CURRENCY)
    staff = Relationship('Staff')
    case = Relationship('Case')
    invoice = Relationship('Invoice')
    """Detail View"""
    billable = Attribute(field_type=enums.FieldTypes.BOOLEAN)
    rate_type = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
    status = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)


@model_type
class Timesheet:
    _title = 'staff'

    staff = Relationship('Staff')
    clock_in_time = Attribute(field_type=enums.FieldTypes.DATETIME)
    clock_out_time = Attribute(field_type=enums.FieldTypes.DATETIME)
    hours_worked = Attribute(field_type=enums.FieldTypes.CURRENCY)
    earned_pay = Attribute(field_type=enums.FieldTypes.CURRENCY)
    approved = Attribute(field_type=enums.FieldTypes.BOOLEAN)
    """Detail View"""
    approved_by = Relationship('Staff')
    """Need to add Payroll class at some point"""
    # payroll_record = Relationship('Payroll')


@model_type
class TypeOfAction:
    _title = 'name'
    name = Attribute(field_type=enums.FieldTypes.SINGLE_LINE)
