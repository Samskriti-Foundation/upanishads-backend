from pydantic import BaseModel


class SutraBase(BaseModel):
    number: int
    text: str


class SutraCreate(SutraBase):
    pass


class SutraOut(SutraBase):
    id: int


class SutraUpdate(SutraBase):
    id: int
