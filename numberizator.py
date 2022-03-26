from numbers import Integral


def add_parent(cls, parent):
    namespace = {"cls": cls, "parent": parent}
    exec(f"class {cls.__name__}(cls, parent): pass", namespace)
    return namespace[cls.__name__]


def add_method(cls, name, body):
    namespace = {"cls": cls, "name": name, "body": body}
    exec(f"class {cls.__name__}(cls): {name} = body", namespace)
    return namespace[cls.__name__]


def numberizate(original):
    assert "__int__" in original.__dict__
    cls = add_parent(original, Integral)
    for method in (
        "rpow rrshift add and floordiv invert mod mul neg pos".split()
        + "lshift pow radd rand rfloordiv rlshift rmod rmul rshift".split()
        + "truediv rtruediv xor rxor or ror eq le lt".split()
    ):
        method = f"__{method}__"
        if method not in original.__dict__:
            cls = add_method(cls, method, lambda *args: NotImplemented)
    for method in "trunc ceil floor round".split():
        method = f"__{method}__"
        if method not in original.__dict__:
            cls = add_method(cls, method, lambda x: int(x))
    if "__abs__" not in original.__dict__:
        cls = add_method(cls, "__abs__", lambda x: abs(int(x)))
    return cls
