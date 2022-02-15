#!/usr/bin/env python3
import sys
import os

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

    def positive_number_input(prompt, default_value):
        return st.number_input(prompt, value=default_value, min_value=1)

    try:
        match option:
            case "Circle":
                r = positive_number_input("Radius:", default_value=25)
                shape = Circle(radius=r)
            case "Square":
                a = positive_number_input("Side:", default_value=40)
                shape = Square(a=a)
            case "Rectangle":
                a = positive_number_input("Side A:", default_value=30)
                b = positive_number_input("Side B:", default_value=40)
                shape = Rectangle(a=a, b=b)
            case "Triangle":
                a = positive_number_input("Side A:", default_value=20)
                b = positive_number_input("Side B:", default_value=30)
                c = positive_number_input("Side C:", default_value=40)
                shape = Triangle(a=a, b=b, c=c)
            case "Trapezoid":
                a = positive_number_input("Top base:", default_value=30)
                b = positive_number_input("Bottom base:", default_value=40)
                h = positive_number_input("Height:", default_value=20)
                shape = Trapezoid(a=a, b=b, height=h)
            case "Rhombus":
                a = positive_number_input("Side:", default_value=40)
                h = positive_number_input("Height:", default_value=30)
                shape = Rhombus(a=a, height=h)
            case "Sphere":
                r = positive_number_input("Radius:", default_value=15)
                shape = Sphere(radius=r)
            case "Cube":
                a = positive_number_input("Side:", default_value=15)
                shape = Cube(a=a)
            case "Cuboid":
                w = positive_number_input("Width:", default_value=20)
                l = positive_number_input("Length:", default_value=40)
                h = positive_number_input("Height:", default_value=25)
                shape = Cuboid(width=w, length=l, height=h)
            case "Pyramid":
                a = positive_number_input("Base edge:", default_value=30)
                h = positive_number_input("Height:", default_value=40)
                shape = Pyramid(a=a, height=h)
            case "Cylinder":
                r = positive_number_input("Radius:", default_value=20)
                h = positive_number_input("Height:", default_value=40)
                shape = Cylinder(radius=r, height=h)
            case "Cone":
                r = positive_number_input("Radius:", default_value=20)
                h = positive_number_input("Height:", default_value=40)
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
                            st.write("Median A:", round_float(shape.get_median(1)))
                        with col2:
                            st.write("Median B:", round_float(shape.get_median(2)))
                        with col3:
                            st.write("Median C:", round_float(shape.get_median(3)))
                    write_visualization(shape)
                case Solid():
                    st.write("Volume:", round_float(shape.volume))
                    write_visualization(shape, is_3d=True)
                case _:
                    raise ValueError("Invalid shape.")
    except Exception as e:
        st.error(f"Error: {e}")


if __name__ == "__main__":
    if st._is_running_with_streamlit:
        try:
            render_page()
        except Exception as e:
            sys.stderr.write(f"Exception: {e}" + os.linesep)
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
