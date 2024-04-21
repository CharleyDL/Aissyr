#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Tuesday 19 Apr. 2024
# ==============================================================================

import base64
import dagshub
import json
import mlflow.pyfunc
import numpy as np
import os
import requests
import streamlit as st

import utils.functions as fct

from io import BytesIO
from mlflow.pyfunc import PyFuncModel
from PIL import Image
from streamlit_img_label import st_img_label
from streamlit_img_label.manage import ImageManager
from streamlit_extras.row import row


API_URL = os.getenv("API_URL")
DAGSHUB_REPO_OWNER = os.getenv("DAGSHUB_REPO_OWNER")
DAGSHUB_REPO = os.getenv("DAGSHUB_REPO")
MODEL_URI = os.getenv("MODEL_URI")


## --------------------------- STREAMLIT UTILITIES -------------------------- ##


def button_detect_page() -> None:
    st.markdown("""
    <style>
    [data-testid="baseButton-secondary"] {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    """, unsafe_allow_html=True)


def check_session() -> bool:
    """
    Check if the user is authenticated and set the session state accordingly.
    """
    if 'log' not in st.session_state:
        st.switch_page("pages/error401.py")

    if not st.session_state.log:
        st.session_state['log'] = True
        return True


def clear_session_state(key: str) -> None:
    """
    Clear the session state to avoid duplicate when new detection.
    The rects saved the selection so we don't lose the information.
    """
    st.session_state[key] = []


def disable():
    st.session_state.disabled = True


def enable():
    if st.session_state.disabled == True:
        st.session_state.disabled = False


def logout() -> None:
    """Log out the user and redirect to the home page."""
    st.switch_page("Home.py")


def space() -> None:
    """Add a break line"""
    st.markdown("""<style> <br /> </style>""", unsafe_allow_html=True)


## --------------------------------- MODEL ---------------------------------- ##

@st.cache_resource(show_spinner=False)
def load_model() -> PyFuncModel | None:
    """
    Loads a MLflow PyFuncModel from a dagshub repository and model_uri.
    URI example : "runs:/<run_id>/model"

    Returns:
    ------
        PyFuncModel | None: The loaded PyFuncModel object if successful, 
        else None.
    """
    try:
        dagshub.init(DAGSHUB_REPO, DAGSHUB_REPO_OWNER, mlflow=True)

        model = mlflow.pyfunc.load_model(MODEL_URI)
        return model

    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None


## --------------------------------- IMAGES --------------------------------- ##

def extract_and_resize(image, output_size=(100, 100)) -> Image.Image:
    """
    Extracts a region of interest from an image and resizes it to the specified 
    output size.

    Args:
    ----
        image (Image.Image): The input image from which the ROI will be 
            extracted.
        output_size (Tuple[int, int], optional): The desired output size 
            of the resized image. Defaults to (100, 100).

    Returns:
    ----
        Image.Image: The resized ROI as a PIL image.
    """
    if image.mode != 'RGB':
        image = image.convert('RGB')

    resized_roi = image.resize(output_size, resample=Image.LANCZOS)

    return resized_roi


def encode_image(image: Image.Image) -> str:
    """
    Encodes a PIL image to a base64 string.

    Args:
    ----
        image (Image.Image): The input image to be encoded.

    Returns:
    ----
        str: The base64 encoded image as a string.
    """
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    encoded_img = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return encoded_img


## ------------------------ GLYPHS CLASSIFICATION --------------------------- ##


def mzl_info(label: str) -> dict:
    """
    Retrieves information about a specific MZL from the database.

    Args:
    ----
        label (str): The MZL label to search for.

    Returns:
    -------
        dict: A dictionary containing the information of the MZL :
        mzl_number, glyph_name, glyph and glphy_phonetic
    """
    res = requests.get(url=f"{API_URL}/resources/glyphs/{label}/")
    res_dict = res.json()
    return res_dict


def glyphnet_img_preprocess(image: Image.Image) -> np.ndarray:
    """ 
    Preprocesses an image to make it compatible with the Glyphnet model.

    - The image is resized to 100x100 pixels and converted to grayscale.
    - The pixel values are normalized between 0 and 1.
    - The image is expanded to add a channel dimension.

    Args:
    ----
        image (Image.Image): The input PIL image to be preprocessed.

    Returns:
    -------
        np.ndarray: The preprocessed image as a numpy array.
    """
    image = image.resize((100, 100)).convert("L")
    img_array = np.array(image, dtype=np.float32) / 255.0
    img_preprocessed = np.reshape(img_array, (-1, 100, 100, 1))

    return img_preprocessed


