from dataclasses import dataclass
import re


@dataclass
class Roles:
    admin = 1
    user = 2


@dataclass
class User:
    """Base user structure"""
    username: str
    password: str
    firstName: str
    lastName: str
    email: str
    age: int
    role: int = Roles.user

    def is_admin(self) -> bool:
        "Return true if the user is admin, else false"
        return self.role == Roles.admin


def validate_username(username: str, minLong: int = 3, maxLong: int = 15) -> bool:
    """Verify that a valid username (alphanumeric)"""
    # If is valid the username, return true
    if re.match(r"^[a-zA-Z0-9]{%d,%d}$" % (minLong, maxLong), username):
        return True
    # else, return false
    return False


def validate_email(email: str) -> bool:
    """Verify that it is a valid email"""
    regex = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"

    # If is valid the email, return true
    if re.match(regex, email):
        return True
    # else, return false
    return False
