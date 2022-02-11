#!/usr/bin/env python3
from abc import ABC, abstractmethod
from math import pi


class Shape(ABC):
    @abstractmethod
    def __init__(self, name):
        self._name = name

    @property
    @abstractmethod
    def name(self):
        pass

    @name.setter
    @abstractmethod
    def name(self, name):
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


# flat shapes

class Circle(Flat):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def area(self, radius):
        return radius ** 2 * pi

    def perimeter(self, radius):
        return 2 * pi * radius


class Square(Flat):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def area(self, side):
        return side ** 2

    def perimeter(self, side):
        return 4 * side


class Rectangle(Flat):
    pass


class Triangle(Flat):
    pass


class Trapezoid(Flat):
    pass


class Rhombus(Flat):
    pass


# solid shapes

class Sphere(Solid):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def area(self, radius):
        return radius ** 2 * 4 * pi

    def volume(self, radius):
        return radius ** 3 * pi * 4/3


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
