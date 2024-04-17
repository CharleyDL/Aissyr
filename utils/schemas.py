from pydantic import BaseModel, Field


class MessageAccount(BaseModel):
    result: bool
    message: str 
    content: dict | None


class VerifyLogin(BaseModel):
    email: str
    input_pwd: str


class CreateAccount(BaseModel):
    title: str
    last_name: str
    first_name: str
    email: str
    pwd_hash: str


class Annotation(BaseModel):
    id_annotation: int
    bbox: str
    relative_bbox: str
    mzl_number: int
    id_segment: int