#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Tuesday 16 Apr. 2024
# ==============================================================================
# API ROUTES ARCHIVES
# ==============================================================================

import utils.database as db

from fastapi import APIRouter, HTTPException, status
from psycopg2.errors import OperationalError

from utils.schemas import MessageAccount


router = APIRouter()


## ------------------------- ARCHIVE CLASSIFICATION ------------------------- ##

@router.get('/classification/', response_model=MessageAccount, 
            status_code=status.HTTP_200_OK)

async def archive_classification():
    try:
        result = db.get_archive_classifications()

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='No archive for classification found')
    
        return MessageAccount(result=True, 
                              message="Archive classification found", 
                              content=result)

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


## -------------------------- ARCHIVE LABELISATION -------------------------- ##

@router.get('/labelisation/', response_model=MessageAccount, 
            status_code=status.HTTP_200_OK)

async def archive_labelisation():
    try:
        result = db.get_archive_labelisation()

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='No archive for labelisation found')

        return MessageAccount(result=True, 
                              message="Archive labelisation found", 
                              content=result)

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
