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

from fastapi import FastAPI


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

## --------------------------------- DETECT --------------------------------- ##

# @app.post("/detect", response_model=fct.DetectionResponse, 
#         summary="Classify glyph from an image")
# def detect_glyph(request: fct.DetectionRequest):
#     return fct.detect_glyph(request)
    # return {"message": "Detecting glyph from image"}




if __name__=='__main__':
    uvicorn.run(app, host='0.0.0.0', port=4000)