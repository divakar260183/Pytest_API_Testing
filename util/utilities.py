
def get_value_for_key(data_list, key_value):
    value = None
    if isinstance(data_list, list):
        for items in data_list:
            for key in items:
                if key == key_value:
                    value = items[key]
    return value
