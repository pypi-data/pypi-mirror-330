def is_empty(value):
    if value is None:
        return True
    if not value:
        return True
    if value == '':
        return True

    return False

