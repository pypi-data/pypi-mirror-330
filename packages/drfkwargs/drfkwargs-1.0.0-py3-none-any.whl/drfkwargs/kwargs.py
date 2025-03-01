# Field (kwargs which are specified in __init__ for every field)
READ_ONLY = 'read_only'
WRITE_ONLY = 'write_only'
REQUIRED = 'required'
DEFAULT = 'default'
INITIAL = 'initial'
SOURCE = 'source'
LABEL = 'label'
HELP_TEXT = 'help_text'
STYLE = 'style'
ERROR_MESSAGES = 'error_messages'
VALIDATORS = 'validators'
ALLOW_NULL = 'allow_null'

# RegexField
REGEX = 'regex'

# SlugField
ALLOW_UNICODE = 'allow_unicode'

# IPAddressField
PROTOCOL = 'protocol'

# DecimalField
MAX_DIGITS = 'max_digits'
DECIMAL_PLACES = 'decimal_places'
COERCE_TO_STRING = 'coerce_to_string'
MAX_VALUE = 'max_value'
MIN_VALUE = 'min_value'
LOCALIZE = 'localize'
ROUNDING = 'rounding'
NORMALIZE_OUTPUT = 'normalize_output'

# DateTimeField
FORMAT = 'format'

# DateTimeField, DateField, TimeField
INPUT_FORMATS = 'input_formats'
DEFAULT_TIMEZONE = 'default_timezone'

# ChoiceField
CHOICES = 'choices'

# FilePathField
PATH = 'path'
MATCH = 'match'
RECURSIVE = 'recursive'
ALLOW_FILES = 'allow_files'
ALLOW_FOLDERS = 'allow_folders'

# SerializerMethodField
METHOD_NAME = 'method_name'

# ModelField
MODEL_FIELD = 'model_field'
