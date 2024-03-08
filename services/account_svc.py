"""
Services for accounts to be created, login and logout. Maybe combine with auth services.
"""
from data.db_models import User
from sqlalchemy.orm import Session
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
from sqlalchemy import select


def create_account(db: Session, username: str, password: str):
    user = User()
    user.username = username
    user.hash_password = crypto.hash(password, rounds=123_981)
    db.add(user)
    db.flush()
    return user.id


def login_account(db: Session, username: str, password: str):
    user_data = None
    query = select(User).where(User.username == username)
    result = db.execute(query)
    user = result.scalar_one_or_none()
    if user and crypto.verify(password, user.hash_password):
        user_data = {"username": user.username, "id": user.id}
    return user_data
