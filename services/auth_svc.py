from data.db_models import User
from data.database import get_db_session
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
from sqlalchemy import select


def create_account(username: str, password: str):
    user = User()
    user.username = username
    user.hash_password = crypto.hash(password, rounds=123_981)
    with get_db_session as session:
        session.add(user)
        session.commit()
        usr_name = user.username
    return usr_name


def get_login():
    user = input("Login - Enter your username: ")
    pword = input("Login - Now enter your password: ")
    return user, pword


def login_user(username: str, password: str):
    user_data = None
    with get_db_session() as session:
        query = select(User).where(User.username == username)
        result = session.execute(query)
        user = result.scalar_one_or_none()
        if user and crypto.verify(password, user.hash_password):
            user_data = {"username": user.username, "id": user.id}
    return user_data

