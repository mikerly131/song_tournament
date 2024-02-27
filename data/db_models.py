"""
Setup ORM models with attributes to create/interact with db tables and columns

Relationships commented out while working on simple pydantic models and routes, it complicates things
"""
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text, String
from typing import Optional, List


class Base(DeclarativeBase):
    pass


class Song(Base):
    __tablename__ = 'song'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    artist: Mapped[str]
    clip: Mapped[str]


class SongList(Base):
    __tablename__ = 'song_list'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80))
    creator: Mapped[int] = mapped_column(ForeignKey('user.id'))
    size: Mapped[int]
    songs: Mapped[list] = mapped_column(Text)


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    hash_password: Mapped[str]

    # relationships
    # created_brackets: Mapped[List["Bracket"]] = relationship(back_populates="user")
    # filled_brackets: Mapped[List["FilledBracket"]] = relationship(back_populates="user")


class Bracket(Base):
    __tablename__ = 'bracket'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    song_list_id: Mapped[int] = mapped_column(ForeignKey('song_list.id'))
    pool_size: Mapped[int]
    ranking_type: Mapped[str]
    bracket_status: Mapped[str]
    seed_list: Mapped[Optional[list]] = mapped_column(Text)

    # relationships
    # user: Mapped['User'] = relationship(back_populates="created_brackets")
    # filled_brackets: Mapped[List["FilledBracket"]] = relationship(back_populates="original_bracket")


class FilledBracket(Base):
    __tablename__ = 'filled_bracket'

    id: Mapped[int] = mapped_column(primary_key=True)
    bracket_id: Mapped[int] = mapped_column(ForeignKey('bracket.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    bracket_list: Mapped[list] = mapped_column(Text)
    first_32: Mapped[Optional[list]] = mapped_column(Text)
    sweet_16: Mapped[Optional[list]] = mapped_column(Text)
    elite_8: Mapped[Optional[list]] = mapped_column(Text)
    final_4: Mapped[Optional[list]] = mapped_column(Text)
    last_2: Mapped[Optional[list]] = mapped_column(Text)
    champion: Mapped[Optional[list]] = mapped_column(Text)

    # relationships
    # user: Mapped["User"] = relationship(back_populates="filled_brackets")
    # original_bracket: Mapped["Bracket"] = relationship(back_populates="filled_brackets")
