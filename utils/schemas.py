from pydantic import BaseModel, Field


class Verify(BaseModel):
    result: bool
    message: str

class Account(BaseModel):
    email: str
    pwd_hash: str

class Annotation(BaseModel):
    id_annotation: int
    bbox: str
    relative_bbox: str
    mzl_number: int
    id_segment: int