from math import acos, sqrt, tan
import sys
import os
import streamlit as st
import pythreejs as THREE

from model import *


SEGMENTS = 32


def create_2d_mesh(*points):
    width = max([p[0] for p in points])
    height = max([p[1] for p in points])
    geometry = THREE.Geometry(vertices=points)
    lines = THREE.Line(geometry, THREE.LineBasicMaterial(color="#0000ff"))
    lines.position = (-width / 2, -height / 2, 0)
    return lines


def create_circle_mesh(radius):
    geometry = THREE.CircleGeometry(radius, segments=50)
    return THREE.Mesh(geometry, THREE.MeshBasicMaterial(color="#5f9ea0"))


def create_rectangle_mesh(width, height):
    return create_2d_mesh(
        (0, 0, 0),
        (width, 0, 0),
        (width, height, 0),
        (0, height, 0),
        (0, 0, 0)
    )


def create_square_mesh(size):
    return create_rectangle_mesh(size, size)


def calculate_third_triangle_point(alpha, beta, c):
    x = (c * tan(beta)) / (tan(alpha) + tan(beta))
    y = x * tan(alpha)
    return x, y


def create_triangle_mesh(a, b, c):
    (a, b, c) = sorted((a, b, c))
    if a + b <= c:
        raise ValueError("Invalid triangle size")
    alpha = acos((b ** 2 + c ** 2 - a ** 2) / (2.0 * b * c))
    beta = acos((-b ** 2 + c ** 2 + a ** 2) / (2.0 * a * c))
    (x, y) = calculate_third_triangle_point(alpha, beta, c)
    return create_2d_mesh(
        (0, 0, 0),
        (c, 0, 0),
        (x, y, 0),
        (0, 0, 0)
    )


def create_trapezoid_mesh(a, b, h):
    (a, b) = sorted((a, b))
    x = (a + b) / 2
    return create_2d_mesh(
        (0, 0, 0),
        (b, 0, 0),
        (x, h, 0),
        (x - a, h, 0),
        (0, 0, 0)
    )


def create_rhombus_mesh(a, h):
    if h > a:
        raise ValueError("Invalid rhombus size")
    x = sqrt(a ** 2 - h ** 2)
    return create_2d_mesh(
        (0, 0, 0),
        (a, 0, 0),
        (x + a, h, 0),
        (x, h, 0),
        (0, 0, 0)
    )


def create_3d_mesh(geometry):
    return THREE.Mesh(geometry, THREE.MeshStandardMaterial(color="#6495ed"))


def create_sphere_mesh(radius):
    return create_3d_mesh(THREE.SphereGeometry(radius, SEGMENTS, SEGMENTS))


def create_cuboid_mesh(a, b, c):
    return create_3d_mesh(THREE.BoxGeometry(a, b, c))


def create_cube_mesh(size):
    return create_cuboid_mesh(size, size, size)


def create_pyramid_mesh(a, height):
    radius = a / sqrt(2)
    mesh = create_3d_mesh(THREE.ConeGeometry(radius, height, 4))
    mesh.rotateY(pi / 6)
    return mesh


def create_cylinder_mesh(radius, height):
    return create_3d_mesh(THREE.CylinderGeometry(radius, radius, SEGMENTS, height))


def create_cone_mesh(radius, height):
    return create_3d_mesh(THREE.ConeGeometry(radius, height, SEGMENTS))


def get_2d_camera():
    return THREE.OrthographicCamera(-50, 50, 50, -50)


def get_3d_camera():
    camera = THREE.PerspectiveCamera()
    camera.position = (60, 30, 60)
    camera.lookAt((0, 0, 0))
    return camera


