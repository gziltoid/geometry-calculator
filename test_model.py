import pytest
from model import Circle, Square, Sphere


def test_area_and_perimeter():
    circle = Circle(radius=5)
    assert circle.name == 'Circle'
    assert circle.area() == 78.53981633974483
    assert circle.perimeter() == 31.41592653589793

    square = Square(a=7.3)
    assert square.name == 'Square'
    assert square.area() == 53.29
    assert square.perimeter() == 29.2

    sphere = Sphere(radius=5)
    assert sphere.name == 'Sphere'
    assert sphere.area() == 314.1592653589793


def test_volume():
    sphere = Sphere(radius=8)
    assert sphere.volume() == 2144.660584850632
    assert sphere.name == 'Sphere'
