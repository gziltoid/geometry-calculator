from abc import ABC, abstractmethod
from math import pi


class Shape(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def area(self):
        pass


class Flat(Shape):
    @abstractmethod
    def perimeter(self):
        pass


class Solid(Shape):
    @abstractmethod
    def volume(self):
        pass


# Flat shapes

class Circle(Flat):
    __name = 'Circle'

    def __init__(self, radius):
        self.radius = radius

    @property
    def name(self):
        return self.__name

    def area(self):
        return self.radius ** 2 * pi

    def perimeter(self):
        return 2 * pi * self.radius


class Square(Flat):
    __name = 'Square'

    def __init__(self, a):
        self.a = a

    @property
    def name(self):
        return self.__name

    def area(self):
        return self.a ** 2

    def perimeter(self):
        return 4 * self.a


class Rectangle(Flat):
    __name = 'Rectangle'

    def __init__(self, a, b):
        self.a = a
        self.b = b

    @property
    def name(self):
        return self.__name

    def area(self):
        return self.a * self.b

    def perimeter(self):
        return 2 * (self.a + self.b)


class Triangle(Flat):
    __name = 'Triangle'

    # TODO base height
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    @property
    def name(self):
        return self.__name

    def area(self):
        '''Heron's formula'''
        p = 0.5 * self.perimeter()
        return (p * (p - self.a) * (p - self.b) * (p - self.c)) ** 0.5

    def perimeter(self):
        return self.a + self.b + self.c


class Trapezoid(Flat):
    __name = 'Trapezoid'

    # TODO c, d
    def __init__(self, a, b, height):
        '''a, b - bases'''
        self.a = a
        self.b = b
        self.height = height

    @property
    def name(self):
        return self.__name

    def area(self):
        return 0.5 * (self.a + self.b) * self.height

    def perimeter(self):
        # P = a + b + c + d
        pass


class Rhombus(Flat):
    __name = 'Rhombus'

    def __init__(self, a, h):
        self.a = a
        self.height = h

    @property
    def name(self):
        return self.__name

    def area(self):
        return self.a * self.height

    def perimeter(self):
        return 4 * self.a


# Solid shapes

class Sphere(Solid):
    __name = 'Sphere'

    def __init__(self, radius):
        self.radius = radius

    @property
    def name(self):
        return self.__name

    def area(self):
        return self.radius ** 2 * 4 * pi

    def volume(self):
        return self.radius ** 3 * pi * 4/3


class Cube(Solid):
    __name = 'Cube'

    def __init__(self, a):
        self.a = a

    @property
    def name(self):
        return self.__name

    def area(self):
        return self.a ** 2 * 6

    def volume(self):
        return self.a ** 3


class Cuboid(Solid):
    __name = 'Cuboid'

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    @property
    def name(self):
        return self.__name

    def area(self):
        return 2 * (self.a * self.b + self.b * self.c + self.a * self.c)

    def volume(self):
        return self.a * self.b * self.c


class Pyramid(Solid):
    '''Square Pyramid'''
    __name = 'Pyramid'

    def __init__(self, a, h):
        '''h: height
        a: side length'''
        self.a = a
        self.height = h

    @property
    def name(self):
        return self.__name

    def area(self):
        return self.a * (self.a + (self.a ** 2 + self.height ** 2 * 4) ** 0.5)

    def volume(self):
        return self.a ** 2 * self.height * 1/3


class Cylinder(Solid):
    __name = 'Cylinder'

    def __init__(self, radius, h):
        self.radius = radius
        self.height = h

    @property
    def name(self):
        return self.__name

    def area(self):
        return 2 * pi * self.radius * (self.height + self.radius)

    def volume(self):
        return self.radius ** 2 * pi * self.height


class Cone(Solid):
    __name = 'Cone'

    def __init__(self, radius, h):
        self.radius = radius
        self.height = h

    @property
    def name(self):
        return self.__name

    def area(self):
        return pi * self.radius * (self.radius + (self.radius ** 2 + self.height ** 2) ** 0.5)

    def volume(self):
        return self.radius ** 2 * pi * self.height * 1/3
