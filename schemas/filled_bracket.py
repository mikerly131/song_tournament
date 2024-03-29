"""
Pydantic classes for filled out brackets, data translation between routes and db
"""
from pydantic import BaseModel
from typing import Optional, ForwardRef


class FilledBracket(BaseModel):
    id: int
    bracket_id: int
    user_id: int
    bracket_name: str
    pool_size: int
    seed_list: list
    bracket_list: list
    champion: Optional[list]


# For relationships, commented out until I decide ot use them
#
# User = ForwardRef('User')
# Bracket = ForwardRef('Bracket')
#
#
# class FilledBracketDetails(FilledBracket):
#     user: User
#     original_bracket: Bracket
#
#
# from .account import User
# from .bracket import Bracket
# FilledBracketDetails.update_forward_refs()
