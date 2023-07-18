import anvil.server
# Global application constants, named strings, enumerations

# Use session
pm_logged_user = None


# Application id
APP_NAME = 'practiceMANAGER_SF'
APP_PREFIX = 'pm'


# model types
SYSTEM_MODEL = 'system'
DATA_MODEL = 'data'

# field type names
UID_FIELD = 'uid'
SINGLE_LINE_FIELD = 'single_line'
MULTI_LINE_FIELD = 'multi_line'
NUMBER_FIELD = 'number'
DECIMAL_FIELD = 'decimal'
CURRENCY_FIELD = 'currency'
DATE_FIELD = 'date'
DATETIME_FIELD = 'datetime'
TIME_FIELD = 'time'
BOOLEAN_FIELD = 'checkbox'
EMAIL_FIELD = 'email'
ADDRESS_FIELD = 'address'
HYPERLINK_FIELD = 'hyperlink'
SIGNATURE_FIELD = 'signature'
OBJECT_FIELD = 'object'
MEDIA_FIELD = 'media'
UPLOAD_FIELD = 'file_upload'
ENUM_SINGLE_FIELD = 'enum_single'
ENUM_MULTI_FIELD = 'enum_multi'

# filed type model to grid map
FIELD_TO_GRID = {
  UID_FIELD: 'string',
  SINGLE_LINE_FIELD: 'string',
  MULTI_LINE_FIELD: 'string',
  NUMBER_FIELD: 'number',
  DECIMAL_FIELD: 'number',
  CURRENCY_FIELD: 'number',
  DATE_FIELD: 'date',
  DATETIME_FIELD: 'datetime',
  TIME_FIELD: 'datetime',
  BOOLEAN_FIELD: 'boolean',
  EMAIL_FIELD: 'string',
  ADDRESS_FIELD: 'string',
  HYPERLINK_FIELD: 'string',
  SIGNATURE_FIELD: 'string',
  OBJECT_FIELD: 'string',
  MEDIA_FIELD: 'string',
  UPLOAD_FIELD: 'string',
  ENUM_SINGLE_FIELD: 'string',
  ENUM_MULTI_FIELD: 'string',
}

# field type to form input map
FIELD_TO_INPUT = {
  UID_FIELD: 'TextInput',
  SINGLE_LINE_FIELD: 'TextInput',
  MULTI_LINE_FIELD: 'MultiLineInput',
  NUMBER_FIELD: 'NumberInput',
  DECIMAL_FIELD: 'NumberInput',
  CURRENCY_FIELD: 'NumberInput',
  DATE_FIELD: 'DateInput',
  DATETIME_FIELD: 'DateTimeInput',
  TIME_FIELD: 'TimeInput',
  BOOLEAN_FIELD: 'CheckboxInput',
  EMAIL_FIELD: 'TextInput',
  ADDRESS_FIELD: 'MultiLineInput',
  HYPERLINK_FIELD: 'MultiLineInput',
  SIGNATURE_FIELD: 'SignatureInput',
  OBJECT_FIELD: 'MultiLineInput',
  MEDIA_FIELD: 'FileUploadInput',
  UPLOAD_FIELD: 'FileUploadInput',
  ENUM_SINGLE_FIELD: 'DropdownInput',
  ENUM_MULTI_FIELD: 'DropdownInput',
}

# field type grid to edit map
GRID_EDIT_TYPE = {
  'none': 'defaultEdit',
  'string': 'defaultEdit',
  'number': 'numericEdit',
  'boolean': 'booleanEdit',
  'dropdown': 'dropDownEdit',
  'date': 'datePickerEdit',
  'time': 'timePickerEdit',
  'datetime': 'dateTimePickerEdit',
}
