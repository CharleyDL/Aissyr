import utils.functions as fct

from typing import List
from fastapi import APIRouter, HTTPException, Response, status
from fastapi.responses import JSONResponse, RedirectResponse
from psycopg2.errors import DatetimeFieldOverflow, OperationalError

from utils.database import select_annotation, verify_user_account
from utils.schemas import Account, Annotation, Verify

router = APIRouter()


## -------------------------------- ACCOUNT --------------------------------- ##
@router.get('/verify/', response_model=Verify, status_code=status.HTTP_200_OK)
async def verify_account(email: str, input_pwd: str):
    try:
        account_info = verify_user_account(email)
        if account_info is None:
            return Verify(result=False, message="Account not found")

        res = fct.verify_password_hash(account_info, input_pwd)
        if not res:
            return Verify(result=False, message="Invalid password")
        return Verify(result=True, message="Account verified")



    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="""Check if the database exists, connection is successful 
            or tables  exist."""
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"""Error {e}"""
        )



## ------------------------------ ANNOTATION -------------------------------- ##


@router.get('/', response_model=List[Annotation], status_code=status.HTTP_200_OK)
async def read_annotation():
    try:
        return select_annotation()
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="""Check if the database exists, connection is successful 
            or tables exist. To create tables use '/initdb' endpoint"""
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"""Error {e}"""
        )