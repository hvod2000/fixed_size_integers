def add_method(cls, name, body):
    namespace = {"cls": cls, "name": name, "body": body}
    exec(f"class {cls.__name__}(cls): {name} = body", namespace)
    return namespace[cls.__name__]
