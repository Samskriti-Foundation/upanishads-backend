from pydantic import BaseModel

from app.utils import Language, Philosophy
from app.schemas import Project


class SutraBase(BaseModel):
    id: int = None  # Make id optional
    chapter: int
    number: int
    text: str


class SutraCreate(SutraBase):
    pass


class SutraOut(SutraBase):
    id: int
class SutraListOut(BaseModel):
    id: int
    number: int
class SutraUpdate(SutraBase):
    pass
class Sutra(SutraBase):
    id: int
    project: Project
    class Config:
        orm_mode = True

class MeaningBase(BaseModel):
    language: Language
    text: str
class MeaningCreate(MeaningBase):
    pass
class MeaningOut(MeaningBase):
    id: int
class MeaningUpdate(MeaningBase):
    pass
class Meaning(MeaningBase):
    id: int
    sutra: Sutra
    class Config:
        orm_mode = True

class TransliterationBase(BaseModel):
    language: Language
    text: str
class TransliterationCreate(TransliterationBase):
    pass
class TransliterationOut(TransliterationBase):
    id: int
class TransliterationUpdate(TransliterationBase):
    pass
class Transliterations(TransliterationBase):
    id: int
    sutra: Sutra
    class Config:
        orm_mode = True

class InterpretationBase(BaseModel):
    language: Language
    text: str
    philosophy: Philosophy
class InterpretationCreate(InterpretationBase):
    pass
class InterpretationOut(InterpretationBase):
    id: int
class InterpretationUpdate(InterpretationBase):
    pass
class Interpretation(InterpretationBase):
    id: int
    sutra: Sutra
    class Config:
        orm_mode = True

class Audio(BaseModel):
    file_path: str

class BhashyamBase(BaseModel):
    language: Language
    text: str
    philosophy: Philosophy
class BhashyamCreate(BhashyamBase):
    pass
class BhashyamOut(BhashyamBase):
    id: int
class BhashyamUpdate(BhashyamBase):
    pass
class Bhashyam(BhashyamBase):
    id: int
    sutra: Sutra
    class Config:
        orm_mode = True

class Result(BaseModel):
    text: str
    sutra_no: int
    mode: str | None
    lang: str | None
