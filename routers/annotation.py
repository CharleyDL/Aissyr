#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Friday 26 Apr. 2024
# ==============================================================================
# API ROUTES ANNOTATION
# ==============================================================================

import utils.database as db

from fastapi import APIRouter, HTTPException, Response, status
from fastapi.responses import JSONResponse, RedirectResponse
from psycopg2.errors import OperationalError

from utils.schemas import MessageAccount, SaveAnnotation


router = APIRouter()


## ------------------------ SAVE ANNOTATION GLYPHS -------------------------- ##

@router.post('/saving_annotation/', response_model=MessageAccount, 
            status_code=status.HTTP_200_OK)
async def save_annotation(payload: SaveAnnotation):
    try:
        ## - Save in tablet_ref
        id_tablet = db.save_in_tablet_ref(payload)

        ## - Save in reveal
        db.save_in_reveal(id_tablet)

        ## - Save in segment_ref
        id_segment = db.save_in_segment_ref(payload, id_tablet)

        ## - Save in annotation_ref
        res = db.save_in_annotation_ref(payload, id_segment)

        if not res:
            return MessageAccount(result=False,
                                  message=f"""
                                           {payload.mzl_number} with the bbox
                                           {payload.bbox_annotation} already 
                                           exists in database for 
                                           {payload.img_name}
                                           """,
                                  content=None)

        return MessageAccount(result=True,
                              message=f"""
                                       {payload.mzl_number} with the bbox
                                       {payload.bbox_annotation} has saved
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





# @router.get('/get_annotation/', response_model=List[Annotation], 
#             status_code=status.HTTP_200_OK)
# async def read_annotation():
#     try:
#         return select_annotation()
#     except OperationalError:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="""Check if the route exists, connection is successful 
#                        or database/tables exist."""
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f"""Error {e}"""
#         )
