
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Saturday 23 Dec. 2023
# ==============================================================================
# Script for web scraping cuneiform signs from the Neo-Assyrian period (900-600 BC)
# on the Electronic Babylonian Library (EBL) website, generating a JSON file with
# the following information: MZL Number, Sign Name, Glyph, and Sign Phonetic.
# ==============================================================================



import chromedriver_autoinstaller
import json
import re
import time

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm


chromedriver_autoinstaller.install()
chrome_options = Options()
chrome_options.add_argument("--headless")


URL_EBL = "https://www.ebl.uni-muenchen.de/signs?listsName=MZL&listsNumber={}"
PATH_JSON_SAVE = "data/neo_assyrien_info.json"

mzl_not_found = []


def dict_to_json(dict_to_convert: dict, output_file_path: str) -> None:
    with open(output_file_path, "w", encoding='utf-8') as outfile:
        json.dump(dict_to_convert, outfile, indent=4, ensure_ascii=False)
        outfile.write('\n')


def get_name(html_content: str, data_dict: dict) -> None:
    glyph_name = html_content.find('dfn', 
        {'class': 'signs__sign__name mx-2'}).text.strip()
    data_dict['name'] = glyph_name


def get_glyph(html_content: str, data_dict: dict) -> None:
    glyph = html_content.find('span', 
        {'class': 'signs__sign__cuneiform'}).text.strip()
    data_dict['glyph'] = glyph


def get_phonetics(html_content: str, data_dict: dict) -> None:
    ## - Get all content of the page because phonetic have two parts of which 
    ## - one without tag
    all_content = html_content.find('div', class_='signs__sign').text.strip()
    glyph_phonetics = re.findall(r'\b(?!MZL\b)[a-zA-Z₀₁₂₃₄₅₆₇₈₉]+\b',
                                 all_content)
    data_dict['phonetic'] = glyph_phonetics


def get_information_url(mzl_number: int) -> dict:
    """
    Extracts information about a cuneiform sign from the Electronic Babylonian 
    Library (EBL) website.

    Parameter:
    ----
    - mzl_number (int, required): The MZL number of the cuneiform sign.

    Return:
    ----
    - data_dict (dict): A dictionary containing information about the cuneiform sign,
                       including MZL Number, Sign Name, Glyph, and Sign Phonetic.

    >>> get_information_url(2)
    >>> return => data_dict["mzl_number": 2, "name": "AŠ.AŠ", "glyph": "𒀸𒀸", 
            "phonetic": ["didli", "man₃", "min₅"]]
    """
    data_dict = {'mzl_number': mzl_number}

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(URL_EBL.format(mzl_number))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 
                                                                        'signs__sign')))
        html_source = driver.page_source
        page_content = bs(html_source, 'html.parser')

        get_name(page_content, data_dict)
        get_glyph(page_content, data_dict)
        get_phonetics(page_content, data_dict)
    except Exception as e:
        mzl_not_found.append(mzl_number)
        print(f"MZL {mzl_number} doesn't exist\
              \n ou erreur : {e}")

    driver.close()
    return data_dict




if __name__ == "__main__":
    list_of_dicts = []

    for mzl_number in tqdm(range(1, 908, 1)):
        data_dict = get_information_url(mzl_number)
        list_of_dicts.append(data_dict)
        time.sleep(2)

    dict_to_json(list_of_dicts, PATH_JSON_SAVE)
    print(mzl_not_found)

    # print(data_dict)