from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Sutra(Base):
    __tablename__ = "sutras"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    number: Mapped[int] = mapped_column(Integer, unique=True)
    text: Mapped[str] = mapped_column(String(1000), nullable=False, unique=True)

    transliterations: Mapped[list["Transliteration"]] = relationship(
        "Transliteration", back_populates="sutra", cascade="all, delete-orphan"
    )
    meanings: Mapped[list["Meaning"]] = relationship(
        "Meaning", back_populates="sutra", cascade="all, delete-orphan"
    )
    interpretations: Mapped[list["Interpretation"]] = relationship(
        "Interpretation", back_populates="sutra", cascade="all, delete-orphan"
    )


class Transliteration(Base):
    __tablename__ = "transliterations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    language: Mapped[str] = mapped_column(String(50), nullable=False)
    text: Mapped[str] = mapped_column(String(1000), nullable=False)
    sutra_id: Mapped[int] = mapped_column(ForeignKey("sutras.id", ondelete="CASCADE"))

    sutra: Mapped["Sutra"] = relationship("Sutra", back_populates="transliterations")


class Meaning(Base):
    __tablename__ = "meanings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    language: Mapped[str] = mapped_column(String(50), nullable=False)
    text: Mapped[str] = mapped_column(String(1000), nullable=False)
    sutra_id: Mapped[int] = mapped_column(ForeignKey("sutras.id", ondelete="CASCADE"))

    sutra: Mapped["Sutra"] = relationship("Sutra", back_populates="meanings")


class Interpretation(Base):
    __tablename__ = "interpretations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    language: Mapped[str] = mapped_column(String(50), nullable=False)
    text: Mapped[str] = mapped_column(String(1000), nullable=False)
    philosophy_type: Mapped[str] = mapped_column(String(50), nullable=False)
    sutra_id: Mapped[int] = mapped_column(ForeignKey("sutras.id", ondelete="CASCADE"))

    sutra: Mapped["Sutra"] = relationship("Sutra", back_populates="interpretations")


class Word(Base):
    __tablename__ = "sanskrit_words"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    word: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    word_meanings: Mapped[list["WordMeaning"]] = relationship(
        "WordMeaning", back_populates="word", cascade="all, delete-orphan"
    )
    references: Mapped[list["Reference"]] = relationship(
        "Reference", back_populates="word", cascade="all, delete-orphan"
    )
    etymologies: Mapped[list["Etymology"]] = relationship(
        "Etymology", back_populates="word", cascade="all, delete-orphan"
    )
    derivations: Mapped[list["Derivation"]] = relationship(
        "Derivation", back_populates="word", cascade="all, delete-orphan"
    )
    synonyms: Mapped[list["Synonym"]] = relationship(
        "Synonym", back_populates="word", cascade="all, delete-orphan"
    )
    antonyms: Mapped[list["Antonym"]] = relationship(
        "Antonym", back_populates="word", cascade="all, delete-orphan"
    )


class WordMeaning(Base):
    __tablename__ = "word_meanings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    language: Mapped[str] = mapped_column(String(50), nullable=False)
    text: Mapped[str] = mapped_column(String(1000), nullable=False)
    sanskrit_word_id: Mapped[int] = mapped_column(
        ForeignKey("sanskrit_words.id", ondelete="CASCADE")
    )

    word: Mapped["Word"] = relationship("Word", back_populates="word_meanings")


class Reference(Base):
    __tablename__ = "references"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    language: Mapped[str] = mapped_column(String(50), nullable=False)
    text: Mapped[str] = mapped_column(String(1000), nullable=False)
    sanskrit_word_id: Mapped[int] = mapped_column(
        ForeignKey("sanskrit_words.id", ondelete="CASCADE")
    )

    word: Mapped["Word"] = relationship("Word", back_populates="references")


class Etymology(Base):
    __tablename__ = "etymologies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    language: Mapped[str] = mapped_column(String(50), nullable=False)
    text: Mapped[str] = mapped_column(String(1000), nullable=False)
    sanskrit_word_id: Mapped[int] = mapped_column(
        ForeignKey("sanskrit_words.id", ondelete="CASCADE")
    )

    word: Mapped["Word"] = relationship("Word", back_populates="etymologies")


class Derivation(Base):
    __tablename__ = "derivations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    language: Mapped[str] = mapped_column(String(50), nullable=False)
    text: Mapped[str] = mapped_column(String(1000), nullable=False)
    sanskrit_word_id: Mapped[int] = mapped_column(
        ForeignKey("sanskrit_words.id", ondelete="CASCADE")
    )

    word: Mapped["Word"] = relationship("Word", back_populates="derivations")


class Synonym(Base):
    __tablename__ = "synonyms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    language: Mapped[str] = mapped_column(String(50), nullable=False)
    text: Mapped[str] = mapped_column(String(1000), nullable=False)
    sanskrit_word_id: Mapped[int] = mapped_column(
        ForeignKey("sanskrit_words.id", ondelete="CASCADE")
    )

    word: Mapped["Word"] = relationship("Word", back_populates="synonyms")


class Antonym(Base):
    __tablename__ = "antonyms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    language: Mapped[str] = mapped_column(String(50), nullable=False)
    text: Mapped[str] = mapped_column(String(1000), nullable=False)
    sanskrit_word_id: Mapped[int] = mapped_column(
        ForeignKey("sanskrit_words.id", ondelete="CASCADE")
    )

    word: Mapped["Word"] = relationship("Word", back_populates="antonyms")
