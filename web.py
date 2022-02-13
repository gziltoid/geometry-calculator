from math import sqrt
import streamlit as st
import pythreejs as THREE

from model import *


SEGMENTS = 32


# def createLine(points):
#     let vertices = [];
#     let width = 0;
#     let height = 0;
#     for (p of points) {
#     if (p[0] > width) {
#         width = p[0];
#     }
#     if (p[1] > height) {
#         height = p[1];
#     }
#     vertices.push(new THREE.Vector3(p[0], p[1], p[2]));
#     }
#     const geometry = new THREE.BufferGeometry().setFromPoints(vertices);
#     let line = new THREE.Line(geometry);
#     line.translateX(-width / 2);
#     line.translateY(-height / 2);
#     return line;


def create_3d_mesh(geometry):
    return THREE.Mesh(geometry, THREE.MeshStandardMaterial())


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
    if not figure:
        return

    base = THREE.Mesh(
        THREE.BoxBufferGeometry(20, 0.1, 20),
        THREE.MeshLambertMaterial(color='green', opacity=0.5, transparent=True),
        position=(0, 0, 0),
    )
    obj = create_cube_mesh(15)

    view_width = 700
    view_height = 500
    target = (0, 0, 0)
    camera = THREE.CombinedCamera(position=[60, 60, 60], width=view_width, height=view_height)
    # camera.mode = 'orthographic'
    camera.lookAt(target)
    # camera.zoom = 1
    # camera = get_3d_camera()
    orbit = THREE.OrbitControls(controlling=camera, target=target)

    lights = [
        THREE.PointLight(position=[200, 0, 0], color="#ffffff"),
        THREE.PointLight(position=[0, 200, 0], color="#bbbbbb"),
        THREE.PointLight(position=[0, 0, 200], color="#888888"),
        THREE.AmbientLight(intensity=0.2),
    ]

    scene = THREE.Scene(children=[base, obj, camera] + lights)

    renderer = THREE.Renderer(scene=scene, camera=camera, controls=[orbit],
                        width=view_width, height=view_height)


    from ipywidgets import embed
    snippet = embed.embed_snippet(views=renderer)
    html = embed.html_template.format(title="", snippet=snippet)

    import streamlit.components.v1 as components
    components.html(html, width=view_width, height=view_height)


st.write("""# Geometry Calculator""")

options = ['Circle', 'Square', 'Rectangle', 'Triangle', 'Trapezoid',
           'Rhombus', 'Sphere', 'Cube', 'Cuboid', 'Pyramid', 'Cylinder', 'Cone']
option = st.selectbox('Select a shape:', options=options)


width = 20
figure = None
if option == 'Circle':
    r = st.number_input('Radius:')
    figure = Circle(radius=r)
elif option == 'Square':
    side = st.number_input('Side:')
    figure = Square(a=side)
elif option == 'Rectangle':
    a = st.number_input('A:')
    b = st.number_input('B:')
    figure = Rectangle(a=a, b=b)
elif option == 'Triangle':
    a = st.number_input('A:')
    b = st.number_input('B:')
    c = st.number_input('C:')
    figure = Triangle(a=a, b=b, c=c)
elif option == 'Trapezoid':
    a = st.number_input('A:')
    b = st.number_input('B:')
    h = st.number_input('H:')
    figure = Trapezoid(a=a, b=b, height=h)
elif option == 'Rhombus':
    a = st.number_input('A:')
    h = st.number_input('H:')
    figure = Rhombus(a=a, h=h)
elif option == 'Sphere':
    r = st.number_input('Radius:')
    figure = Sphere(radius=r)
elif option == 'Cube':
    a = st.number_input('A:')
    figure = Cube(a=a)
elif option == 'Cuboid':
    a = st.number_input('A:')
    b = st.number_input('B:')
    c = st.number_input('C:')
    figure = Cuboid(a=a, b=b, c=c)
elif option == 'Pyramid':
    a = st.number_input('A:')
    h = st.number_input('H:')
    figure = Pyramid(a=a, h=h)
elif option == 'Cylinder':
    r = st.number_input('Radius:')
    h = st.number_input('H:')
    figure = Cylinder(radius=r, h=h)
elif option == 'Cone':
    r = st.number_input('Radius:')
    h = st.number_input('H:')
    figure = Cone(radius=r, h=h)
    st.write(figure.volume())


# st.write('You selected:', option)

if st.button("Calculate"):
    st.write('Why hello there')
    write_visualization(figure)
