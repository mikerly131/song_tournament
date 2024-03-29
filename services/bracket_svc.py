"""
Services for CRUD on db for bracket routes / operations
"""
from data import db_models, targets
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy import select, func, outerjoin
import random


# Function to create the songs in the db
def create_songs(db: Session, songs: list):

    # Using the ORM model, create a Song for each item in songs (list of dicts)
    db_songs = []
    for song in songs:
        db_song = db_models.Song(
            title=song['title'],
            artist=song['artist']
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


# Get tournament bracket data for filling out a bracket
def get_tournament_data(db: Session, bracket_id: int):
    query = select(db_models.Bracket).where(db_models.Bracket.id == bracket_id)
    result = db.execute(query)
    tournament_data = result.scalars().first()
    return tournament_data


# Escape stupid characters in songs and artists so it doesn't break html/htmx
def handle_stupid_chars(song_attribute: str):
    song_attribute = song_attribute.replace(
        "'", "\\'"
    ).replace(
        '"', '\\"'
    ).replace("&", "u0026")
    return song_attribute


# Creates a bracket based on an initial tournament bracket
def create_filled_bracket(db: Session, brkt_id: int, seed_list: list,
                          brkt_name: str, pool_size: int, user_id: int):

    new_filled_bracket = db_models.FilledBracket(
        bracket_id=brkt_id,
        user_id=user_id,
        seed_list=seed_list,
        bracket_name=brkt_name,
        pool_size=pool_size
    )
    db.add(new_filled_bracket)
    db.flush()

    return new_filled_bracket.id


# Get location in next round for selected winner
def get_target_location(prev_target: str) -> str:
    next_target = targets.locations.get(prev_target)
    return next_target


# Save bracket data in the filled bracket dict (each match winner selection)
def save_bracket_data(db: Session, f_brkt_id: int, target: str, song: dict):
    query = select(db_models.FilledBracket).where(db_models.FilledBracket.id == f_brkt_id)
    result = db.execute(query)
    f_brkt_data = result.scalars().first()

    if not f_brkt_data:
        return False

    f_brkt_data.bracket_dict[target] = song
    db.add(f_brkt_data)
    flag_modified(f_brkt_data, "bracket_dict")
    db.flush()

    return True


# (Not in use right now) Function to save entire filled out tournament bracket
# def save_filled_bracket(db: Session, brkt_id: int, seed_list: list,
#                           brkt_name: str, pool_size: int, user_id: int):
#
#     new_filled_bracket = db_models.FilledBracket(
#         bracket_id=brkt_id,
#         user_id=user_id,
#         seed_list=seed_list,
#         bracket_name=brkt_name,
#         pool_size=pool_size
#     )
#     db.add(new_filled_bracket)
#     db.flush()
#
#     return new_filled_bracket.id


# Gat a filled out bracket by a user for a tournament
def get_my_filled_out_bracket(db: Session, bracket_id: int, user_id: int):
    query = select(db_models.FilledBracket).where(db_models.FilledBracket.id == bracket_id,
                                                  db_models.FilledBracket.user_id == user_id)
    result = db.execute(query)
    bracket_data = result.scalars().first()
    return bracket_data


# Function to view summary details of all brackets
# add .offset(offset) and offset = 10 if enabling caching at some point
# might need to add a limit at some point, like .limit(100) or something
def view_tournaments(db: Session):
    query = (select(db_models.Bracket.id, db_models.Bracket.pool_size, db_models.Bracket.name,
                    func.count(db_models.FilledBracket.id).label('fill_count'))
             .outerjoin(db_models.FilledBracket, db_models.Bracket.id == db_models.FilledBracket.bracket_id)
             .group_by(db_models.Bracket.id)
             .order_by(func.count(db_models.FilledBracket.id).desc()))
    result = db.execute(query)
    tournaments = result.all()
    return tournaments


# Get the filled out brackets for a tournament
def get_f_bracket_data(db: Session, bracket_id: int):
    query = (select(db_models.FilledBracket.id, db_models.FilledBracket.bracket_id, db_models.FilledBracket.user_id,
                    db_models.User.username)
             .join(db_models.User, db_models.FilledBracket.user_id == db_models.User.id)
             .where(db_models.FilledBracket.bracket_id == bracket_id))
    result = db.execute(query)
    filled_brackets = []
    for fb_id, fb_bracket_id, fb_user_id, username in result.all():
        filled_bracket_data = {
            'id': fb_id,
            'bracket_id': fb_bracket_id,
            'user_id': fb_user_id,
            'username': username
        }
        filled_brackets.append(filled_bracket_data)

    return filled_brackets


# Get a single filled out bracket for a tournament
def view_single_f_bracket_(db: Session, f_brkt_id: int):
    query = (select(db_models.FilledBracket, db_models.User.username)
             .join(db_models.User, db_models.FilledBracket.user_id == db_models.User.id)
             .where(db_models.FilledBracket.id == f_brkt_id))
    result = db.execute(query)
    fb, username = result.first()
    single_f_bracket = {
            'id': fb.id,
            'bracket_id': fb.bracket_id,
            'user_id': fb.user_id,
            'bracket_name': fb.bracket_name,
            'pool_size': fb.pool_size,
            'seed_list': fb.seed_list,
            'bracket_dict': fb.bracket_dict,
            'username': username
        }

    return single_f_bracket






