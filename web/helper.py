from jsonschema import validate
from jsonschema.exceptions import ValidateError
from json import loads, dumps


class InvalidSchemaError(Exception):
    """ Raised if schema is not valid. """


schema_errors = [
    "Failed validating 'type' in schema",
    "Failed validating 'required' in schema",
    "Failed validating 'minLength' in schema",
    "Failed validating 'maxLength' in schema",
    "Failed validating 'minimum' in schema",
    "Failed validating 'maximum' in schema",
    "Failed validating 'minItems' in schema",
    "Failed validating 'maxItems' in schema"
]

INVALID_SCHEMA = 451


def validate_schema(schema: dict, data: dict):
    """ Schemma validation.

    Args:
        schema (dict): valid dictionary
        data (dict): dictionary for validation

    Raises:
        InvalidSchemaError: if data (schema) is not valid
    """
    # data = dumps(data)
    try:
        validate(data, schema)
    except ValidationError as ex:
        ex_str = str(ex)
        for message in schema_errors:
            if message in ex_str:
                raise InvalidSchemaError(message, INVALID_SCHEMA)
