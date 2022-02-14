from abc import ABC, abstractmethod
from math import pi, sin


class Shape(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def area(self):
        pass


class Flat(Shape):
    @property
    @abstractmethod
    def perimeter(self):
        pass


class Solid(Shape):
    @property
    @abstractmethod
    def volume(self):
        pass


'''Flat shapes'''


class Circle(Flat):

    def __init__(self, radius):
        self.radius = radius

    @property
    def name(self):
        return 'Circle'

    @property
    def area(self):
        return self.radius ** 2 * pi

    @property
    def perimeter(self):
        return 2 * pi * self.radius


class Square(Flat):

    def __init__(self, a):
        self.a = a

    @property
    def name(self):
        return 'Square'

    @property
    def area(self):
        return self.a ** 2

    @property
    def perimeter(self):
        return 4 * self.a


class Rectangle(Flat):

    def __init__(self, a, b):
        self.a = a
        self.b = b

    @property
    def name(self):
        return 'Rectangle'

    @property
    def area(self):
        return self.a * self.b

    @property
    def perimeter(self):
        return 2 * (self.a + self.b)


class Triangle(Flat):

    def __init__(self, a, b, c):
        (a, b, c) = sorted((a, b, c))
        if a + b <= c:
            raise ValueError("Invalid triangle size")
        self.a = a
        self.b = b
        self.c = c

    @property
    def name(self):
        return 'Triangle'

    @property
    def area(self):
        '''Heron's formula'''
        p = 0.5 * self.perimeter
        return (p * (p - self.a) * (p - self.b) * (p - self.c)) ** 0.5

    @property
    def perimeter(self):
        return self.a + self.b + self.c

    @staticmethod
    def __calculate_median(a, b, c):
        return 0.5 * (2 * a ** 2 + 2 * b ** 2 - c ** 2) ** 0.5

    def get_median(self, side_number):
        params = {1: (self.b, self.c, self.a), 2: (
            self.a, self.c, self.b), 3: (self.a, self.b, self.c)}
        if side_number not in params.keys():
            raise ValueError('Invalid side')
        return Triangle.__calculate_median(*params.get(side_number))


class Trapezoid(Flat):

    def __init__(self, a, b, height):
        '''a, b - bases'''
        self.a = a
        self.b = b
        self.height = height

    @property
    def name(self):
        return 'Trapezoid'

    @property
    def area(self):
        return 0.5 * (self.a + self.b) * self.height

    @property
    def perimeter(self):
        side = self.height ** 2 + (abs(self.a - self.b) / 2) ** 2
        return self.a + self.b + 2 * side


class Rhombus(Flat):

    def __init__(self, a, h):
        self.a = a
        self.height = h

    @classmethod
    def from_side_and_angle(cls, side, angle):
        height = side * sin(angle * pi / 180)
        return cls(a=side, h=height)

    @property
    def name(self):
        return 'Rhombus'

    @property
    def area(self):
        return self.a * self.height

    @property
    def perimeter(self):
        return 4 * self.a


'''Solid shapes'''


class Sphere(Solid):

    def __init__(self, radius):
        self.radius = radius

    @property
    def name(self):
        return 'Sphere'

    @property
    def area(self):
        return self.radius ** 2 * 4 * pi

    @property
    def volume(self):
        return self.radius ** 3 * pi * 4/3


class Cube(Solid):

    def __init__(self, a):
        self.a = a

    @property
    def name(self):
        return 'Cube'

    @property
    def area(self):
        return self.a ** 2 * 6

    @property
    def volume(self):
        return self.a ** 3


class Cuboid(Solid):

    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height

    @property
    def name(self):
        return 'Cuboid'

    @property
    def area(self):
        return 2 * (self.width * self.length + self.length * self.height + self.width * self.height)

    @property
    def volume(self):
        return self.width * self.length * self.height


class Pyramid(Solid):
    '''Square Pyramid'''

    def __init__(self, a, h):
        '''a - base edge, h - height'''
        self.a = a
        self.height = h

    @property
    def name(self):
        return 'Pyramid'

    @property
    def area(self):
        return self.a * (self.a + (self.a ** 2 + self.height ** 2 * 4) ** 0.5)

    @property
    def volume(self):
        return self.a ** 2 * self.height * 1/3


class Cylinder(Solid):

    def __init__(self, radius, h):
        self.radius = radius
        self.height = h

    @property
    def name(self):
        return 'Cylinder'

    @property
    def area(self):
        return 2 * pi * self.radius * (self.height + self.radius)

    @property
    def volume(self):
        return self.radius ** 2 * pi * self.height


class Cone(Solid):

    def __init__(self, radius, h):
        self.radius = radius
        self.height = h

    @property
    def name(self):
        return 'Cone'

    @property
    def area(self):
        return pi * self.radius * (self.radius + (self.radius ** 2 + self.height ** 2) ** 0.5)

    @property
    def volume(self):
        return self.radius ** 2 * pi * self.height * 1/3
