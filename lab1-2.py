class Mother:
    def __init__(self, name):
        self.__name = name

    def __str__(self):
        return  f"{self.__name}"


class Daughter(Mother):
    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    def __str__(self):
        return f"Daughter's name is {self.__name} and she is {self.__age} years old"


mother = Mother("Bobr")
daughter = Daughter("Bobrena", 10)

print("Mother's name is", mother)
print(daughter)
