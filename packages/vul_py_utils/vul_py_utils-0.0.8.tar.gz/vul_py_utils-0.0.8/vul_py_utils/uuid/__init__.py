import uuid


def generate_uuid(*args, **kwargs)->str:
    """ Generate uuid with args and kwargs

    Returns:
        str: uuid with args and kwargs
    """
    id = str(uuid.uuid4())
    for arg in args:
        id += "_" + str(arg)
    for kwarg in kwargs:
        id += "_" + str(kwarg)
    return id