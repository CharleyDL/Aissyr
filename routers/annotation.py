#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Tuesday 16 Apr. 2024
# ==============================================================================
# API ROUTES ANNOTATION
# ==============================================================================

import utils.functions as fct
import utils.database as db

from typing import List
from fastapi import APIRouter, HTTPException, Response, status
from fastapi.responses import JSONResponse, RedirectResponse
from psycopg2.errors import OperationalError

from utils.schemas import Annotation


router = APIRouter()


## ------------------------ SAVE ANNOTATION GLYPHS -------------------------- ##

# @router.get('/get_annotation/', response_model=List[Annotation], 
#             status_code=status.HTTP_200_OK)
# async def read_annotation():
#     try:
#         return select_annotation()
#     except OperationalError:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="""Check if the database exists, connection is successful 
#             or tables exist. To create tables use '/initdb' endpoint"""
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f"""Error {e}"""
#         )
