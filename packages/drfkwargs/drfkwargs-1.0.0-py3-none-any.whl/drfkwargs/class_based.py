from . import kwargs


class FieldKwargs:
    READ_ONLY = kwargs.READ_ONLY
    WRITE_ONLY = kwargs.WRITE_ONLY
    REQUIRED = kwargs.REQUIRED
    DEFAULT = kwargs.DEFAULT
    INITIAL = kwargs.INITIAL
    SOURCE = kwargs.SOURCE
    LABEL = kwargs.LABEL
    HELP_TEXT = kwargs.HELP_TEXT
    STYLE = kwargs.STYLE
    ERROR_MESSAGES = kwargs.ERROR_MESSAGES
    VALIDATORS = kwargs.VALIDATORS
    ALLOW_NULL = kwargs.ALLOW_NULL


class BooleanFieldKwargs(FieldKwargs):
    pass


class CharFieldKwargs(FieldKwargs):
    pass


class EmailFieldKwargs(CharFieldKwargs):
    pass


class RegexFieldKwargs(CharFieldKwargs):
    REGEX = kwargs.REGEX


class SlugFieldKwargs(CharFieldKwargs):
    ALLOW_UNICODE = kwargs.ALLOW_UNICODE


class URLFieldKwargs(CharFieldKwargs):
    pass


class UUIDFieldKwargs(FieldKwargs):
    pass


class IPAddressFieldKwargs(CharFieldKwargs):
    PROTOCOL = kwargs.PROTOCOL


class IntegerFieldKwargs(FieldKwargs):
    pass


class FloatFieldKwargs(FieldKwargs):
    pass


class DecimalFieldKwargs(FieldKwargs):
    MAX_DIGITS = kwargs.MAX_DIGITS
    DECIMAL_PLACES = kwargs.DECIMAL_PLACES
    COERCE_TO_STRING = kwargs.COERCE_TO_STRING
    MAX_VALUE = kwargs.MAX_VALUE
    MIN_VALUE = kwargs.MIN_VALUE
    LOCALIZE = kwargs.LOCALIZE
    ROUNDING = kwargs.ROUNDING
    NORMALIZE_OUTPUT = kwargs.NORMALIZE_OUTPUT


class DateTimeFieldKwargs(FieldKwargs):
    FORMAT = kwargs.FORMAT
    INPUT_FORMATS = kwargs.INPUT_FORMATS
    DEFAULT_TIMEZONE = kwargs.DEFAULT_TIMEZONE


class DateFieldKwargs(FieldKwargs):
    FORMAT = kwargs.FORMAT
    INPUT_FORMATS = kwargs.INPUT_FORMATS


class TimeFieldKwargs(FieldKwargs):
    FORMAT = kwargs.FORMAT
    INPUT_FORMATS = kwargs.INPUT_FORMATS


class DurationFieldKwargs(FieldKwargs):
    pass


class ChoiceFieldKwargs(FieldKwargs):
    CHOICES = kwargs.CHOICES


class MultipleChoiceFieldKwargs(ChoiceFieldKwargs):
    pass


class FilePathFieldKwargs(ChoiceFieldKwargs):
    PATH = kwargs.PATH
    MATCH = kwargs.MATCH
    RECURSIVE = kwargs.RECURSIVE
    ALLOW_FILES = kwargs.ALLOW_FILES
    ALLOW_FOLDERS = kwargs.ALLOW_FOLDERS


class FileFieldKwargs(FieldKwargs):
    pass


class ImageFieldKwargs(FileFieldKwargs):
    pass


class ListFieldKwargs(FieldKwargs):
    pass


class DictFieldKwargs(FieldKwargs):
    pass


class HStoreFieldKwargs(DictFieldKwargs):
    pass


class JSONFieldKwargs(FieldKwargs):
    pass


class ReadOnlyFieldKwargs(FieldKwargs):
    pass


class HiddenFieldKwargs(FieldKwargs):
    pass


class SerializerMethodFieldKwargs(FieldKwargs):
    METHOD_NAME = kwargs.METHOD_NAME


class ModelFieldKwargs(FieldKwargs):
    MODEL_FIELD = kwargs.MODEL_FIELD
