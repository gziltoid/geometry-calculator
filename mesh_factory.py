from math import acos, sqrt, tan
from operator import itemgetter

import pythreejs as THREE

from shapes import *


class MeshFactory:
    __SEGMENTS = 32

    @staticmethod
    def __create_2d_mesh(*points):
        width = max(points, key=itemgetter(0))[0]
        height = max(points, key=itemgetter(1))[1]
        geometry = THREE.Geometry(vertices=points)
        lines = THREE.Line(geometry, THREE.LineBasicMaterial(color="#0000ff"))
        lines.position = (-width / 2, -height / 2, 0)
        return lines

    @staticmethod
    def __create_circle_mesh(radius):
        geometry = THREE.CircleGeometry(radius, segments=50)
        return THREE.Mesh(geometry, THREE.MeshBasicMaterial(color="#5f9ea0"))

    @staticmethod
    def __create_rectangle_mesh(width, height):
        return MeshFactory.__create_2d_mesh(
            (0, 0, 0), (width, 0, 0), (width, height, 0), (0, height, 0), (0, 0, 0)
        )

    @staticmethod
    def __create_square_mesh(size):
        return MeshFactory.__create_rectangle_mesh(size, size)

    @staticmethod
    def __calculate_third_triangle_point(alpha, beta, c):
        x = (c * tan(beta)) / (tan(alpha) + tan(beta))
        y = x * tan(alpha)
        return x, y

    @staticmethod
    def __create_triangle_mesh(a, b, c):
        (a, b, c) = sorted((a, b, c))
        if a + b <= c:
            raise ValueError("Invalid triangle size.")
        alpha = acos((b**2 + c**2 - a**2) / (2.0 * b * c))
        beta = acos((-(b**2) + c**2 + a**2) / (2.0 * a * c))
        (x, y) = MeshFactory.__calculate_third_triangle_point(alpha, beta, c)
        return MeshFactory.__create_2d_mesh((0, 0, 0), (c, 0, 0), (x, y, 0), (0, 0, 0))

    @staticmethod
    def __create_trapezoid_mesh(a, b, h):
        x = (a + b) / 2
        return MeshFactory.__create_2d_mesh(
            (0, 0, 0), (b, 0, 0), (x, h, 0), (x - a, h, 0), (0, 0, 0)
        )

    @staticmethod
    def __create_rhombus_mesh(a, h):
        if h > a:
            raise ValueError("Invalid rhombus size.")
        x = sqrt(a**2 - h**2)
        return MeshFactory.__create_2d_mesh(
            (0, 0, 0), (a, 0, 0), (x + a, h, 0), (x, h, 0), (0, 0, 0)
        )

    @staticmethod
    def __create_3d_mesh(geometry):
        return THREE.Mesh(geometry, THREE.MeshStandardMaterial(color="#6495ed"))

    @staticmethod
    def __create_sphere_mesh(radius):
        return MeshFactory.__create_3d_mesh(
            THREE.SphereGeometry(radius, MeshFactory.__SEGMENTS, MeshFactory.__SEGMENTS)
        )

    @staticmethod
    def __create_cuboid_mesh(a, b, c):
        return MeshFactory.__create_3d_mesh(THREE.BoxGeometry(a, b, c))

    @staticmethod
    def __create_cube_mesh(size):
        return MeshFactory.__create_cuboid_mesh(size, size, size)

    @staticmethod
    def __create_pyramid_mesh(a, height):
        radius = a / sqrt(2)
        mesh = MeshFactory.__create_3d_mesh(THREE.ConeGeometry(radius, height, 4))
        mesh.rotateY(pi / 6)
        return mesh

    @staticmethod
    def __create_cylinder_mesh(radius, height):
        return MeshFactory.__create_3d_mesh(
            THREE.CylinderGeometry(radius, radius, MeshFactory.__SEGMENTS, height)
        )

    @staticmethod
    def __create_cone_mesh(radius, height):
        return MeshFactory.__create_3d_mesh(
            THREE.ConeGeometry(radius, height, radialSegments=60)
        )

    @staticmethod
    def create_mesh(shape):
        match shape:
            case Circle():
                return MeshFactory.__create_circle_mesh(shape.radius)
            case Rectangle():
                return MeshFactory.__create_rectangle_mesh(shape.a, shape.b)
            case Square():
                return MeshFactory.__create_square_mesh(shape.a)
            case Triangle():
                return MeshFactory.__create_triangle_mesh(shape.a, shape.b, shape.c)
            case Trapezoid():
                return MeshFactory.__create_trapezoid_mesh(
                    shape.a, shape.b, shape.height
                )
            case Rhombus():
                return MeshFactory.__create_rhombus_mesh(shape.a, shape.height)
            case Sphere():
                return MeshFactory.__create_sphere_mesh(shape.radius)
            case Cuboid():
                return MeshFactory.__create_cuboid_mesh(
                    shape.width, shape.height, shape.length
                )
            case Cube():
                return MeshFactory.__create_cube_mesh(shape.a)
            case Pyramid():
                return MeshFactory.__create_pyramid_mesh(shape.a, shape.height)
            case Cylinder():
                return MeshFactory.__create_cylinder_mesh(shape.radius, shape.height)
            case Cone():
                return MeshFactory.__create_cone_mesh(shape.radius, shape.height)
            case _:
                return None
