from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Sutra(Base):
    __tablename__ = "sutras"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, unique=True)
    text = Column(String(1000), nullable=False, unique=True)

    transliterations = relationship(
        "Transliteration", back_populates="sutra", cascade="all, delete-orphan"
    )
    meanings = relationship(
        "Meaning", back_populates="sutra", cascade="all, delete-orphan"
    )
    interpretations = relationship(
        "Interpretation", back_populates="sutra", cascade="all, delete-orphan"
    )


class Transliteration(Base):
    __tablename__ = "transliterations"

    id = Column(Integer, primary_key=True, index=True)
    language = Column(String(50), nullable=False)
    text = Column(String(1000), nullable=False)
    sutra_id = Column(Integer, ForeignKey("sutras.id", ondelete="CASCADE"))

    sutra = relationship("Sutra", back_populates="transliterations")


class Meaning(Base):
    __tablename__ = "meanings"

    id = Column(Integer, primary_key=True, index=True)
    language = Column(String(50), nullable=False)
    text = Column(String(1000), nullable=False)
    sutra_id = Column(Integer, ForeignKey("sutras.id", ondelete="CASCADE"))

    sutra = relationship("Sutra", back_populates="meanings")


class Interpretation(Base):
    __tablename__ = "interpretations"

    id = Column(Integer, primary_key=True, index=True)
    language = Column(String(50), nullable=False)
    text = Column(String(1000), nullable=False)
    philosophy_type = Column(String(50), nullable=False)
    sutra_id = Column(Integer, ForeignKey("sutras.id", ondelete="CASCADE"))

    sutra = relationship("Sutra", back_populates="interpretations")


class Word(Base):
    __tablename__ = "sanskrit_words"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(50), unique=True, nullable=False)

    word_meanings = relationship(
        "WordMeaning", back_populates="word", cascade="all, delete-orphan"
    )
    references = relationship(
        "Reference", back_populates="word", cascade="all, delete-orphan"
    )
    etymologies = relationship(
        "Etymology", back_populates="word", cascade="all, delete-orphan"
    )
    derivations = relationship(
        "Derivation", back_populates="word", cascade="all, delete-orphan"
    )
    synonyms = relationship(
        "Synonym", back_populates="word", cascade="all, delete-orphan"
    )
    antonyms = relationship(
        "Antonym", back_populates="word", cascade="all, delete-orphan"
    )


class WordMeaning(Base):
    __tablename__ = "word_meanings"

    id = Column(Integer, primary_key=True, index=True)
    language = Column(String(50), nullable=False)
    text = Column(String(1000), nullable=False)
    sanskrit_word_id = Column(
        Integer, ForeignKey("sanskrit_words.id", ondelete="CASCADE")
    )

    word = relationship("Word", back_populates="word_meanings")


class Reference(Base):
    __tablename__ = "references"

    id = Column(Integer, primary_key=True, index=True)
    language = Column(String(50), nullable=False)
    text = Column(String(1000), nullable=False)
    sanskrit_word_id = Column(
        Integer, ForeignKey("sanskrit_words.id", ondelete="CASCADE")
    )

    word = relationship("Word", back_populates="word_meanings")


class Etymology(Base):
    __tablename__ = "etymologies"

    id = Column(Integer, primary_key=True, index=True)
    language = Column(String(50), nullable=False)
    text = Column(String(1000), nullable=False)
    sanskrit_word_id = Column(
        Integer, ForeignKey("sanskrit_words.id", ondelete="CASCADE")
    )

    word = relationship("Word", back_populates="word_meanings")


class Derivation(Base):
    __tablename__ = "derivations"

    id = Column(Integer, primary_key=True, index=True)
    language = Column(String(50), nullable=False)
    text = Column(String(1000), nullable=False)
    sanskrit_word_id = Column(
        Integer, ForeignKey("sanskrit_words.id", ondelete="CASCADE")
    )

    word = relationship("Word", back_populates="word_meanings")


class Antonyms(Base):
    __tablename__ = "antonyms"

    id = Column(Integer, primary_key=True, index=True)
    language = Column(String(50), nullable=False)
    text = Column(String(1000), nullable=False)
    sanskrit_word_id = Column(
        Integer, ForeignKey("sanskrit_words.id", ondelete="CASCADE")
    )

    word = relationship("Word", back_populates="word_meanings")


class Synonyms(Base):
    __tablename__ = "synonyms"

    id = Column(Integer, primary_key=True, index=True)
    language = Column(String(50), nullable=False)
    text = Column(String(1000), nullable=False)
    sanskrit_word_id = Column(
        Integer, ForeignKey("sanskrit_words.id", ondelete="CASCADE")
    )

    word = relationship("Word", back_populates="word_meanings")
