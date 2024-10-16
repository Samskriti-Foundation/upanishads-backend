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