def write_visualization(figure):
    obj = None
    if isinstance(figure, Circle):
        obj = create_circle_mesh(figure.radius)
    elif isinstance(figure, Rectangle):
        obj = create_rectangle_mesh(figure.a, figure.b)
    elif isinstance(figure, Square):
        obj = create_square_mesh(figure.a)
    elif isinstance(figure, Triangle):
        obj = create_triangle_mesh(figure.a, figure.b, figure.c)
    elif isinstance(figure, Trapezoid):
        obj = create_trapezoid_mesh(figure.a, figure.b, figure.height)
    elif isinstance(figure, Rhombus):
        obj = create_rhombus_mesh(figure.a, figure.height)
    elif isinstance(figure, Sphere):
        obj = create_sphere_mesh(figure.radius)
    elif isinstance(figure, Cuboid):
        obj = create_cuboid_mesh(figure.width, figure.length, figure.height)
    elif isinstance(figure, Cube):
        obj = create_cube_mesh(figure.a)
    elif isinstance(figure, Pyramid):
        obj = create_pyramid_mesh(figure.a, figure.height)
    elif isinstance(figure, Cylinder):
        obj = create_cylinder_mesh(figure.radius, figure.height)
    elif isinstance(figure, Cone):
        obj = create_cone_mesh(figure.radius, figure.height)

    if not obj:
        return

    view_width = 700
    view_height = 500

    if is_3d := isinstance(figure, Solid):
        camera_pos = (60, 60, 60)
    else:
        camera_pos = (0, 0, 100)
    camera = THREE.CombinedCamera(
        position=camera_pos, width=view_width, height=view_height)
    camera.lookAt((0, 0, 0))
    orbit = THREE.OrbitControls(controlling=camera, target=(0, 0, 0))
    orbit.enableRotate = is_3d

    light = THREE.PointLight(position=[200, 300, 100])
    scene = THREE.Scene(children=[obj, camera, light])

    # if is_3d:
    #     axesHelper = THREE.AxesHelper(100)
    #     scene.add(axesHelper)

    renderer = THREE.Renderer(scene=scene, camera=camera, controls=[orbit],
                              width=view_width, height=view_height)

    from ipywidgets import embed
    snippet = embed.embed_snippet(views=renderer)
    html = embed.html_template.format(title="Plot", snippet=snippet)

    import streamlit.components.v1 as components
    components.html(html, width=view_width, height=view_height)


st.write("""# Geometry Calculator""")

options = ('Circle', 'Square', 'Rectangle', 'Triangle', 'Trapezoid',
           'Rhombus', 'Sphere', 'Cube', 'Cuboid', 'Pyramid', 'Cylinder', 'Cone')
option = st.selectbox('Select a shape:', options=options)


figure = None
if option == 'Circle':
    r = st.number_input('Radius:', value=25)
    figure = Circle(radius=r)
elif option == 'Square':
    side = st.number_input('Side A:', value=40)
    figure = Square(a=side)
elif option == 'Rectangle':
    a = st.number_input('Side A:', value=30)
    b = st.number_input('Side B:', value=40)
    figure = Rectangle(a=a, b=b)
elif option == 'Triangle':
    a = st.number_input('Side A:', value=20)
    b = st.number_input('Side B:', value=30)
    c = st.number_input('Side C:', value=40)
    figure = Triangle(a=a, b=b, c=c)
elif option == 'Trapezoid':
    a = st.number_input('Top base:', value=30)
    b = st.number_input('Bottom base:', value=40)
    h = st.number_input('Height:', value=20)
    figure = Trapezoid(a=a, b=b, height=h)
elif option == 'Rhombus':
    a = st.number_input('Side A:', value=40)
    h = st.number_input('Height:', value=30)
    figure = Rhombus(a=a, h=h)
elif option == 'Sphere':
    r = st.number_input('Radius:', value=15)
    figure = Sphere(radius=r)
elif option == 'Cube':
    a = st.number_input('Side A:', value=15)
    figure = Cube(a=a)
elif option == 'Cuboid':
    a = st.number_input('Length:', value=15)
    b = st.number_input('Width:', value=20)
    c = st.number_input('Height:', value=25)
    figure = Cuboid(width=a, length=b, height=c)
elif option == 'Pyramid':
    a = st.number_input('Side A:', value=30)
    h = st.number_input('Height:', value=40)
    figure = Pyramid(a=a, h=h)
elif option == 'Cylinder':
    r = st.number_input('Radius:', value=20)
    h = st.number_input('Height:', value=40)
    figure = Cylinder(radius=r, h=h)
elif option == 'Cone':
    r = st.number_input('Radius:', value=20)
    h = st.number_input('Height:', value=40)
    figure = Cone(radius=r, h=h)


try:
    if figure:
        st.caption('Result:')
        st.write('Area:', figure.area)
        if isinstance(figure, Flat):
            st.write('Perimeter:', figure.perimeter)
            if isinstance(figure, Triangle):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write('Median 1:', figure.get_median(1))
                with col2:
                    st.write('Median 2:', figure.get_median(2))
                with col3:
                    st.write('Median 3:', figure.get_median(3))
        elif isinstance(figure, Solid):
            st.write('Volume:', figure.volume)
            write_visualization(figure)
except Exception as e:
    st.error(f'Error: {e}')
    st.exception(e)
    sys.stderr.write(f"Exception: {e}" + os.linesep)
