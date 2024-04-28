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

from io import BytesIO
from mlflow.pyfunc import PyFuncModel
from PIL import Image
from streamlit.runtime.uploaded_file_manager import UploadedFile
from streamlit_img_label import st_img_label
from streamlit_img_label.manage import ImageManager
from streamlit_extras.row import row


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


def disable_btns_detect_page() -> None:
    st.session_state.disable_btns_detect_page = not st.session_state.disable_btns_detect_page


def disable_btns_correct_page() -> None: 
    st.session_state.disable_btns_correct_page = not st.session_state.disable_btns_correct_page


def enable(state_key: str) -> None:
    st.session_state[state_key] = False


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


## --------------------------------- IMAGE --------------------------------- ##

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


## -------------------------------- MZL INFO -------------------------------- ##

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

    labels = [1, 10, 100]
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

def save_annotation(img_name: str,
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
