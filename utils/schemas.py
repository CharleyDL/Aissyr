from pydantic import BaseModel, Field

class Annotation(BaseModel):
    id_annotation: int
    bbox: str
    relative_bbox: str
    mzl_number: int
    id_segment: int