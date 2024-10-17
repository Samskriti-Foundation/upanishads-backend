from pydantic import BaseModel

from app.isha.routers.utils import Language


class SutraBase(BaseModel):
    number: int
    text: str


class SutraCreate(SutraBase):
    pass


class SutraOut(SutraBase):
    id: int


class SutraUpdate(SutraBase):
    pass


class MeaningBase(BaseModel):
    language: Language
    text: str
    sutra_id: int


class MeaningCreate(MeaningBase):
    pass


class MeaningOut(MeaningBase):
    id: int


class MeaningUpdate(MeaningBase):
    pass


class TransliterationBase(BaseModel):
    language: Language
    text: str
    sutra_id: int


class TransliterationCreate(TransliterationBase):
    pass


class TransliterationOut(TransliterationBase):
    id: int


class TransliterationUpdate(TransliterationBase):
    pass
