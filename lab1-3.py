class Animal:
    def __init__(self, name, age, view):
        self.name = name
        self.age = age
        self.view = view


class Zebra(Animal):
    def description(self):
        return f"Zebra's name is {self.name}, and she is {self.age} years old, she is {self.view}."


class Dolphin(Animal):
    def description(self):
        return f"Dolphin's name is {self.name}, and he is {self.age} лет, he is {self.view}."


zebra = Zebra("Zebr", "8", "Not Bober")
print(zebra.description())
dolphin = Dolphin("Dolph", "5", "Also Not Bobr")
print(dolphin.description())