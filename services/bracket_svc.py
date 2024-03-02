from data import db_models
from sqlalchemy.orm import Session
from sqlalchemy import select
import random


# Function to create the songs in the db
def create_songs(db: Session, songs: list):

    # Using the ORM model, create a Song for each item in songs (list of dicts)
    db_songs = []
    for song in songs:
        db_song = db_models.Song(
            title=song['title'],
            artist=song['artist'],
            clip_url=song['clip_url']
        )
        db.add(db_song)
        db_songs.append(db_song)

    # Flush to get the song ids generated
    db.flush()

    # Return a list of song dicts instead of Song objects
    song_list = []
    for s in db_songs:
        song_list.append({
            'id': s.id,
            'title': s.title,
            'artist': s.artist,
        })

    return song_list


def extract_song_id(songs: list):
    song_ids = []
    for song in songs:
        song_ids.append(song['id'])
    return song_ids


# Function to create a song list in the db
def create_song_list(db: Session, songs: list, size: int, user_id: int):

    song_ids = extract_song_id(songs)
    song_list = db_models.SongList(
        creator=user_id,
        size=size,
        songs=song_ids
    )
    db.add(song_list)
    db.flush()

    return song_list.id


def shuffle_songs(songs: list):
    random.shuffle(songs)
    return songs


# Function to create a new tournament bracket in the db
def create_new_bracket(db: Session, song_list_id: int, song_list: list,
                       name: str, seed_typ: str, pool_size: int, user_id: int):

    if seed_typ == "random":
        song_list = shuffle_songs(song_list)

    new_bracket = db_models.Bracket(
        user_id=user_id,
        song_list_id=song_list_id,
        name=name,
        pool_size=pool_size,
        seeding_type=seed_typ,
        seed_list=song_list
    )
    db.add(new_bracket)
    db.flush()

    return new_bracket.id


# Function to get bracket data
def get_bracket_data(db: Session, bracket_id: int):
    query = select(db_models.Bracket).where(id=bracket_id)
    result = db.execute(query)
    bracket_data = result.scalars().first()
    return bracket_data


# Function to view summary details of all brackets
def view_brackets():
    pass


# Function to view a single filled out bracket
def view_bracket():
    pass



