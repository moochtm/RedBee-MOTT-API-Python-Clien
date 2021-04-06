
def filter_nested_dict(value, default, path):
    keys = path.split('.')
    for key in keys:
        try:
            value = value[key]
        except KeyError:
            return default
    return value
