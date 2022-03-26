def add_parent(cls, parent):
    namespace = {"cls": cls, "parent": parent}
    exec(f"class {cls.__name__}(cls, parent): pass", namespace)
    return namespace[cls.__name__]


def add_method(cls, name, body):
    namespace = {"cls": cls, "name": name, "body": body}
    exec(f"class {cls.__name__}(cls): {name} = body", namespace)
    return namespace[cls.__name__]