def predicted_class(pred_array: np.ndarray) -> list:
    """
    Predicts the class label and percentage probability from a prediction array.

    Args:
    ----
        pred_array (np.ndarray): The prediction array containing probabilities 
        for each class.

    Returns:
    -------
        list: Contain the predicted class label and percentage probability. 
        - The first element -> the predicted class label.
        - The second element -> the percentage probability.

    Example:
    -------
        >>> prediction = predicted_class(np.array([[0.1, 0.2, 0.7]]))
        >>> print(prediction)
        ['110', 70.0]
    """
    mzl_label = ['1', '10', '110', '112', '24', '248', '252', '380', '490', 
                 '514', '552', '566', '596', '661', '724', '736', '748', '754', 
                 '839', '859', '869', '89']

    pred_idx = np.argmax(pred_array)
    pred_label = mzl_label[pred_idx]
    pred_percentage = round(pred_array[0][pred_idx] * 100, 2)

    ## - Get mzl information from the database
    mzl_information = mzl_info(pred_label)
    pred_result = [
        mzl_information['mzl_number'],
        mzl_information['glyph'],
        mzl_information['glyph_name'],
        pred_percentage
    ]

    return pred_result


def classify_glyph(img_name: str, img: Image.Image, 
                  glyph_selection: Image.Image, bbox: list) -> list:
    """Send request to the API to detect the glyphs in the image.

    Parameters:
    - img_name (str): The name of the tablet
    - img (Image): The full image
    - glyph_selection (list): Image of the selected glyph (not resized)
    - bbox (list): List of dictionary (left, top, width, height, label)

    Returns:
    - pred_result (Image): The detected glyphs label
    """

    ## - Load the model from MLflow
    model = load_model()

    ## - Preprocess & Predict
    img_preprocessed = glyphnet_img_preprocess(glyph_selection)
    pred = model.predict(img_preprocessed)
    pred_result = predicted_class(pred)

    return pred_result


def classification_setup(uploaded_file):

    button_detect_page()

    if "disabled" not in st.session_state:
        st.session_state.disabled = True
    if 'preview_imgs' not in st.session_state:
        st.session_state.preview_imgs = []
    if 'zip_detect' not in st.session_state:
        st.session_state.zip_detect = []

    col1, col2 = st.columns(2)
    with col1:
        im = ImageManager(uploaded_file)
        img = im.get_img()
        resized_img = im.resizing_img()
        resized_rects = im.get_resized_rects()
        rects = st_img_label(resized_img, box_color="red", rects=resized_rects)

        if rects:       # Enable/Disable detect/save/correct button
            enable() 
        else:
            clear_session_state('zip_detect')
            disable()

        ## - Button row for detect, save and correct
        rowOption = row(3, gap='small')
        detect_button = rowOption.button(label="Detect", 
                                  disabled=st.session_state.disabled)
        save_button = rowOption.button(label="Save",
                                       disabled=st.session_state.disabled)
        correct_button = rowOption.button(label="Correct Label",
                                          disabled=st.session_state.disabled)


    with col2:
        space()

        st.session_state.preview_imgs = im.init_annotation(rects)

        _cL, colC, _cR = st.columns([1,4,1])
        with colC:
            tmp_img = st.empty()

        ## - Display the glyph preview for selection
        if st.session_state.preview_imgs:
            for i, prev_img in enumerate(st.session_state.preview_imgs):
                resize_prev_img = extract_and_resize(prev_img[0], 
                                                    output_size=(200, 200))
                tmp_img.image(resize_prev_img)

        ## - Predict the selected glyphs and display result
        if detect_button:
            clear_session_state('zip_detect')

            for i, glyph in enumerate(st.session_state.preview_imgs):
                pred_res = classify_glyph(uploaded_file.name, img, 
                                    glyph[0], rects[i])

                # Resize the glyph for display result
                glyph_resize = extract_and_resize(glyph[0])
                st.session_state.zip_detect.append((glyph_resize, pred_res))

            tmp_img.empty()

        for i, result in enumerate(st.session_state.zip_detect):
            space()
            rowImgDet = row([0.3, 0.7], gap='small')

            rowImgDet.image(result[0])
            rowImgDet.write(f"""
                <p style='padding-top: 24px;
                        font-size: 20px;'>
                <b>
                    {result[1][0]}
                    <span style='margin-left: 16px;'>&nbsp;</span>
                    {result[1][1]} - {result[1][2]}
                </b>
                <span style='margin-left: 24px;'>&nbsp;</span>
                <em style='font-size: 16px;'>
                    ({result[1][3]}%)
                </em>
                </p>
                """, unsafe_allow_html=True)

        if save_button:
            ## - Clear preview to keep the result of the prediction
            clear_session_state('preview_imgs')
            tmp_img.empty()

            ## - Send the result to the API
            print("Save the result")

            save_inference(uploaded_file.name,
                           img,
                           rects,
                           st.session_state.zip_detect)

        # if correct_button:
        #     pass



