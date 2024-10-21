import pickle
from collections import deque


def serialize_iterator():
    iterator = iter([1, 2, 3])
    serialized = pickle.dumps(iterator)
    return serialized


def deserialize_iterator(serialized):
    deserialized = pickle.loads(serialized)
    return list(deserialized)


def serialize_builtin_function():
    serialized = pickle.dumps(print)
    return serialized


def deserialize_builtin_function(serialized):
    deserialized = pickle.loads(serialized)
    deserialized("Hello, World!")


def serialize_library_class():
    serialized = pickle.dumps(deque)
    return serialized


def deserialize_library_class(serialized):
    deserialized = pickle.loads(serialized)
    d = deserialized([1, 2, 3])
    return d


def serialize_custom_class():
    class MyClass:
        def __init__(self, value):
            self.value = value

        def display(self):
            print(self.value)

    obj = MyClass(42)
    serialized = pickle.dumps(obj)
    return serialized


def deserialize_custom_class(serialized):
    deserialized = pickle.loads(serialized)
    deserialized.display()