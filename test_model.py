import pytest
from shapes import Circle, Cone, Cube, Cuboid, Cylinder, Pyramid, Rectangle, Rhombus, Square, Sphere, Trapezoid, Triangle


def test_model():
    circle = Circle(radius=5)
    assert circle.name == 'Circle'
    assert circle.area == 78.53981633974483
    assert circle.perimeter == 31.41592653589793

    square = Square(a=7.3)
    assert square.name == 'Square'
    assert square.area == 53.29
    assert square.perimeter == 29.2

    rect = Rectangle(a=5, b=6.5)
    assert rect.name == 'Rectangle'
    assert rect.area == 32.5

    triangle = Triangle(a=5, b=6, c=7)
    assert triangle.name == 'Triangle'
    assert triangle.area == 14.696938456699069
    assert triangle.perimeter == 18

    trapezoid = Trapezoid(a=5, b=10, height=6)
    assert trapezoid.name == 'Trapezoid'
    assert trapezoid.area == 45
    assert trapezoid.perimeter == 99.5

    rhombus = Rhombus(a=10, height=15)
    assert rhombus.name == 'Rhombus'
    assert rhombus.area == 150

    rhombus = Rhombus.from_side_and_angle(side=10, angle=30)
    assert rhombus.area == 49.99999999999999

    sphere = Sphere(radius=5)
    assert sphere.name == 'Sphere'
    assert sphere.area == 314.1592653589793
    assert sphere.volume == 523.5987755982989

    cube = Cube(a=5)
    assert cube.name == 'Cube'
    assert cube.area == 150
    assert cube.volume == 125

    cuboid = Cuboid(width=5, length=10, height=15)
    assert cuboid.name == 'Cuboid'
    assert cuboid.area == 550
    assert cuboid.volume == 750

    pyramid = Pyramid(a=5, height=10)
    assert pyramid.name == 'Pyramid'
    assert pyramid.area == 128.07764064044153
    assert pyramid.volume == 83.33333333333333

    cylinder = Cylinder(radius=5, height=10)
    assert cylinder.name == 'Cylinder'
    assert cylinder.area == 471.23889803846896
    assert cylinder.volume == 785.3981633974483

    cone = Cone(radius=5, height=10)
    assert cone.name == 'Cone'
    assert cone.area == 254.160184615763
    assert cone.volume == 261.79938779914943


def test_invalid_params():
    with pytest.raises(ValueError):
        Triangle(a=1, b=2, c=3)
    with pytest.raises(ValueError):
        Circle(radius=-5)
    with pytest.raises(ValueError):
        Cone(radius=5, height=-10)

    


def test_triangle_median():
    triangle = Triangle(a=20, b=30, c=40)
    assert round(triangle.get_median(side_number=1), 2) == 33.91
    assert round(triangle.get_median(side_number=2), 2) == 27.84
    assert round(triangle.get_median(side_number=3), 2) == 15.81
