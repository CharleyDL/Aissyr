#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Wednesday 1 May 2024
# ==============================================================================

import os
import requests

from dotenv import load_dotenv


load_dotenv()


class TestAPIOnline:

    def test_api_online(url):
        url = os.getenv("API_URL")

        response = requests.get(url)
        assert response.status_code == 200, f"""Failed to connect to {url}. 
                                                Status code: {response.status_code}"""
        print(f"API at {url} is online.")