## ------------------------------- ANNOTATION ------------------------------- ##

def annotate():
    print("Detecting")
    # im.save_annotation()
    # image_annotate_file_name = img_file_name.split(".")[0] + ".xml"
    # if image_annotate_file_name not in st.session_state["annotation_files"]:
    #     st.session_state["annotation_files"].append(image_annotate_file_name)
    # next_annotate_file()

def annotation(img_path):
    # if 'preview_imgs' not in st.session_state:
    #     st.session_state.preview_imgs = []

    # if 'res_label' not in st.session_state:
    #     st.session_state.res_detect = []

    # if 'zip_label' not in st.session_state:
    #     st.session_state.zip_detect = []

    labels = fct.postgres_execute_get_mzl()
    preview_imgs = []

    col1, col2 = st.columns(2)
    with col1:
        im = ImageManager(img_path)
        img = im.get_img()
        resized_img = im.resizing_img()
        resized_rects = im.get_resized_rects()
        rects = st_img_label(resized_img, box_color="red", rects=resized_rects)

        label_button = st.button(label="Labeled")

    with col2:
        preview_imgs = im.init_annotation(rects)

        rowImgDet = row(2, gap='medium')
        # tmp_img = st.empty()

        for i, prev_img in enumerate(preview_imgs):
            resize_prev_img = extract_and_resize(prev_img[0])

            rowImgDet.image(resize_prev_img)

            default_index = 0
            if prev_img[1]:
                default_index = labels.index(prev_img[1])

            select_label = rowImgDet.selectbox(
                "Label", labels, key=f"label_{i}", index=default_index
            )
            im.set_annotation(i, select_label)


## --------------------------------- SAVING --------------------------------- ##

def save_inference(img_name: str,
                   original_img: Image.Image, 
                   bbox_glyphs: list, 
                   pred_results: list) -> None:

    ## - Preprocess the data
    img_name = img_name.split(".")[0]  # Remove the extension
    binary_original_img = encode_image(original_img)

    for i, glyph in enumerate(pred_results):
        bbox_dict = bbox_glyphs[i]
        bbox = [
            bbox_dict['left'],  # x_min
            bbox_dict['top'],   # y_min
            bbox_dict['left'] + bbox_dict['width'], # x_max
            bbox_dict['top'] + bbox_dict['height']  # y_max
        ]
        mzl_number = pred_results[i][1][0]
        confidence = pred_results[i][1][3]

        print(confidence)
        data = {
            "img_name": img_name,
            "img": binary_original_img,
            "bbox": bbox,
            "mzl_number": mzl_number,
            "confidence": confidence
        }

        # print(data)

        res = requests.post(url=f"{API_URL}/prediction/saving_classification/", 
                            data=json.dumps(data))
        print(res.json())









## --------------------------- BACKUP OLD CODE  ------------------------------ ##
# def classify_glyph(img_name: str, img: Image.Image, 
#                   glyph_selection: Image.Image, bbox: list) -> list:
    """Send request to the API to detect the glyphs in the image.

    Parameters:
    - tablet_name (str): The name of the tablet
    - img (Image): The full image
    - glyph_selection (list): Image of the selected glyph (not resized)
    - bbox (list): List of dictionary (left, top, width, height, label)

    Returns:
    - res (str): The detected glyphs label
    """

    # print(tablet_name)
    # print(img)
    # print(glyph_selection)
    # print(bbox)

    ## - Load the model from MLflow
    # model = load_model()

    ## - Preprocess & Predict
    # img_preprocessed = glyphnet_img_preprocess(glyph_selection)
    # pred = model.predict(img_preprocessed)

    # pred_result = predicted_class(pred)
    # return pred_result

    ## - Preprocess the request and send it
    # img_name = img_name.split(".")[0]
    # for i, glyph in enumerate(glyph_selection):
    #     print(img_name)
    #     print(f"Glyph {i}: {glyph}")
    #     print(f"Box {i}: {bbox[i]}")
    #     # st.image(glyph[0])

    #     info_for_api = {"tablet_name": img_name,
    #                     "picture": img,
    #                     "glyph": glyph[0],
    #                     "bbox": bbox[i]}

    ## - Raw response for test the Front-End
    # res = "113: 𒁁, BAD -- 88.7%"

    # return res