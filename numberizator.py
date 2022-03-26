from numbers import Integral, Number


def add_parent(cls, parent):
    namespace = {"cls": cls, "parent": parent}
    exec(f"class {cls.__name__}(cls, parent): pass", namespace)
    return namespace[cls.__name__]


def add_method(cls, name, body):
    namespace = {"cls": cls, "name": name, "body": body}
    exec(f"class {cls.__name__}(cls): {name} = body", namespace)
    return namespace[cls.__name__]


def implement_binary_op(binary_operation):
    namespace, definition = {"Number": Number}, (
        f"""def {binary_operation}(self, other):
    if isinstance(other, Number):
        return int(self).{binary_operation}(other)
    return NotImplemented"""
    )
    exec(definition, namespace)
    return namespace[binary_operation]


def implement_unary_op(op):
    namespace, definition = {}, f"def {op}(self):\n    return int(self).{op}()"
    exec(definition, namespace)
    return namespace[op]


def implement_mutation(op, gen_setter):
    namespace, mutation = {}, gen_setter(f"int(self).__{op}__(other)")
    definition = f"""def __i{op}__(self, other):
    {mutation}
    return self"""
    exec(definition, namespace)
    return namespace[f"__i{op}__"]


def has_method(cls, method):
    for cls in cls.mro():
        if cls is object:
            continue
        if method in cls.__dict__:
            return True
    return False


binary_operations = list(
    sorted(
        "add radd sub rsub mul rmul truediv rtruediv floordiv rfloordiv".split()
        + "and rand mod rmod lshift rlshift pow rpow rshift rrshift".split()
        + "or ror xor rxor eq rer le rle lt rlt".split()
    )
)

unary_operations = list(
    sorted("invert neg trunc ceil floor round pos abs".split())
)


def numberizate(cls=None, assignment=None):
    if cls is None:
        return lambda cls: numberizate(cls, assignment)
    assert "__int__" in cls.__dict__
    for method in (f"__{op}__" for op in binary_operations):
        if not has_method(cls, method):
            print("add", method)
            cls = add_method(cls, method, implement_binary_op(method))
        else:
            print("DUPLICATE", method)
    for method in (f"__{op}__" for op in unary_operations):
        if not has_method(cls, method):
            print("add", method)
            cls = add_method(cls, method, implement_unary_op(method))
        else:
            print("DUPLICATE", method)
    if assignment is None:
        return add_parent(cls, Integral)
    for method in binary_operations:
        if not has_method(cls, f"__i{method}__"):
            print("add", f"__i{method}__")
            mutation = implement_mutation(method, assignment)
            cls = add_method(cls, f"__i{method}__", mutation)
        else:
            print("DUPLICATE", f"__i{method}__")
    return add_parent(cls, Integral)
