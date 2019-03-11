# 1) Create a Food class with a “name” and a “kind” attribute as well as a “describe()” method (which prints “name” and “kind” in a sentence).
class Food:
    def __init__(self, name, kind):
        self.name = name
        self.kind = kind

    def describe(self):
        print('The food is {} and it\'s {}'.format(self.name, self.kind))
    @staticmethod
    def describeStatic(name, kind):
        print('The food is {} and it\'s {}'.format(name, kind))
    
    def __repr__(self):
        return 'The food is {} and it\'s {}'.format(self.name, self.kind)

# 2) Try turning describe() from an instance method into a class and a static method. Change it back to an instance method thereafter.
food = Food('fasolada', 'Ospria')
food.describe()
Food.describeStatic('Fakes', 'Ospria')


# 3) Create a  “Meat” and a “Fruit” class – both should inherit from “Food”. Add a “cook()” method to “Meat” and “clean()” to “Fruit”.
class Meat(Food):
    def __init__(self, name):
        super().__init__(name, 'Meat')

    def cook(self):
        print('the food {} is cooked now!'.format(self.name))

class Fruit(Food):
    def __init__(self, name):
        super().__init__(name, 'Fruit')

    def clean(self):
        print('the fruit {} is clean now!'.format(self.name))

meat = Meat('giouvetsi')
meat.describe()
meat.cook()
fruit = Fruit('apples')
fruit.describe()
fruit.clean()

# 4) Overwrite a “dunder” method to be able to print your “Food” class.

print(meat)
print(fruit)