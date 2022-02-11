#!/usr/bin/env python3
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

    def __init__(self, side):
        self.side = side

    @property
    def name(self):
        return self.__name

    def area(self):
        return self.side ** 2

    def perimeter(self):
        return 4 * self.side


class Rectangle(Flat):
    pass


class Triangle(Flat):
    pass


class Trapezoid(Flat):
    pass


class Rhombus(Flat):
    pass


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
    pass


class Cuboid(Solid):
    pass


class Pyramid(Solid):
    pass


class Cylinder(Solid):
    pass


class Cone(Solid):
    pass
