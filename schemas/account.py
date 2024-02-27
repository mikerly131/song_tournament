"""
Pydantic classes for accounts, data translation between routes and db
"""
from pydantic import BaseModel
from typing import List, ForwardRef


class User(BaseModel):
    id: int
    username: str


class UserIn(User):
    password: str


class UserInDB(User):
    hashed_password: str

# For relationships, commented out until I decide ot use them
#
# Bracket = ForwardRef('Bracket')
# FilledBracket = ForwardRef('FilledBracket')
#
#
# class UserWithBrackets(User):
#     created_brackets: List[Bracket] = []
#     filled_brackets: List[FilledBracket] = []
#
#
# from .bracket import Bracket
# from .filled_bracket import FilledBracket
# UserWithBrackets.update_forward_refs()