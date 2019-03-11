class Printable:
    def __repr__(self):
        return str(self.__dict__)
    
    def __str__(self):
        return str(self.__dict__.copy())

    def to_json(self):
        return self.__dict__.copy()