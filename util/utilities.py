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
        validate(instance=actual_data, schema=schema)


def validate_response_data(actual_data, expected_data):
    data_found = []
    if isinstance(expected_data, list):
        for exp_data in expected_data:
            if isinstance(actual_data, list):
                data_found.append(act_data_compare(actual_data, exp_data))
            elif json_compare(actual_data, exp_data):
                data_found.append(True)
                break
    elif isinstance(actual_data, list):
        data_found.append(act_data_compare(actual_data, expected_data))
    elif json_compare(actual_data, expected_data):
        data_found.append(True)
    else:
        data_found.append(True)
    for i in range(len(data_found)):
        if data_found[i] is False:
            assert False, str(i) + "th data is not found in response"


def act_data_compare(actual_data, expected_data):
    data_found = False
    for act_data in actual_data:
        if json_compare(act_data, expected_data):
            data_found = True
            break
    return data_found


def json_compare(actual_json, expected_json):
    for key in expected_json.keys():
        if key in actual_json.keys():
            if isinstance(actual_json[key], dict):
                json_compare(actual_json[key], expected_json[key])
            else:
                if isinstance(actual_json[key], list):
                    if not isinstance(expected_json[key], list):
                        return False
                    else:
                        for exp_data in expected_json[key]:
                            matched = True
                            for act_data in actual_json[key]:
                                if isinstance(exp_data, dict):
                                    if json_compare(act_data, exp_data):
                                        matched = True
                                        break
                                    else:
                                        matched = False
                                else:
                                    if act_data != exp_data:
                                        return False
                            if matched is False:
                                return False
                elif actual_json[key] != expected_json[key]:
                    return False
        else:
            print("Key not found in actual data:", key)
            return False
    return True
