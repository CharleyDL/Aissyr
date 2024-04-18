import utils.database as db

from fastapi import APIRouter, HTTPException, Response, status
from fastapi.responses import JSONResponse, RedirectResponse
from psycopg2.errors import OperationalError

from utils.schemas import AllGlyphs, GlyphInfo


router = APIRouter()


## --------------------------------- MZL REF -------------------------------- ##

@router.get('/glyphs/', 
            response_model=AllGlyphs, status_code=status.HTTP_200_OK)
async def all_glyphs():
    result = db.select_all_glyphs()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='No glyphs found')
    return result




@router.get('/glyphs/{mzl_number}/', 
            response_model=GlyphInfo, status_code=status.HTTP_200_OK)
async def glyphs_by_mzl_number(mzl_number: int):
    result = db.select_glyph_by_mzl(mzl_number)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Glyph {mzl_number} not found'
        )
    return result
