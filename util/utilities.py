from genson import SchemaBuilder
from jsonschema import validate


def get_value_for_key(data_list, key_value):
    value = None
    if isinstance(data_list, list):
        for items in data_list:
            for key in items:
                if key == key_value:
                    value = items[key]
    return value


def validate_schema(actual_data, expected_data):
    builder = SchemaBuilder()
    if isinstance(expected_data, list):
        builder.add_object(expected_data[0])
        schema = builder.to_schema()
    else:
        builder.add_object(expected_data)
        schema = builder.to_schema()
    if isinstance(actual_data, list):
        for data in actual_data:
            validate(instance=data, schema=schema)
    else:
        validate(instance=expected_data, schema=schema)


def validate_response_data(actual_data, expected_data):
    if isinstance(expected_data, list):
        for exp_data in expected_data:
            for items in exp_data:
                if exp_data[items] != "XXX":
                    if isinstance(actual_data, list):
                        for data in actual_data:
                            if data[items] == exp_data[items]:
                                notmached = True
                            else:
                              notmached = False
                    else:
                        actual_data[items] = "XXX"
    else:
        for items in expected_data:
            if expected_data[items] == "XXX":
                if isinstance(actual_data, list):
                    for data in actual_data:
                        data[items] = "XXX"
                else:
                    actual_data[items] = "XXX"

        for exp_data in expected_data:
            for items in exp_data:
                if exp_data[items] == "XXX":
                    if isinstance(actual_data, list):
                        for data in actual_data:
                            data[items] = "XXX"
                    else:
                        actual_data[items] = "XXX"




