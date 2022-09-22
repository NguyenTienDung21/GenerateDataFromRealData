

def transform_name(edge_id, name):
    new_name = f'_{edge_id}_{name}'
    invalid_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_'
    if type(new_name) is not str or len(new_name) < 1:
        return new_name
    for char in new_name:
        if char not in invalid_chars:
            new_name = new_name.replace(char, '_')
    return new_name
