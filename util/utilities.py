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
    data_found = False
    if isinstance(expected_data, list):
        for exp_data in expected_data:
            data_found = False
            if isinstance(actual_data, list):
                for act_data in actual_data:
                    if json_compare(act_data, exp_data):
                        data_found = True
                        break
            elif json_compare(actual_data, exp_data):
                data_found = True
                break
    elif isinstance(actual_data, list):
        for act_data in actual_data:
            if json_compare(act_data, expected_data):
                data_found = True
                break
    elif json_compare(actual_data, expected_data):
        data_found = True
    else:
        data_found = False
    assert data_found is True, "Data is not found in response"


def json_compare(actual_json, expected_json):
    matched = True
    for key in actual_json.keys():
        if key in expected_json.keys():
            if isinstance(actual_json[key], dict):
                json_compare(actual_json[key], expected_json[key])
            elif isinstance(actual_json[key], list):
                if not isinstance(expected_json[key], list):
                    matched = False
                else:
                    for act_data in actual_json[key]:
                        for exp_data in expected_json[key]:
                            if isinstance(act_data, dict):
                                if json_compare(act_data, exp_data):
                                    break
                            elif act_data != exp_data and exp_data != "XXX":
                                matched = False
            elif expected_json[key] != "XXX":
                if actual_json[key] != expected_json[key]:
                    matched = False
        else:
            print("New key found :", key)
    if matched is not True:
        return False
    else:
        return True
