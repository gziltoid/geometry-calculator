#!usr/bin/env python
import sys
import os
import streamlit as st
import pythreejs as THREE
from ipywidgets import embed
import streamlit.components.v1 as components

from shapes import *
from mesh_factory import MeshFactory


VISUALIZATION_VIEW_WIDTH = 700
VISUALIZATION_VIEW_HEIGHT = 500


def write_visualization(figure, is_3d=False):
    obj = MeshFactory.create_mesh(figure)
    if not obj:
        return

    camera_pos = (60, 60, 90) if is_3d else (0, 0, 100)
    camera = THREE.CombinedCamera(
        position=camera_pos, width=VISUALIZATION_VIEW_WIDTH, height=VISUALIZATION_VIEW_HEIGHT)
    camera.lookAt((0, 0, 0))
    orbit = THREE.OrbitControls(controlling=camera, target=(0, 0, 0))
    orbit.enableRotate = is_3d

    light = THREE.PointLight(position=[200, 300, 100])
    scene = THREE.Scene(children=[obj, camera, light])

    # show axes for 3d shapes
    if is_3d:
        axesHelper = THREE.AxesHelper(100)
        scene.add(axesHelper)

    renderer = THREE.Renderer(scene=scene, camera=camera, controls=[orbit],
                              width=VISUALIZATION_VIEW_WIDTH, height=VISUALIZATION_VIEW_HEIGHT)
    # embed shape visualization block
    snippet = embed.embed_snippet(views=renderer)
    html = embed.html_template.format(title="Shape", snippet=snippet)
    components.html(html, width=VISUALIZATION_VIEW_WIDTH,
                    height=VISUALIZATION_VIEW_HEIGHT)


def round_float(number):
    return round(number, 2)


def render_page():
    st.write("""# Geometry Calculator""")
    options = ('Circle', 'Square', 'Rectangle', 'Triangle', 'Trapezoid',
               'Rhombus', 'Sphere', 'Cube', 'Cuboid', 'Pyramid', 'Cylinder', 'Cone')

    option = st.selectbox('Select a figure:', options=options)

    try:
        match option:
            case 'Circle':
                r = st.number_input('Radius:', value=25, min_value=1)
                figure = Circle(radius=r)
            case 'Square':
                a = st.number_input('Side:', value=40, min_value=1)
                figure = Square(a=a)
            case 'Rectangle':
                a = st.number_input('Side A:', value=30, min_value=1)
                b = st.number_input('Side B:', value=40, min_value=1)
                figure = Rectangle(a=a, b=b)
            case 'Triangle':
                a = st.number_input('Side A:', value=20, min_value=1)
                b = st.number_input('Side B:', value=30, min_value=1)
                c = st.number_input('Side C:', value=40, min_value=1)
                figure = Triangle(a=a, b=b, c=c)
            case 'Trapezoid':
                a = st.number_input('Top base:', value=30, min_value=1)
                b = st.number_input('Bottom base:', value=40, min_value=1)
                h = st.number_input('Height:', value=20, min_value=1)
                figure = Trapezoid(a=a, b=b, height=h)
            case 'Rhombus':
                a = st.number_input('Side:', value=40, min_value=1)
                h = st.number_input('Height:', value=30, min_value=1)
                figure = Rhombus(a=a, height=h)
            case 'Sphere':
                r = st.number_input('Radius:', value=15, min_value=1)
                figure = Sphere(radius=r)
            case 'Cube':
                a = st.number_input('Side:', value=15, min_value=1)
                figure = Cube(a=a)
            case 'Cuboid':
                a = st.number_input('Length:', value=15, min_value=1)
                b = st.number_input('Width:', value=20, min_value=1)
                h = st.number_input('Height:', value=25, min_value=1)
                figure = Cuboid(length=a, width=b, height=h)
            case 'Pyramid':
                a = st.number_input('Base edge:', value=30, min_value=1)
                h = st.number_input('Height:', value=40, min_value=1)
                figure = Pyramid(a=a, height=h)
            case 'Cylinder':
                r = st.number_input('Radius:', value=20, min_value=1)
                h = st.number_input('Height:', value=40, min_value=1)
                figure = Cylinder(radius=r, height=h)
            case 'Cone':
                r = st.number_input('Radius:', value=20, min_value=1)
                h = st.number_input('Height:', value=40, min_value=1)
                figure = Cone(radius=r, height=h)
            case _:
                figure = None

        if figure:
            st.caption('Result:')
            st.write('Area:', round_float(figure.area))
            match figure:
                case Flat():
                    st.write('Perimeter:', round_float(figure.perimeter))
                    if isinstance(figure, Triangle):
                        # create columns to show median values in a row
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.write('Median A:', round_float(figure.get_median(1)))
                        with col2:
                            st.write('Median B:', round_float(figure.get_median(2)))
                        with col3:
                            st.write('Median C:', round_float(figure.get_median(3)))
                    write_visualization(figure)
                case Solid():
                    st.write('Volume:', round_float(figure.volume))
                    write_visualization(figure, is_3d=True)
    except Exception as e:
        st.error(f'Error: {e}')


if __name__ == '__main__':
    try:
        render_page()
    except Exception as e:
        sys.stderr.write(f"Exception: {e}" + os.linesep)
