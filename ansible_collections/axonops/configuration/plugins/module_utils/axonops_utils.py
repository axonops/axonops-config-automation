from ansible.module_utils.basic import env_fallback


def make_module_args(module_args: dict) -> dict:
    return {**base_module_args(), **module_args}


def base_module_args() -> dict:
    return {
        "base_url": {"type": 'str', "required": False, "fallback": (env_fallback, ['AXONOPS_URL'])},
        "org": {"type": 'str', "required": True, "fallback": (env_fallback, ['AXONOPS_ORG'])},
        "cluster": {"type": 'str', "required": False, "fallback": (env_fallback, ['AXONOPS_CLUSTER'])},
        "auth_token": {"type": 'str', "required": False, "fallback": (env_fallback, ['AXONOPS_TOKEN'])},
        "username": {"type": 'str', "required": False, "fallback": (env_fallback, ['AXONOPS_USERNAME'])},
        "password": {"type": 'str', "required": False, "fallback": (env_fallback, ['AXONOPS_PASSWORD'])},
        "cluster_type": {"type": 'str', "required": False, "fallback": (env_fallback, ['AXONOPS_CLUSTER_TYPE']),
                         'default': 'cassandra'},

    }


def dicts_are_different(a: dict, b: dict) -> bool:
    """
    Check if the dictionaries a and b are different
    """
    # check the keys
    if set(a.keys()) != set(b.keys()):
        return True  # If keys are different, dictionaries are different

    # check the content of the keys
    for key_a, value_a in a.items():
        value_b = b.get(key_a)
        if value_a != value_b:
            return True  # If any value is different, dictionaries are different

    return False  # Dictionaries are identical


def find_by_field(dicts, field, value):
    """
    Find an item in a list of dicts by searching a particular field for a value
    """
    for d in dicts or []:
        if d.get(field) == value:
            return d
    return None


def string_to_bool(value):
    return value is not None and value.lower() in ('true', 't', '1', 'yes', 'y')


def bool_to_string(value):
    return 'true' if value else 'false'


def string_or_none(value):
    if value is None or value.lower() in ('none', 'null'):
        return None
    return value
