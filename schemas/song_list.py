"""
Pydantic classes for song lists, translation between routes and db
"""
from pydantic import BaseModel
from typing import Optional


class SongList(BaseModel):
    id: int
    creator: int
    size: int
    songs: Optional[list]
