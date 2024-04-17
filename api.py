#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Saturday 23 Dec. 2023
# ==============================================================================
# API for the AISSYR project.
# ==============================================================================


import utils.functions as fct
import uvicorn

from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException

from routers import account, annotation


app = FastAPI(
    title="AISSYR API by Charley ∆. L.",
    summary="AISSYR API for the classification of assyrian glyphs",
    description="""This API is used to operate the AISSYR webapp toolbox.
    Among other things, it enables glyph prediction, inference posting and 
    retrieval, MZL glyph information retrieval..."""
)


## ---------------------------------- ROOT ---------------------------------- ##
@app.get("/")
async def root():
    return {"message": "Welcome to the AISSYR API"}

app.include_router(account.router, prefix='/account', tags=['account'])
app.include_router(annotation.router, prefix='/annotation', tags=['annotation'])




if __name__=='__main__':
    uvicorn.run(app, host='0.0.0.0', port=4000)