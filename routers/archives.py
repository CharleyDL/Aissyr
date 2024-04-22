#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Tuesday 16 Apr. 2024
# ==============================================================================
# API ROUTES ARCHIVES
# ==============================================================================

import utils.functions as fct
import utils.database as db

from fastapi import APIRouter, HTTPException, Response, status
from fastapi.responses import JSONResponse, RedirectResponse
from psycopg2.errors import OperationalError

from utils.schemas import MessageAccount, ClassifyRequest


router = APIRouter()


## ------------------------- ARCHIVE CLASSIFICATION ------------------------- ##

@router.get('/classification/', response_model=MessageAccount, 
            status_code=status.HTTP_200_OK)
async def classification(payload: ClassifyRequest):
    pass

## --------------------------- ARCHIVE ANNOTATIONS -------------------------- ##
@router.get('/annotation/', response_model=MessageAccount, 
            status_code=status.HTTP_200_OK)
async def annotation(payload: ClassifyRequest):
    pass
