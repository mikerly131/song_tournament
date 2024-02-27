"""
Pydantic classes for songs, translation between routes and db
"""
from pydantic import BaseModel


class Song(BaseModel):
    id: int
    title: str
    artist: str
    clip: str

