import dagshub
import os

import utils.functions as fct
import utils.database as db

from fastapi import APIRouter, HTTPException, Response, status
from fastapi.responses import JSONResponse, RedirectResponse
from psycopg2.errors import OperationalError

from utils.schemas import MessageAccount, ClassifyRequest
import mlflow as mlf

router = APIRouter()


TRACKING_URI = os.getenv("TRACKING_URI")
# TRACKING_URI=f"https://dagshub.com/{DAGSHUB_REPO_OWNER}/{DAGSHUB_REPO}.mlflow"


## ------------------------- CLASSIFICATION GLYPHS -------------------------- ##


@router.get('/model/', response_model=MessageAccount, 
            status_code=status.HTTP_200_OK)
async def model():
    try:
        mlf.set_tracking_uri(TRACKING_URI)
        print(mlf.get_tracking_uri())
        mlflow_handler = fct.MLFlowHandler(mlf.get_tracking_uri())
        res = mlflow_handler.check_mlflow_health()
        return MessageAccount(result=True, message=res, content=None)

        # model = fct.MLFlowHandler(TRACKING_URI)
        # return MessageAccount(result=True, message=model, content=None)

    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="""Connection is bad"""
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"""Error {e}"""
        )


# @router.post('/classify_glyphs/', response_model=MessageAccount, 
#             status_code=status.HTTP_200_OK)
# async def classify_glyphs(payload: ClassifyRequest):
#     try:
#         res = fct.check_mlflow_health(TRACKING_URI)
#         return MessageAccount(result="MLFLOW", message=res, content=None)

#     except OperationalError:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="""Check if the database exists, connection is successful 
#             or tables  exist."""
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f"""Error {e}"""
#         )
