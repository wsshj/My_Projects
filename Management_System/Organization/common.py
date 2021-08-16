

def has_none(values):
    for key,value in values.items():
        if value is None:
            return True

    return False