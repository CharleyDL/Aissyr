#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Tuesday 19 Apr. 2024
# ==============================================================================

import base64
import dagshub
import json
import matplotlib.pyplot as plt
import mlflow.pyfunc
import numpy as np
import os
import re
import requests
import streamlit as st

from io import BytesIO
from mlflow.pyfunc import PyFuncModel
from PIL import Image
from streamlit_extras.row import row
from streamlit_img_label import st_img_label
from streamlit_img_label.manage import ArchiveImageManager, ImageManager
from streamlit.runtime.uploaded_file_manager import UploadedFile
from typing import Any, Dict, List, Tuple


API_URL = os.getenv("API_URL")
DAGSHUB_REPO_OWNER = os.getenv("DAGSHUB_REPO_OWNER")
DAGSHUB_REPO = os.getenv("DAGSHUB_REPO")
MODEL_URI = os.getenv("MODEL_URI")


## --------------------------- STREAMLIT UTILITIES -------------------------- ##

def button_del_page() -> None:
    st.markdown("""
    <style>
    [data-testid="baseButton-secondary"] {
        display: block;
        margin-top: 29px;
    }
    </style>
    """, unsafe_allow_html=True)


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
    Clear the session state for list key only

    Special case:
    ----
    Using on zip_detection : avoid duplicate when new detection.
    The rects saved the selection so we don't lose the information.
    """
    st.session_state[key] = []


def disable(state_key: str) -> None:
    st.session_state[state_key] = True


def disable_btns_correct_page() -> None: 
    st.session_state.disable_btns_correct_page = not st.session_state.disable_btns_correct_page


def disable_btns_detect_page() -> None:
    st.session_state.disable_btns_detect_page = not st.session_state.disable_btns_detect_page


def disable_btns_save() -> None: 
    st.session_state.disable_btns_save = not st.session_state.disable_btns_save


def enable(state_key: str) -> None:
    st.session_state[state_key] = False


def is_valid_email(email):
    # Expression régulière pour vérifier le format de l'e-mail
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(regex, email) is not None


def logout() -> None:
    """Log out the user and redirect to the home page."""
    st.session_state.pop('f_name')
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


## --------------------------------- IMAGE --------------------------------- ##

def decode_image(encoded_img: str) -> Image.Image:
    """
    Decodes a base64 encoded image string to a PIL image.

    Args:
    ----
        encoded_img (str): The base64 encoded image string.

    Returns:
    ----
        Image.Image: The decoded PIL image.
    """
    decoded_img = base64.b64decode(encoded_img)
    # image = Image.open(BytesIO(decoded_img))
    # return image
    return decoded_img


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


def plot_boxes_on_image(image: Image.Image, 
                        rects: List[Tuple[int, int, int, int]],
                        figsize: Tuple[int, int] = (10, 10)) -> plt.Figure:
    """
    Plot bounding boxes on the input image.

    Args:
    -----
        image (PIL.Image.Image): The input image.
        rects (List[Tuple[int, int, int, int]]): List of tuples representing bounding boxes. 
            Each tuple contains (left, top, right, bottom) coordinates of the bounding box.
        figsize (Tuple[int, int], optional): Size of the matplotlib figure. 
            Defaults to (10, 10).

    Returns:
    -------
        plt.Figure: The matplotlib figure containing the plotted image with bounding boxes.
    """

    image_array = np.array(image)

    fig, ax = plt.subplots(figsize=figsize)
    ax.imshow(image_array)

    for rect in rects:
        left, top, width, height = (rect[0], rect[1], 
                                    rect[2] - rect[0], 
                                    rect[3] - rect[1])
        rect_patch = plt.Rectangle((left, top), width, height, 
                                   fill=False, edgecolor='red', linewidth=2)
        ax.add_patch(rect_patch)

    ax.axis('off')
    return fig


def resizing_img_ratio(img, max_height=300, max_width=300):
        """resizing the image by max_height and max_width.

        Args:
            max_height(int): the max_height of the frame.
            max_width(int): the max_width of the frame.
        Returns:
            resized_img(PIL.Image): the resized image.
        """
        resized_img = img.copy()
        if resized_img.height > max_height:
            ratio = max_height / resized_img.height
            resized_img = resized_img.resize(
                (int(resized_img.width * ratio), int(resized_img.height * ratio))
            )
        if resized_img.width > max_width:
            ratio = max_width / resized_img.width
            resized_img = resized_img.resize(
                (int(resized_img.width * ratio), int(resized_img.height * ratio))
            )

        # resized_ratio_w = img.width / resized_img.width
        # resized_ratio_h = img.height / resized_img.height
        return resized_img


## -------------------------------- MZL INFO -------------------------------- ##

@st.cache_data(show_spinner=False)
def all_mzl_info(choice: str='dict') -> dict:
    """
    Get the all mzl resources from the database.

    Returns:
    -------
        dict: A dictionary containing all MZL glyphs and their info :
        mzl_number, glyph_name, glyph (get phonetic but no return it))
    """
    res = requests.get(url=f"{API_URL}/resources/glyphs/")
    res_dict = res.json()

    mzl_dict_format = {}
    for key, value in res_dict.items():
        mzl_dict_format[key] = {
            'mzl_number': value['mzl_number'],
            'glyph': value['glyph'],
            'glyph_name': value['glyph_name']
         }

    mzl_list_format = []
    for key, value in res_dict.items():
        mzl_number = value['mzl_number']
        glyph = value['glyph']
        glyph_name = value['glyph_name']

        formatted_string = f"{mzl_number} {glyph} - {glyph_name}"

        mzl_list_format.append(formatted_string)

    if choice == 'list':
        return mzl_list_format
    else:
        return mzl_dict_format


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



## --------------------------------- ARCHIVES ------------------------------- ##

def display_archives_classification(detection_dict: Dict[str, dict]) -> None:
    """
    Display the archives classification.

    Args:
    -----
        detection_dict (Dict[str, dict]): A dictionary containing the classification data.
            Each key is a category and the corresponding value is a dictionary containing 
            the information for that category.
    """
    for key, value in detection_dict.items():
            expander = st.expander(f"**{key}**")

            with expander:
                cols = st.columns([2, 3])

                ## - LEFT - Display artefact and bbox
                with cols[0]:
                    # - Initiate the image
                    decoded_img = decode_image(value['picture'])
                    im = ArchiveImageManager(decoded_img)
                    img = im.get_img()

                    # - Get all glyph bbox 
                    all_rects = []
                    for i, glyph in enumerate(value['glyphs_data']):
                        all_rects.append(glyph[0])

                    st.pyplot(plot_boxes_on_image(img, all_rects))

                ## - RIGHT - Display information
                with cols[1]:
                    for i, glyph in enumerate(value['glyphs_data']):
                        rowGlyphs = row([0.2, 0.2, 0.5], gap='small')
                        rowGlyphs.empty()

                        # - Display the glyph image
                        glyph_bbox = glyph[0]
                        resized_bbox = im._resize_rect({
                            "left": glyph_bbox[0],
                            "top": glyph_bbox[1],
                            "width": glyph_bbox[2] - glyph_bbox[0],
                            "height": glyph_bbox[3] - glyph_bbox[1]
                        })
                        glyph_img, _ = im._chop_box_img(resized_bbox)
                        resize_glyph_img = extract_and_resize(glyph_img, 
                                                        output_size=(100, 100))
                        rowGlyphs.image(resize_glyph_img)

                        # - Display glyph information
                        rowGlyphs.write(f"""
                        <p style='padding-top: 24px;
                                font-size: 20px;'>
                        <b>
                            <span style='margin-left: 16px;'>&nbsp;</span>
                            {glyph[2]} : {glyph[1]} - {glyph[3]}
                        </b>
                        <span style='margin-left: 24px;'>&nbsp;</span>
                        <em style='font-size: 16px;'>
                            Confiance: {glyph[4]}%
                        </em>
                        </p>
                        """, unsafe_allow_html=True)


def display_archives_labelisation(labelisation_dict: Dict[str, dict]) -> None:
    """
    Display the archives labelisation.

    Args:
    ----
        - labelisation_dict (Dict[str, dict]): A dictionary containing 
                the labelisation data. Each key is a category and the 
                corresponding value is a dictionary containing the information 
                for that category.
    """
    for key, value in labelisation_dict.items():
            expander = st.expander(f"**{key}**")

            with expander:
                cols = st.columns([2, 3])

                ## - LEFT - Display artefact and bbox
                with cols[0]:
                    # - Initiate the image
                    decoded_img = decode_image(value['picture'])
                    im = ArchiveImageManager(decoded_img)
                    img = im.get_img()

                    # - Get all glyph bbox 
                    all_rects = []
                    for i, glyph in enumerate(value['glyphs_data']):
                        all_rects.append(glyph[0])

                    st.pyplot(plot_boxes_on_image(img, all_rects))

                ## - RIGHT - Display information
                with cols[1]:
                    for i, glyph in enumerate(value['glyphs_data']):
                        rowGlyphs = row([0.2, 0.2, 0.5], gap='small')
                        rowGlyphs.empty()

                        # - Display the glyph image
                        glyph_bbox = glyph[0]
                        resized_bbox = im._resize_rect({
                            "left": glyph_bbox[0],
                            "top": glyph_bbox[1],
                            "width": glyph_bbox[2] - glyph_bbox[0],
                            "height": glyph_bbox[3] - glyph_bbox[1]
                        })
                        glyph_img, _ = im._chop_box_img(resized_bbox)
                        resize_glyph_img = extract_and_resize(glyph_img, 
                                                        output_size=(100, 100))
                        rowGlyphs.image(resize_glyph_img)

                        # - Display glyph information
                        rowGlyphs.write(f"""
                        <p style='padding-top: 24px;
                                font-size: 20px;'>
                        <b>
                            <span style='margin-left: 16px;'>&nbsp;</span>
                            {glyph[2]} : {glyph[1]} - {glyph[3]}
                        </b>
                        </p>
                        """, unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def get_archives_classification() -> Dict[str, Any]:
    """
    Retrieve the archives classification data from the API.

    Returns:
        Dict[str, Any]: A dictionary containing the classification data.
            Each key is a category and the corresponding value is the information
            for that category.
    """
    res = requests.get(url=f"{API_URL}/archives/classification/")
    # print(res.json())
    res_json = res.json()
    return res_json['content']


@st.cache_data(show_spinner=False)
def get_archives_labelisation() -> Dict[str, Any]:
    """
    Retrieve the archives labelisation data from the API.

    Returns:
        Dict[str, Any]: A dictionary containing the classification data.
            Each key is a category and the corresponding value is the information
            for that category.
    """
    res = requests.get(url=f"{API_URL}/archives/labelisation/")
    # print(res.json())
    res_json = res.json()
    return res_json['content']


## -------------------------- GLYPHS CLASSIFICATION ------------------------- ##

def classify_glyph(glyph_selection: Image.Image) -> list:
    """Send request to the API to detect the glyphs in the image.

    Parameters:
    ----------
    - glyph_selection (list): Image of the selected glyph (not resized)

    Returns:
    -------
    - pred_result (Image): The detected glyphs label
    """

    ## - Load the model from MLflow
    model = load_model()

    ## - Preprocess & Predict
    img_preprocessed = glyphnet_img_preprocess(glyph_selection)
    pred = model.predict(img_preprocessed)
    pred_result = predicted_class(pred)

    return pred_result


def classification_setup(uploaded_file: UploadedFile) -> None:
    """
    Sets up the classification interface for detecting, saving labels, 
    and correcting labels.

    Displays buttons for detecting, saving labels, and correcting labels. 

    Clears the session states 'correct_label' and 'del_label'. 
    Enables or disables the detection button based on the presence
    of rectangles.

    - If the 'detect' button is clicked, it clears the session state 
    'zip_detect', classifies the selected glyphs, and displays the results. 

    - If the 'save' button is clicked, it sends the results to the API for 
    saving and displays the corresponding message.

    - If the 'correct' button is clicked, it switches to the correct_label page.

    Args:
    ----
        uploaded_file (streamlit UploadedFile): The uploaded file containing 
        the image to be classified.
    """

    button_detect_page()

    clear_session_state('correct_label')
    clear_session_state('del_label')

    col1, col2 = st.columns(2)
    with col1:
        im = ImageManager(uploaded_file)
        img = im.get_img()
        resized_img = im.resizing_img()
        resized_rects = im.get_resized_rects()
        rects = st_img_label(resized_img, box_color="red", rects=resized_rects)

        if rects:       # Enable/Disable detect
            enable('disabled_detect')

        else:
            clear_session_state('zip_detect')
            disable('disabled_detect')
            disable('disable_btns_detect_page')

        ## - Button row for detect, save and correct
        rowOption = row(3, gap='small')
        detect_button = rowOption.button(label="Detect",
                                         on_click=disable_btns_detect_page,
                                         disabled=st.session_state.disabled_detect)
        save_button = rowOption.button(label="Save Label", key="save_detect_page",
            disabled=st.session_state.disable_btns_detect_page)
        correct_button = rowOption.button(label="Correct Label",
            disabled=st.session_state.disable_btns_detect_page)

    with col2:
        space()

        rowImgDet = row([0.3, 0.7], gap='small')

        _cL, colC, _cR = st.columns([1,4,1])
        with colC:
            tmp_img = st.empty()

        ## - Display the glyph preview for selection
        st.session_state.preview_imgs = im.init_annotation(rects) 
        if st.session_state.preview_imgs:
            for i, prev_img in enumerate(st.session_state.preview_imgs):
                resize_prev_img = extract_and_resize(prev_img[0], 
                                                     output_size=(200, 200))
                tmp_img.image(resize_prev_img)
                clear_session_state('rects_detect')

        st.session_state.rects_detect = rects

        ## - Predict the selected glyphs and display result
        if detect_button:
            clear_session_state('zip_detect')

            for i, glyph in enumerate(st.session_state.preview_imgs):
                pred_res = classify_glyph(glyph[0])

                # Resize the glyph for display result
                glyph_resize = extract_and_resize(glyph[0])
                st.session_state.zip_detect.append((glyph_resize, pred_res))

            tmp_img.empty()

            for i, result in enumerate(st.session_state.zip_detect):
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

        ## - Save the prediction in database
        if save_button:
            ## - Clear preview to keep the result of the prediction
            clear_session_state('preview_imgs')
            tmp_img.empty()

            ## - Send the result to the API and display the message
            results = save_inference(uploaded_file.name,
                                     img,
                                     rects,
                                     st.session_state.zip_detect)

            for i, result in enumerate(results):
                if result['result']:
                     st.toast(result['message'], icon='✅')
                else:
                    st.toast(result['message'], icon='🚫')

        if correct_button:
            st.switch_page("pages/correct_label.py")


def correct_label() -> None:
    """
    Moves correctly labeled items from the zip_detect list to the 
    correct_label list in the session state.

    Iterates through the zip_detect list in the session state. 
    If an item in the list has a length of 3, indicating that it's correctly 
    labeled, it appends the item to the correct_label list and removes it
    from the zip_detect list.
    """
    for i, value in enumerate(st.session_state.zip_detect):
        if len(value[1]) == 3:   # - if % not in the list means it's corrected
            ## - Prepare the correct label and its bbox
            st.session_state.correct_label.append(value)
            st.session_state.rects_correct.append(st.session_state.rects_detect[i])

            ## - Remove the corrected label and bbox
            del st.session_state.zip_detect[i]
            del st.session_state.rects_detect[i]


def del_unknow_glyphs(index) -> None:
    """
    Deletes the correctly labeled glyph and its corresponding bounding box 
    from the session state lists.

    Args:
    ----
        index (int): The index of the correctly labeled glyph to be deleted 
                     from the lists.
    """
    del st.session_state.zip_detect[index]
    del st.session_state.rects_detect[index]


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


def update_zip_detect(index: int) -> None:
    """
    Update the list of zip_detect predictions in the session by replacing 
    the prediction at the specified index with the new prediction selected 
    by the user.

    Args:
    ----
    - index (int): The index of the item to update in the zip_detect list.
    """
    value = st.session_state[f"label_{index}"]
    new_label = int(value.split(" ")[0])

    if new_label != st.session_state.zip_detect[index][1][0]:
        mzl_information = mzl_info(new_label)
        correct_glyph = [
            mzl_information['mzl_number'],
            mzl_information['glyph'],
            mzl_information['glyph_name'],
        ]

    updated_zip_detect = st.session_state.zip_detect
    updated_zip_detect[index] = (updated_zip_detect[index][0], correct_glyph)

    clear_session_state('zip_detect')
    st.session_state.zip_detect = updated_zip_detect
    correct_label()


## ---------------------------- GLYPHS LABELISATION ------------------------- ##

def labelisation_setup(uploaded_file: UploadedFile) -> None:
    """
    Set up annotation interface for the uploaded file.

    Args:
    ----
    - uploaded_file (UploadedFile): The uploaded image file.
    """
    col1, col2 = st.columns(2)
    with col1:
        im = ImageManager(uploaded_file)
        img = im.get_img()
        resized_img = im.resizing_img()
        resized_rects = im.get_resized_rects()
        rects = st_img_label(resized_img, box_color="red", rects=resized_rects)

        if rects:       # Enable/Disable Label button
            enable('disabled_detect')

        ## - Button row for save
        rowOption = row(3, gap='small')
        label_button = rowOption.button(label="Label", 
                                       key="label_button",
                                       disabled=st.session_state.disabled_detect)

    with col2:
        space()

        _cL, colC, _cR = st.columns([1,4,1])
        with colC:
            tmp_img = st.empty()

        ## - Display the glyph preview for selection
        st.session_state.preview_imgs = im.init_annotation(rects) 
        if st.session_state.preview_imgs:
            for i, prev_img in enumerate(st.session_state.preview_imgs):
                resize_prev_img = extract_and_resize(prev_img[0], 
                                                     output_size=(200, 200))
                tmp_img.image(resize_prev_img)
                clear_session_state('rects_annotation')

        st.session_state.rects_annotation = rects

        if label_button:
            clear_session_state('zip_labelisation')

            for i, glyph in enumerate(st.session_state.preview_imgs):
                glyph_resize = extract_and_resize(glyph[0])
                st.session_state.zip_labelisation.append((glyph_resize, 
                                                          None))

            st.switch_page("pages/select_label.py")


def update_labelisation(index: int) -> None:
    """
    Update the list of zip_labelisation predictions in the session by replacing 
    the prediction at the specified index with the new prediction selected 
    by the user.

    Args:
    ----
    - index (int): The index of the item to update in the zip_labelisation list.
    """
    value = st.session_state[f"label_{index}"]
    if value:
        new_label = int(value.split(" ")[0])
        mzl_information = mzl_info(new_label)
        correct_glyph = [
            mzl_information['mzl_number'],
            mzl_information['glyph'],
            mzl_information['glyph_name'],
        ]

    updated_zip_labelisation = st.session_state.zip_labelisation
    updated_zip_labelisation[index] = (updated_zip_labelisation[index][0], 
                                       correct_glyph)

    clear_session_state('zip_labelisation')
    st.session_state.zip_labelisation = updated_zip_labelisation


## --------------------------------- SAVING --------------------------------- ##

def save_labelisation(img_name: str,
                    original_img: Image.Image,
                    bbox_img: list,
                    bbox_glyphs: list, 
                    annotations: list) -> list[dict]:
    """
    Save annotation to the server

    Args:
    ----
    img_name (str): The name of the image.
    original_img (PIL.Image.Image): The original image.
    bbox_img (list): A list containing the bounding box coordinates of 
                     the entire image.
    bbox_glyphs (list): A list containing dictionaries with bounding box 
                        coordinates for each glyph.
    annotations (list): A list of annotations.

    Returns:
    --------
    list[dict]: A list of dictionaries containing the results of the 
                annotation saving process.
    """
    results = []

    ## - Preprocess the data
    img_name = img_name.split(".")[0]  # Remove the extension
    binary_original_img = encode_image(original_img)

    for i, glyph in enumerate(annotations):
        bbox_dict = bbox_glyphs[i]
        bbox_annotation = [
            bbox_dict['left'],  # x_min
            bbox_dict['top'],   # y_min
            bbox_dict['left'] + bbox_dict['width'], # x_max
            bbox_dict['top'] + bbox_dict['height']  # y_max
        ]
        mzl_number = annotations[i][1][0]

        data = {
            "img_name": img_name,
            "img": binary_original_img,
            "bbox_img": bbox_img,
            "bbox_annotation": bbox_annotation,
            "mzl_number": mzl_number
        }

        print(data)
        res = requests.post(url=f"{API_URL}/annotation/saving_annotation/", 
                            data=json.dumps(data))

        print(res.json())
        results.append(res.json())

    return results


def save_inference(img_name: str,
                   original_img: Image.Image, 
                   bbox_glyphs: list, 
                   pred_results: list) -> list[dict]:

    """
    Save inference results to the server.

    Args:
    -----
        img_name (str): The name of the image.
        original_img (PIL.Image.Image): The full image (not the glyph).
        bbox_glyphs (list): List of dictionaries containing 
                            bounding box information for glyphs.
        pred_results (list): List of prediction results.

    Returns:
    --------
        list[dict]: A list containing all dictionary containing 
        for each glyph response from the server.
    """

    results = []

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

        data = {
            "img_name": img_name,
            "img": binary_original_img,
            "bbox": bbox,
            "mzl_number": mzl_number,
            "confidence": confidence
        }

        res = requests.post(url=f"{API_URL}/prediction/saving_classification/", 
                            data=json.dumps(data))
        print(res.json())
        results.append(res.json())

    return results
