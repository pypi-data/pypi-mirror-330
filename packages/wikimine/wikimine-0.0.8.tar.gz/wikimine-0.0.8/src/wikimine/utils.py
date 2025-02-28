def is_empty(value):
    if value is None:
        return True
    if not value:
        return True
    if value == '':
        return True

    return False


def list_static_class_members(clz):
    return {(k, v) for k, v in vars(clz).items() if not callable(v) and not k.startswith("__")}
