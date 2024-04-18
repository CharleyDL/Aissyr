from pydantic import RootModel, BaseModel
from typing import Dict

## ------------------------------- GENERAL ---------------------------------- ##

class MessageAccount(BaseModel):
    result: bool
    message: str 
    content: dict | None


## ------------------------------- ACCOUNT ---------------------------------- ##

class CreateAccount(BaseModel):
    title: str
    last_name: str
    first_name: str
    email: str
    password: str


class VerifyLogin(BaseModel):
    email: str
    input_pwd: str


## ----------------------------- ANNOTATION --------------------------------- ##

class Annotation(BaseModel):
    id_annotation: int
    bbox: str
    relative_bbox: str
    mzl_number: int
    id_segment: int


## ----------------------------- PREDICTION --------------------------------- ##

class ClassifyRequest(BaseModel):
    image: str


## ------------------------------ RESOURCES --------------------------------- ##

class GlyphInfo(BaseModel):
    mzl_number: int
    glyph_name: str | None
    glyph: str | None
    glyph_phonetic: list[str] | None


class AllGlyphs(RootModel):
    root : Dict[int, GlyphInfo]
