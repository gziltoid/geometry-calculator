from abc import ABC, abstractmethod
from math import pi, sin


class Shape(ABC):
    @abstractmethod
    def __init__(self, args):
        if any(arg <= 0 for arg in args):
            raise ValueError("Parameters should be positive.")

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def area(self):
        pass


class Flat(Shape):
    def __init__(self, *args):
        super().__init__(args)

    @property
    @abstractmethod
    def perimeter(self):
        pass


class Solid(Shape):
    def __init__(self, *args):
        super().__init__(args)

    @property
    @abstractmethod
    def volume(self):
        pass


"""Flat shapes"""


class Circle(Flat):
    def __init__(self, radius):
        super().__init__(radius)
        self.radius = radius

    @property
    def name(self):
        return "Circle"

    @property
    def area(self):
        return pi * self.radius**2

    @property
    def perimeter(self):
        return 2 * pi * self.radius


class Rectangle(Flat):
    def __init__(self, a, b):
        super().__init__(a, b)
        self.a = a
        self.b = b

    @property
    def name(self):
        return "Rectangle"

    @property
    def area(self):
        return self.a * self.b

    @property
    def perimeter(self):
        return 2 * (self.a + self.b)


class Square(Rectangle):
    def __init__(self, a):
        super().__init__(a, a)

    @property
    def name(self):
        return "Square"


class Triangle(Flat):
    def __init__(self, a, b, c):
        super().__init__(a, b, c)
        (a, b, c) = sorted((a, b, c))
        if a + b <= c:
            raise ValueError("Invalid triangle size.")
        self.a = a
        self.b = b
        self.c = c

    @property
    def name(self):
        return "Triangle"

    @property
    def area(self):
        """Heron's formula"""
        p = 0.5 * self.perimeter
        return (p * (p - self.a) * (p - self.b) * (p - self.c)) ** 0.5

    @property
    def perimeter(self):
        return self.a + self.b + self.c

    @staticmethod
    def __calculate_median(a, b, c):
        return 0.5 * (2 * a**2 + 2 * b**2 - c**2) ** 0.5

    def get_median(self, side_index=1):
        match side_index:
            case 1: return Triangle.__calculate_median(self.b, self.c, self.a)
            case 2: return Triangle.__calculate_median(self.a, self.c, self.b)
            case 3: return Triangle.__calculate_median(self.a, self.b, self.c)
            case _: raise ValueError("Invalid side index.")


class Trapezoid(Flat):
    def __init__(self, a, b, height):
        """a, b - bases"""
        super().__init__(a, b, height)
        if a == b:
            raise ValueError("Invalid trapezoid base.")
        self.a = a
        self.b = b
        self.height = height

    @property
    def name(self):
        return "Trapezoid"

    @property
    def area(self):
        return 0.5 * (self.a + self.b) * self.height

    @property
    def perimeter(self):
        side = self.height**2 + (abs(self.a - self.b) / 2) ** 2
        return self.a + self.b + 2 * side


class Rhombus(Flat):
    def __init__(self, a, height):
        super().__init__(a, height)
        if height > a:
            raise ValueError("Invalid rhombus size.")
        self.a = a
        self.height = height

    @classmethod
    def from_side_and_angle(cls, side, angle):
        if not 0 < angle <= 180:
            raise ValueError("Invalid rhombus angle.")
        height = side * sin(angle * pi / 180)
        return cls(a=side, height=height)

    @property
    def name(self):
        return "Rhombus"

    @property
    def area(self):
        return self.a * self.height

    @property
    def perimeter(self):
        return 4 * self.a


"""Solid shapes"""


class Sphere(Solid):
    def __init__(self, radius):
        super().__init__(radius)
        self.radius = radius

    @property
    def name(self):
        return "Sphere"

    @property
    def area(self):
        return 4 * pi * self.radius**2

    @property
    def volume(self):
        return 4 / 3 * pi * self.radius**3


class Cuboid(Solid):
    def __init__(self, length, width, height):
        super().__init__(length, width, height)
        self.length = length
        self.width = width
        self.height = height

    @property
    def name(self):
        return "Cuboid"

    @property
    def area(self):
        return 2 * (
            self.width * self.length
            + self.length * self.height
            + self.width * self.height
        )

    @property
    def volume(self):
        return self.width * self.length * self.height


class Cube(Cuboid):
    def __init__(self, a):
        super().__init__(a, a, a)

    @property
    def name(self):
        return "Cube"


class Pyramid(Solid):
    """Square Pyramid"""

    def __init__(self, a, height):
        """a - base edge"""
        super().__init__(a, height)
        self.a = a
        self.height = height

    @property
    def name(self):
        return "Pyramid"

    @property
    def area(self):
        return self.a * (self.a + (self.a**2 + self.height**2 * 4) ** 0.5)

    @property
    def volume(self):
        return self.a**2 * self.height * 1 / 3


class Cylinder(Solid):
    def __init__(self, radius, height):
        super().__init__(radius, height)
        self.radius = radius
        self.height = height

    @property
    def name(self):
        return "Cylinder"

    @property
    def area(self):
        return 2 * pi * self.radius * (self.height + self.radius)

    @property
    def volume(self):
        return self.radius**2 * pi * self.height


class Cone(Solid):
    def __init__(self, radius, height):
        super().__init__(radius, height)
        self.radius = radius
        self.height = height

    @property
    def name(self):
        return "Cone"

    @property
    def area(self):
        return (
            pi
            * self.radius
            * (self.radius + (self.radius**2 + self.height**2) ** 0.5)
        )

    @property
    def volume(self):
        return self.radius**2 * pi * self.height * 1 / 3
