from jsonschema import validate
from jsonschema.exceptions import ValidateError
from json import loads, dumps
from Data import Data
from Items import Items


class InvalidSchemaError(Exception):
    """ Raised if schema is not valid. """


# todo: add required in schema
# todo: write docummentation and comments

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


outter_keys_valid = ["kind", "etag", "nextPageToken", "regionCode", "pageInfo"]


def sent_data_values(data: dict) -> object:
    values_data = []
    keys = list(data.keys())
    for key in outter_keys_valid:
        if key not in keys:
            raise KeyError(f"'{key}' is not in data.")
        else:
            values_data.append(data[key])
    return Data(*values_data)


item_keys_valid = ["kind", "etag", "id"]


def sent_items_values(data: dict) -> object:
    try:
        items = data["items"]
    except KeyError:
        raise KeyError(f"'items' is not in data.") from None
    else:
        data_items = []
        for item in items:
            item_keys = list(item.keys())
            for key in item_keys_valid:
                if key not in item_keys:
                    raise KeyError(f"'{key}' is not in data.")
                else:
                    data_items.append(item[key])
        return Items(*data_items)
