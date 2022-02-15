#!/usr/bin/env python3
import os
import sys

import pythreejs as THREE
import streamlit as st
from streamlit import cli as stcli
import streamlit.components.v1 as components
from ipywidgets import embed


from mesh_factory import MeshFactory
from shapes import *

VISUALIZATION_VIEW_WIDTH = 700
VISUALIZATION_VIEW_HEIGHT = 500


def write_visualization(shape, is_3d=False):
    obj = MeshFactory.create_mesh(shape)
    if not obj:
        return
    camera_pos = (60, 60, 90) if is_3d else (0, 0, 100)
    camera = THREE.CombinedCamera(
        position=camera_pos,
        width=VISUALIZATION_VIEW_WIDTH,
        height=VISUALIZATION_VIEW_HEIGHT,
    )
    camera.lookAt((0, 0, 0))
    orbit = THREE.OrbitControls(controlling=camera, target=(0, 0, 0))
    orbit.enableRotate = is_3d

    light = THREE.PointLight(position=[200, 300, 100])
    scene = THREE.Scene(children=[obj, camera, light])

    # show axes for 3d shapes
    if is_3d:
        axes_helper = THREE.AxesHelper(100)
        scene.add(axes_helper)

    renderer = THREE.Renderer(
        scene=scene,
        camera=camera,
        controls=[orbit],
        width=VISUALIZATION_VIEW_WIDTH,
        height=VISUALIZATION_VIEW_HEIGHT,
    )
    # embed shape visualization block
    snippet = embed.embed_snippet(views=renderer)
    html = embed.html_template.format(title="Shape", snippet=snippet)
    components.html(
        html, width=VISUALIZATION_VIEW_WIDTH, height=VISUALIZATION_VIEW_HEIGHT
    )


def round_float(number):
    return round(number, 2)


def render_page():
    st.write("""# Geometry Calculator""")
    options = (
        "Circle",
        "Square",
        "Rectangle",
        "Triangle",
        "Trapezoid",
        "Rhombus",
        "Sphere",
        "Cube",
        "Cuboid",
        "Pyramid",
        "Cylinder",
        "Cone",
    )

    option = st.selectbox("Select a shape:", options=options)

    # TODO positive_number_input(prompt, default_value)
    try:
        match option:
            case "Circle":
                r = st.number_input("Radius:", value=25, min_value=1)
                shape = Circle(radius=r)
            case "Square":
                a = st.number_input("Side:", value=40, min_value=1)
                shape = Square(a=a)
            case "Rectangle":
                a = st.number_input("Side A:", value=30, min_value=1)
                b = st.number_input("Side B:", value=40, min_value=1)
                shape = Rectangle(a=a, b=b)
            case "Triangle":
                a = st.number_input("Side A:", value=20, min_value=1)
                b = st.number_input("Side B:", value=30, min_value=1)
                c = st.number_input("Side C:", value=40, min_value=1)
                shape = Triangle(a=a, b=b, c=c)
            case "Trapezoid":
                a = st.number_input("Top base:", value=30, min_value=1)
                b = st.number_input("Bottom base:", value=40, min_value=1)
                h = st.number_input("Height:", value=20, min_value=1)
                shape = Trapezoid(a=a, b=b, height=h)
            case "Rhombus":
                a = st.number_input("Side:", value=40, min_value=1)
                h = st.number_input("Height:", value=30, min_value=1)
                shape = Rhombus(a=a, height=h)
            case "Sphere":
                r = st.number_input("Radius:", value=15, min_value=1)
                shape = Sphere(radius=r)
            case "Cube":
                a = st.number_input("Side:", value=15, min_value=1)
                shape = Cube(a=a)
            case "Cuboid":
                a = st.number_input("Length:", value=15, min_value=1)
                b = st.number_input("Width:", value=20, min_value=1)
                h = st.number_input("Height:", value=25, min_value=1)
                shape = Cuboid(length=a, width=b, height=h)
            case "Pyramid":
                a = st.number_input("Base edge:", value=30, min_value=1)
                h = st.number_input("Height:", value=40, min_value=1)
                shape = Pyramid(a=a, height=h)
            case "Cylinder":
                r = st.number_input("Radius:", value=20, min_value=1)
                h = st.number_input("Height:", value=40, min_value=1)
                shape = Cylinder(radius=r, height=h)
            case "Cone":
                r = st.number_input("Radius:", value=20, min_value=1)
                h = st.number_input("Height:", value=40, min_value=1)
                shape = Cone(radius=r, height=h)
            case _:
                shape = None

        if shape:
            st.caption("Result:")
            st.write("Area:", round_float(shape.area))
            match shape:
                case Flat():
                    st.write("Perimeter:", round_float(shape.perimeter))
                    if isinstance(shape, Triangle):
                        # create columns to show median values in a row
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.write("Median A:", round_float(
                                shape.get_median(1)))
                        with col2:
                            st.write("Median B:", round_float(
                                shape.get_median(2)))
                        with col3:
                            st.write("Median C:", round_float(
                                shape.get_median(3)))
                    write_visualization(shape)
                case Solid():
                    st.write("Volume:", round_float(shape.volume))
                    write_visualization(shape, is_3d=True)
                case _:
                    raise ValueError("Invalid shape.")
    except Exception as e:
        st.error(f"Error: {e}")


if __name__ == '__main__':
    if st._is_running_with_streamlit:
        try:
            render_page()
        except Exception as e:
            sys.stderr.write(f"Exception: {e}" + os.linesep)
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
