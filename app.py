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

    # TODO match case
    try:
        figure = None
        if option == 'Circle':
            r = st.number_input('Radius:', value=25, min_value=0)
            figure = Circle(radius=r)
        elif option == 'Square':
            a = st.number_input('Side:', value=40, min_value=0)
            figure = Square(a=a)
        elif option == 'Rectangle':
            a = st.number_input('Side A:', value=30, min_value=0)
            b = st.number_input('Side B:', value=40, min_value=0)
            figure = Rectangle(a=a, b=b)
        elif option == 'Triangle':
            a = st.number_input('Side A:', value=20, min_value=0)
            b = st.number_input('Side B:', value=30, min_value=0)
            c = st.number_input('Side C:', value=40, min_value=0)
            figure = Triangle(a=a, b=b, c=c)
        elif option == 'Trapezoid':
            a = st.number_input('Top base:', value=30, min_value=0)
            b = st.number_input('Bottom base:', value=40, min_value=0)
            h = st.number_input('Height:', value=20, min_value=0)
            figure = Trapezoid(a=a, b=b, height=h)
        elif option == 'Rhombus':
            a = st.number_input('Side:', value=40, min_value=0)
            h = st.number_input('Height:', value=30, min_value=0)
            figure = Rhombus(a=a, height=h)
        elif option == 'Sphere':
            r = st.number_input('Radius:', value=15, min_value=0)
            figure = Sphere(radius=r)
        elif option == 'Cube':
            a = st.number_input('Side:', value=15, min_value=0)
            figure = Cube(a=a)
        elif option == 'Cuboid':
            a = st.number_input('Length:', value=15, min_value=0)
            b = st.number_input('Width:', value=20, min_value=0)
            h = st.number_input('Height:', value=25, min_value=0)
            figure = Cuboid(length=a, width=b, height=h)
        elif option == 'Pyramid':
            a = st.number_input('Base edge:', value=30, min_value=0)
            h = st.number_input('Height:', value=40, min_value=0)
            figure = Pyramid(a=a, height=h)
        elif option == 'Cylinder':
            r = st.number_input('Radius:', value=20, min_value=0)
            h = st.number_input('Height:', value=40, min_value=0)
            figure = Cylinder(radius=r, height=h)
        elif option == 'Cone':
            r = st.number_input('Radius:', value=20, min_value=0)
            h = st.number_input('Height:', value=40, min_value=0)
            figure = Cone(radius=r, height=h)

        if figure:
            st.caption('Result:')
            st.write('Area:', round_float(figure.area))
            # TODO match case
            if isinstance(figure, Flat):
                st.write('Perimeter:', round_float(figure.perimeter))
                if isinstance(figure, Triangle):
                    # create columns to show values side-by-side
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write('Median A:', round_float(
                            figure.get_median(1)))
                    with col2:
                        st.write('Median B:', round_float(
                            figure.get_median(2)))
                    with col3:
                        st.write('Median C:', round_float(
                            figure.get_median(3)))
                write_visualization(figure)
            elif isinstance(figure, Solid):
                st.write('Volume:', round_float(figure.volume))
                write_visualization(figure, is_3d=True)
    except Exception as e:
        st.error(f'Error: {e}')
        st.exception(e)


if __name__ == '__main__':
    try:
        render_page()
    except Exception as e:
        sys.stderr.write(f"Exception: {e}" + os.linesep)
