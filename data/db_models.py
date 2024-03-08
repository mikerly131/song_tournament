"""
Setup ORM models with attributes to create/interact with db tables and columns

Relationships commented out while working on simple routes, it complicates pydantic models
"""
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import ForeignKey, Text, String
from typing import Optional, List


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    hash_password: Mapped[str]

    # relationships
    # created_brackets: Mapped[List["Bracket"]] = relationship(back_populates="user")
    # filled_brackets: Mapped[List["FilledBracket"]] = relationship(back_populates="user")


class Song(Base):
    __tablename__ = 'song'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    artist: Mapped[str]


class SongList(Base):
    __tablename__ = 'song_list'

    id: Mapped[int] = mapped_column(primary_key=True)
    creator: Mapped[int] = mapped_column(ForeignKey('user.id'))
    size: Mapped[int]
    songs: Mapped[list] = mapped_column(JSON)


class Bracket(Base):
    __tablename__ = 'bracket'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    song_list_id: Mapped[int] = mapped_column(ForeignKey('song_list.id'))
    name: Mapped[str]
    pool_size: Mapped[int]
    seeding_type: Mapped[str]
    seed_list: Mapped[Optional[list]] = mapped_column(JSON)

    # relationships
    # user: Mapped['User'] = relationship(back_populates="created_brackets")
    # filled_brackets: Mapped[List["FilledBracket"]] = relationship(back_populates="original_bracket")


class FilledBracket(Base):
    __tablename__ = 'filled_bracket'

    id: Mapped[int] = mapped_column(primary_key=True)
    bracket_id: Mapped[int] = mapped_column(ForeignKey('bracket.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    bracket_name: Mapped[str]
    pool_size: Mapped[int]
    seed_list: Mapped[list] = mapped_column(JSON)
    bracket_dict: Mapped[Optional[dict]] = mapped_column(JSON, default={})

    # relationships
    # user: Mapped["User"] = relationship(back_populates="filled_brackets")
    # original_bracket: Mapped["Bracket"] = relationship(back_populates="filled_brackets")
