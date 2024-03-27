import os

class TestRequiredElements:

    def test_folder_exists(self):
        required_folders = ['.streamlit', 'asset', 'pages', 
                            'streamlit_img_label', 'utils']
        for folder in required_folders:
            assert os.path.exists(folder)


    def test_file_exists(self):
        required_files = ['Home.py', 'requirements.txt', 
                          'asset/logo_landing.png', 'asset/logo_aissyr_S.png', 
                          'asset/logo_aissyr_M.png', 'asset/logo_aissyr_L.png', 
                          'pages/main_page.py', 'pages/login.py', 
                          'pages/register.py', 'pages/annotation.py',
                          'pages/archive.py', 'pages/detect.py']

        for file in required_files:
            assert os.path.exists(file)
