
MODEL_MODULE_NAME = 'practiceMANAGER_SF.orm_client.model'


# App model list for enumerations
ENUM_MODEL_LIST = {
    'Activity': {'model': 'Activity', 'name_field': 'name'},
    'BankAccount': {'model': 'BankAccount', 'name_field': 'account_type.name'},
    'BankAccountType': {'model': 'BankAccountType', 'name_field': 'name'},
    'Branch': {'model': 'Branch', 'name_field': 'name'},
    'CaseStage': {'model': 'CaseStage', 'name_field': 'name'},
    'CaseStatus': {'model': 'CaseStatus', 'name_field': 'name'},
    'CauseOfAction': {'model': 'CauseOfAction', 'name_field': 'cause_of_action'},
    'ContactGroup': {'model': 'ContactGroup', 'name_field': 'name'},
    'ContactRole': {'model': 'ContactRole', 'name_field': 'name'},
    'EntityType': {'model': 'EntityType', 'name_field': 'name'},
    'FeeType': {'model': 'FeeType', 'name_field': 'name'},
    'LeadSource': {'model': 'LeadSource', 'name_field': 'name'},
    'PracticeArea': {'model': 'PracticeArea', 'name_field': 'name'},
    'StaffGroup': {'model': 'StaffGroup', 'name_field': 'name'},
    'StaffPayType': {'model': 'StaffPayType', 'name_field': 'name'},
    'TypeOfAction': {'model': 'TypeOfAction', 'name_field': 'name'},
}
Models = {}
