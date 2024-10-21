import pickle_functions as pf

# Сериализация и десериализация итератора
serialized_iterator = pf.serialize_iterator()
deserialized_iterator = pf.deserialize_iterator(serialized_iterator)
print("Десериализованный итератор:", deserialized_iterator)

# Сериализация и десериализация встроенной функции
serialized_builtin_function = pf.serialize_builtin_function()
pf.deserialize_builtin_function(serialized_builtin_function)

# Сериализация и десериализация класса из библиотеки
serialized_library_class = pf.serialize_library_class()
deserialized_library_class = pf.deserialize_library_class(serialized_library_class)
print("Десериализованный класс deque:", deserialized_library_class)

# Сериализация и десериализация самописного класса
serialized_custom_class = pf.serialize_custom_class()
pf.deserialize_custom_class(serialized_custom_class)