#!/usr/bin/env python3
import sys
from math import acos, pi, sqrt, tan

import pygame
from external.three_py.cameras.OrthographicCamera import OrthographicCamera
from external.three_py.cameras.PerspectiveCamera import PerspectiveCamera
from external.three_py.core import Mesh, Renderer, Scene
from external.three_py.geometry import LineGeometry
from external.three_py.geometry.BoxGeometry import BoxGeometry
from external.three_py.geometry.CircleGeometry import CircleGeometry
from external.three_py.geometry.ConeGeometry import ConeGeometry
from external.three_py.geometry.CylinderGeometry import CylinderGeometry
from external.three_py.geometry.PyramidGeometry import PyramidGeometry
from external.three_py.geometry.SphereGeometry import SphereGeometry
from external.three_py.lights import PointLight
from external.three_py.material import LineBasicMaterial, SurfaceBasicMaterial, SurfaceLightMaterial

SEGMENTS = 32


class GUI:
    def __init__(self):
        pygame.display.init()
        pygame.font.init()

        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)

        # pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 4)
        # pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 1)
        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)
        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

        pygame.display.set_caption("Shapes")
        pygame.display.set_mode((600, 800), pygame.DOUBLEBUF | pygame.OPENGL)

        self.__clock = pygame.time.Clock()

        self.__renderer = Renderer()
        self.__renderer.setViewport(0, 0, 600, 600)
        self.__renderer.setClearColor(0.15, 0.15, 0.15)

        self.__scene = Scene()
        self.__scene.add(PointLight(position=(200, 300, 100)))

        self.__set_2d_camera()
        self.__mesh = None

    @staticmethod
    def create_2d_mesh(*points):
        geometry = LineGeometry(points)
        return Mesh(geometry, LineBasicMaterial())

    @staticmethod
    def create_3d_mesh(geometry):
        return Mesh(geometry, SurfaceLightMaterial(alpha=0.65))

    @staticmethod
    def create_circle_mesh(radius):
        geometry = CircleGeometry(radius, segments=50)
        return Mesh(geometry, SurfaceBasicMaterial())

    @staticmethod
    def create_square_mesh(size):
        return GUI.create_rectangle_mesh(size, size)

    @staticmethod
    def create_rectangle_mesh(width, height):
        mesh = GUI.create_2d_mesh(
            (0, 0, 0),
            (width, 0, 0),
            (width, height, 0),
            (0, height, 0),
            (0, 0, 0)
        )
        mesh.transform.setPosition(-width / 2, -height / 2)
        return mesh

    @staticmethod
    def calculate_third_triangle_point(alpha, beta, c):
        x = (c * tan(beta)) / (tan(alpha) + tan(beta))
        y = x * tan(alpha)
        return x, y

    @staticmethod
    def create_triangle_mesh(a, b, c):
        (a, b, c) = sorted((a, b, c))
        if a + b < c:
            raise ValueError("Invalid triangle size")
        alpha = acos((b ** 2 + c ** 2 - a ** 2) / (2.0 * b * c))
        beta = acos((-b ** 2 + c ** 2 + a ** 2) / (2.0 * a * c))
        (x, y) = GUI.calculate_third_triangle_point(alpha, beta, c)
        mesh = GUI.create_2d_mesh(
            (0, 0, 0),
            (c, 0, 0),
            (x, y, 0),
            (0, 0, 0)
        )
        mesh.transform.setPosition(-c / 2, -y / 2)
        return mesh

    @staticmethod
    def create_trapezoid_mesh(a, b, h):
        (a, b) = sorted((a, b))
        x = (a + b) / 2
        mesh = GUI.create_2d_mesh(
            (0, 0, 0),
            (b, 0, 0),
            (x, h, 0),
            (x - a, h, 0),
            (0, 0, 0)
        )
        mesh.transform.setPosition(-b / 2, -h / 2)
        return mesh

    @staticmethod
    def create_rhombus_mesh(a, h):
        if h > a:
            raise ValueError("Invalid rhombus size")
        x = sqrt(a ** 2 - h ** 2)
        mesh = GUI.create_2d_mesh(
            (0, 0, 0),
            (a, 0, 0),
            (x + a, h, 0),
            (x, h, 0),
            (0, 0, 0)
        )
        mesh.transform.setPosition(-(x + a) / 2, -h / 2)
        return mesh

    @staticmethod
    def create_sphere_mesh(radius):
        return GUI.create_3d_mesh(SphereGeometry(radius, SEGMENTS, SEGMENTS))

    @staticmethod
    def create_cube_mesh(size):
        return GUI.create_cuboid_mesh(size, size, size)

    @staticmethod
    def create_cuboid_mesh(a, b, c):
        return GUI.create_3d_mesh(BoxGeometry(a, b, c))

    @staticmethod
    def create_pyramid_mesh(a, height):
        radius = a / sqrt(2)
        mesh = GUI.create_3d_mesh(PyramidGeometry(radius, 4, height))
        mesh.transform.rotateY(pi / 6)
        return mesh

    @staticmethod
    def create_cylinder_mesh(radius, height):
        return GUI.create_3d_mesh(CylinderGeometry(radius, radius, SEGMENTS, height))

    @staticmethod
    def create_cone_mesh(radius, height):
        return GUI.create_3d_mesh(ConeGeometry(radius, SEGMENTS, height))

    def __update_mesh(self, mesh):
        if self.__mesh:
            self.__scene.remove(self.__mesh)
        self.__scene.add(mesh)
        self.__mesh = mesh

    def __set_2d_camera(self):
        self.camera = OrthographicCamera(-50, 50, 50, -50)

    def __set_3d_camera(self):
        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(60, 30, 60)
        self.camera.transform.lookAt(0, 0, 0)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_0:
                        self.__update_mesh(GUI.create_circle_mesh(30))
                        self.__set_2d_camera()
                    elif event.key == pygame.K_1:
                        self.__update_mesh(GUI.create_square_mesh(40))
                        self.__set_2d_camera()
                    elif event.key == pygame.K_2:
                        self.__update_mesh(GUI.create_rectangle_mesh(30, 40))
                        self.__set_2d_camera()
                    elif event.key == pygame.K_3:
                        self.__update_mesh(
                            GUI.create_triangle_mesh(30, 40, 50))
                        self.__set_2d_camera()
                    elif event.key == pygame.K_4:
                        self.__update_mesh(
                            GUI.create_trapezoid_mesh(30, 40, 20))
                        self.__set_2d_camera()
                    elif event.key == pygame.K_5:
                        self.__update_mesh(GUI.create_rhombus_mesh(30, 20))
                        self.__set_2d_camera()
                    elif event.key == pygame.K_6:
                        self.__update_mesh(GUI.create_sphere_mesh(30))
                        self.__set_3d_camera()
                    elif event.key == pygame.K_7:
                        self.__update_mesh(GUI.create_cube_mesh(40))
                        self.__set_3d_camera()
                    elif event.key == pygame.K_8:
                        self.__update_mesh(
                            GUI.create_cuboid_mesh(30, 40, 50))
                        self.__set_3d_camera()
                    elif event.key == pygame.K_9:
                        self.__update_mesh(GUI.create_pyramid_mesh(30, 50))
                        self.__set_3d_camera()
                    elif event.key == pygame.K_q:
                        self.__update_mesh(GUI.create_cylinder_mesh(20, 40))
                        self.__set_3d_camera()
                    elif event.key == pygame.K_w:
                        self.__update_mesh(GUI.create_cone_mesh(30, 50))
                        self.__set_3d_camera()

            self.__renderer.render(self.__scene, self.camera)

            pygame.display.flip()
            self.__clock.tick(60)


if __name__ == "__main__":
    gui = GUI()
    gui.run()
