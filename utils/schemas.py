#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By   : Charley ∆. Lebarbier
# Date Created : Saturday 20 Apr. 2024
# ==============================================================================
# SCHEMAS FOR API
# ==============================================================================


from pydantic import Base64Bytes, RootModel, BaseModel
from typing import Dict


## -------------------------------- GENERAL --------------------------------- ##

class MessageAccount(BaseModel):
    result: bool
    message: str 
    content: dict | None


## -------------------------------- ACCOUNT --------------------------------- ##

class CreateAccount(BaseModel):
    title: str
    last_name: str
    first_name: str
    email: str
    password: str


class VerifyLogin(BaseModel):
    email: str
    input_pwd: str


## ------------------------------- ANNOTATION ------------------------------- ##

class SaveAnnotation(BaseModel):
    img_name: str
    img: Base64Bytes
    bbox_img: list[int]
    bbox_annotation: list[int]
    mzl_number: int


## -------------------------------- ARCHIVE --------------------------------- ##

class ImageData(BaseModel):
    img_name: str
    img: Base64Bytes


class GlyphData(BaseModel):
    bbox: list[int]
    mzl_number: int
    glyph: str
    glyph_name: str
    confidence: float


class ArchiveClassification(RootModel):
    root: dict[ImageData, GlyphData]

## ------------------------------ PREDICTION -------------------------------- ##

class SaveClassification(BaseModel):
    img_name: str
    img: Base64Bytes
    bbox: list[int]
    mzl_number: int
    confidence: float


## ------------------------------- RESOURCES -------------------------------- ##

class GlyphInfo(BaseModel):
    mzl_number: int
    glyph_name: str | None
    glyph: str | None
    glyph_phonetic: list[str] | None


class AllGlyphs(RootModel):
    root : Dict[int, GlyphInfo]
