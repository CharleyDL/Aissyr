#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Friday 19 Apr. 2024
# ==============================================================================
# API ROUTES PREDICTION
# ==============================================================================

import utils.database as db

from datetime import date
from fastapi import APIRouter, HTTPException, status
from psycopg2.errors import OperationalError

from utils.schemas import MessageAccount, SaveClassification


router = APIRouter()


# ---------------------- SAVE CLASSIFICATION GLYPHS ------------------------ ##

@router.post('/saving_classification/', response_model=MessageAccount, 
            status_code=status.HTTP_200_OK)
async def save_classification(payload: SaveClassification):
    try:

        ## - Check if the img_name already exists in the database
        id_inference = db.check_img_name(payload.img_name)

        if not id_inference:
            ## - Save in tablet_infrn
            date_infrn = date.today().strftime('%Y-%m-%d')
            id_inference = db.save_in_tablet_name(payload, date_infrn)

        ## - Save in infrn_result
        res = db.save_in_infrn_result(payload, id_inference)

        if not res:
            return MessageAccount(result=False, 
                                  message=f"""
                                           {payload.mzl_number} with
                                           {payload.confidence}% already exists
                                           in database for {payload.img_name}
                                           """, 
                                  content=None)

        return MessageAccount(result=True, 
                              message=f"""
                                       {payload.mzl_number} with
                                       {payload.confidence}% has saved 
                                       successfully""", 
                              content=None)

    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="""Check if the route exists, connection is successful 
            or database/tables exist."""
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"""Error {e}"""
        )
