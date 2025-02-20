from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Sutra(Base):
    __tablename__ = "sutras"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    chapter: Mapped[int] = mapped_column(Integer)
    number: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(String(1000), nullable=False)

    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))

    transliterations: Mapped[list["Transliteration"]] = relationship(
        "Transliteration", back_populates="sutra", cascade="all, delete-orphan"
    )
    meanings: Mapped[list["Meaning"]] = relationship(
        "Meaning", back_populates="sutra", cascade="all, delete-orphan"
    )
    interpretations: Mapped[list["Interpretation"]] = relationship(
        "Interpretation", back_populates="sutra", cascade="all, delete-orphan"
    )
    bhashyams: Mapped[list["Bhashyam"]] = relationship(
        "Bhashyam", back_populates="sutra", cascade="all, delete-orphan"
    )

    audios: Mapped[list["Audio"]] = relationship(
        "Audio", back_populates="sutra", cascade="all, delete-orphan"
    )


class Transliteration(Base):
    __tablename__ = "transliterations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    language: Mapped[str] = mapped_column(String(50), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    sutra_id: Mapped[int] = mapped_column(
        ForeignKey("sutras.id", ondelete="CASCADE")
    )

    sutra: Mapped["Sutra"] = relationship("Sutra", back_populates="transliterations")


class Meaning(Base):
    __tablename__ = "meanings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    language: Mapped[str] = mapped_column(String(50), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    sutra_id: Mapped[int] = mapped_column(
        ForeignKey("sutras.id", ondelete="CASCADE")
    )

    sutra: Mapped["Sutra"] = relationship("Sutra", back_populates="meanings")


class Interpretation(Base):
    __tablename__ = "interpretations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    language: Mapped[str] = mapped_column(String(50), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    philosophy: Mapped[str] = mapped_column(String(50), nullable=False)
    sutra_id: Mapped[int] = mapped_column(
        ForeignKey("sutras.id", ondelete="CASCADE")
    )

    sutra: Mapped["Sutra"] = relationship("Sutra", back_populates="interpretations")

class Audio(Base):
    __tablename__ = "audio"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    file_path: Mapped[str] = mapped_column(String(500))  # Relative to static directory
    mode: Mapped[str] = mapped_column(String(10))
    sutra_id: Mapped[int] = mapped_column(
        ForeignKey("sutras.id", ondelete="CASCADE")
    )

    sutra: Mapped["Sutra"] = relationship("Sutra", back_populates="audios")


class Bhashyam(Base):
    __tablename__ = "bhashyams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    language: Mapped[str] = mapped_column(String(50), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    philosophy: Mapped[str] = mapped_column(String(50), nullable=False)
    sutra_id: Mapped[int] = mapped_column(
        ForeignKey("sutras.id", ondelete="CASCADE")
    )

    sutra: Mapped["Sutra"] = relationship("Sutra", back_populates="bhashyams")

