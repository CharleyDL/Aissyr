#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Tuesday 16 Apr. 2024
# ==============================================================================
# API for the AISSYR project.
# ==============================================================================

import uvicorn

from fastapi import FastAPI

from routers import account, annotation, archives, prediction, resources


app = FastAPI(
    title="AISSYR API by Charley ∆. L.",
    summary="AISSYR API for the classification of assyrian glyphs",
    description="""This API is used to operate the AISSYR webapp toolbox.
    Among other things, it enables glyph prediction, inference posting and 
    retrieval, MZL glyph information retrieval..."""
)


## ----------------------------- ROOT & ROUTES ------------------------------ ##

@app.get("/")
async def root():
    return {"message": "Welcome to the AISSYR API"}

app.include_router(account.router, prefix='/account', tags=['account'])
app.include_router(annotation.router, prefix='/annotation', tags=['annotation'])
app.include_router(archives.router, prefix='/archives', tags=['archives'])
app.include_router(prediction.router, prefix='/prediction', tags=['prediction'])
app.include_router(resources.router, prefix='/resources', tags=['resources'])




if __name__=='__main__':
    uvicorn.run(app, host='0.0.0.0', port=4000)
