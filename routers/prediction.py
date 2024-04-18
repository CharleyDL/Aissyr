import utils.functions as fct
import utils.database as db

from fastapi import APIRouter, HTTPException, Response, status
from fastapi.responses import JSONResponse, RedirectResponse
from psycopg2.errors import OperationalError

from utils.schemas import MessageAccount, ClassifyRequest

router = APIRouter()




## ---------------------- SAVE CLASSIFICATION GLYPHS ------------------------ ##

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
