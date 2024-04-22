#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Tuesday 16 Apr. 2024
# ==============================================================================
# API ROUTES ACCOUNT
# ==============================================================================

import utils.functions as fct
import utils.database as db

from fastapi import APIRouter, HTTPException, status
from psycopg2.errors import OperationalError

from utils.schemas import CreateAccount, MessageAccount, VerifyLogin


router = APIRouter()


## ---------------------------------- LOGIN --------------------------------- ##

@router.post('/verify_login/', response_model=MessageAccount, 
            status_code=status.HTTP_200_OK)
async def verify_login(payload: VerifyLogin):
    try:
        account_info = db.verify_user_account(payload.email)
        if account_info is None:
            return MessageAccount(result=False,
                message="Account not found", content=None)

        res = fct.verify_password_hash(account_info, payload.input_pwd)
        if not res:
            return MessageAccount(result=False, 
                message="Invalid password", content=None)

        del account_info['email']
        del account_info['pwd_hash']
        return MessageAccount(result=True, 
                              message="Login successful", 
                              content=account_info)

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


## ----------------------------- CREATE ACCOUNT ----------------------------- ##

@router.post('/create_account/', response_model=MessageAccount, 
             status_code=status.HTTP_201_CREATED)
async def create_account(payload: CreateAccount):
    try:
        res = db.create_account(payload)
        if not res:
            return MessageAccount(result=False, 
                                  message="Account already exists", 
                                  content=None)

        return MessageAccount(result=True, 
                              message="Account created successfully", 
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
