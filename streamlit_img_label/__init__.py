#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Tuesday 19 Apr. 2024
# ==============================================================================
# This script was adapted from the original work of Tianning Li:
# <https://github.com/lit26/streamlit-img-label/tree/main>
# ==============================================================================


import os
import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import utils.functions as fct

# from .manage import ImageManager


_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "st_img_label",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("st_img_label", path=build_dir)


def st_img_label(resized_img, box_color="blue", rects=[], key=None):
    """Create a new instance of "st_img_label".

    Parameters
    ----------
    img_file: PIL.Image
        The image to be croppepd
    box_color: string
        The color of the cropper's bounding box. Defaults to blue.
    rects: list
        list of bounding boxes that already exists.
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    rects: list
        list of bounding boxes.
    """
    # Get arguments to send to frontend
    canvasWidth = resized_img.width
    canvasHeight = resized_img.height

    # Translates image to a list for passing to Javascript
    imageData = np.array(resized_img.convert("RGBA")).flatten().tolist()

    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # Defaults to a box whose vertices are at 20% and 80% of height and width.
    # The _recommended_box function could be replaced with some kind of image
    # detection algorith if it suits your needs.
    component_value = _component_func(
        canvasWidth=canvasWidth,
        canvasHeight=canvasHeight,
        rects=rects,
        boxColor=box_color,
        imageData=imageData,
        key=key,
    )
    # Return a cropped image using the box from the frontend
    if component_value:
        return component_value["rects"]
    else:
        return rects
