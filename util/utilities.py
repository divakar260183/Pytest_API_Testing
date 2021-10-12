from genson import SchemaBuilder
from jsonschema import validate

testResults = []
not_matched_data = []


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
    print("data not matched" + str(not_matched_data))
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
                    not_matched_data.append(
                        {key: {'actual_value': actual_json[key], 'expected_value': expected_json[key]}})
                    return False
        else:
            print("Key not found in actual data:", key)
            return False
    return True


def match_data(expected_data, actual_data, count=0):
    if type(actual_data) != type(expected_data):
        print("The type of actual_data and expected_data doesn't match. The data doesn't match hence.")
        return False
    if isinstance(actual_data, list):  # it means expected_data is also list
        print("comparing list %s and %s" % (expected_data, actual_data))
        for expected_list_index, expected_data_item in enumerate(expected_data):
            subset_match_found = False
            for actual_list_index, actual_data_item in enumerate(actual_data):
                if match_data(expected_data_item, actual_data_item):
                    subset_match_found = True
                    break
            if not subset_match_found:
                print(
                    "The list %s doesn't match %s since expected_list item %s at index %d isn't the subset of any item in actual_list" % (
                        expected_data, actual_data, expected_data_item, expected_list_index))
                return False
        return True
    elif isinstance(expected_data, dict):
        for key in expected_data:
            if key not in actual_data:
                print("%s key from expected_data %s not found in actual_data %s" % (key, expected_data, actual_data))
                return False
            else:
                if match_data(expected_data[key], actual_data[key]) and count < len(expected_data):
                    count = count + 1
                    if count == len(expected_data):
                        return True
                    else:
                        continue
                return False
    else:
        if actual_data != expected_data:
            # print "%s != %s" %(actual_data, expected_data)
            return False
        return True
