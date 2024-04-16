from typing import List
from fastapi import APIRouter, HTTPException, Response, status
from fastapi.responses import JSONResponse, RedirectResponse
from psycopg2.errors import DatetimeFieldOverflow, OperationalError

from utils.database import select_annotation
from utils.schemas import Annotation


router = APIRouter()


# @router.post('/', response_model=NewsDB, status_code=status.HTTP_201_CREATED)
# async def create_news(payload: NewsSchema):
#     try:
#         res = select_annotation()
#         return res
#     except DatetimeFieldOverflow:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Formats are : month-day-year hour:minute:seconds or year-month-day hour:minute:seconds"
#         )


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