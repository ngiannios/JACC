import vehicle

class Car(vehicle.Vehicle):
    # top_speed = 100
    # warnings = []
    def brag(self):
        print('Look how cool it is!!')


car1 = Car()
car1.drive()
car1.add_warning('New warning')
car1.top_speed=200
print(car1.__dict__)
print(car1.__dict__)
print(car1)
car2 = Car(120)
car2.drive()
print(car2.get_warnings())
car3=Car(150) 
car3.drive() 
print(car3.get_warnings())
