

def compare_dicts(dict1, dict2):
    """
    Compares two dictionaries. Returns True if they hold the same
    keys and the same values, returns False otherwise.
    """
    if not isinstance(dict1, dict) or not isinstance(dict2, dict):
        return False
    key_set_1 = set(dict1.keys())
    key_set_2 = set(dict2.keys())
    same_keys = key_set_1 & key_set_2
    if len(same_keys) == len(key_set_1) and len(same_keys) == len(key_set_2):
        for k in same_keys:
            if dict1[k] != dict2[k]:
                return False
        return True
    else:
        return False
