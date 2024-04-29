import os

class TestRequiredElements:

    def test_folder_exists(self):
        required_folders = ['.streamlit', 'asset', 'pages', 
                            'streamlit_img_label', 'utils']
        for folder in required_folders:
            assert os.path.exists(folder)


    def test_file_exists(self):
        required_files = ['asset/icn_save.png', 'asset/icn_shield.png',
                          'asset/logo_landing.png', 'asset/logo_aissyr_S.png', 
                          'asset/logo_aissyr_M.png', 'asset/logo_aissyr_L.png', 
                          'pages/annotation_page.py', 'pages/archive.py',
                          'pages/correct_label.py', 'pages/detect_page.py',
                          'pages/error401.py', 'pages/login.py', 
                          'pages/main_page.py', 'pages/register.py',
                          'pages/save_result.py', 'pages/select_label.py',
                          'utils/functions.py', 'streamlit_img_label/',
                          'Home.py', 'requirements.txt', 
                          '.streamlit/config.toml',
                         ]

        for file in required_files:
            assert os.path.exists(file)
