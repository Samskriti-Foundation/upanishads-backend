from enum import Enum

import bcrypt


# Hash a password before storing it
def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()  # Generate a salt
    hashed_password = bcrypt.hashpw(
        plain_password.encode("utf-8"), salt
    )  # Hash the password
    return hashed_password.decode(
        "utf-8"
    )  # Return as a string to store in the database


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


class Language(str, Enum):
    sa = "sa"  # Sanskrit
    en = "en"  # English
    kn = "kn"  # Kannada
    ta = "ta"  # Tamil
    te = "te"  # Telugu
    hi = "hi"  # Hindi


class Philosophy(str, Enum):
    advaita = "adv"  # Advaita
    vishishtadvaita = "vis"  # Vishishtadvaita
    dvaita = "dva"  # Dvaita


class Mode(str, Enum):
    chant = "chant"  # Chant
    teachMe = "teach_me"  # Teach Me
    learnMore = "learn_more"  # Learn More
