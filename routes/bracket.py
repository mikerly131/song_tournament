"""
Has routes for creating, viewing and filling out brackets
"""
from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from data.database import get_db_session
from services import bracket_svc

templates = Jinja2Templates(directory='templates')
router = APIRouter()


def get_db():
    with get_db_session() as db:
        yield db


@router.get("/create/bracket")
async def create_bracket(request: Request):
    return templates.TemplateResponse("/brackets/create-bracket.html", {"request": request})


@router.post("/create/bracket")
async def create_bracket(request: Request, db: Session = Depends(get_db)):

    # get the form data
    form_data = await request.form()

    # get user from cookie or token
    user_id = 1

    name = form_data.get("bracket_name")
    seeding_type = form_data.get("bracket_seed")
    pool_size = int(form_data.get("bracket_size"))
    form_songs = []
    for s in range(pool_size):
        song = {
            "title": form_data.get(f"songs[{s}][title]"),
            "artist": form_data.get(f"songs[{s}][artist]"),
            "clip_url": form_data.get(f"songs[{s}][clip_url]")
        }
        form_songs.append(song)
    print(form_songs)

    # create the songs in the database, get back a list of songs dictionaries with song ids
    songs = bracket_svc.create_songs(db, form_songs)

    # create the song list in the database, get back the song list id
    song_list_id = bracket_svc.create_song_list(db, songs, pool_size, user_id)

    # create the bracket in the database, get back the bracket id
    bracket_id = bracket_svc.create_new_bracket(db, song_list_id, songs, name, seeding_type, pool_size, user_id)

    # redirect user to fill out bracket
    return RedirectResponse(url=f"/fill-out/bracket/{bracket_id}", status_code=303)


@router.get("/fill-out/bracket/{bracket_id}")
async def fill_out_bracket(request: Request, bracket_id: int, db: Session = Depends(get_db)):

    bracket_data = bracket_svc.get_bracket_data(db, bracket_id)

    # if bracket_data.pool_size == 8:
    #     pass
    # elif bracket_data.pool_size == 16:
    #     pass
    # elif bracket_data.pool_size == 32:
    #     pass
    # elif bracket_data.pool_size == 64:
    #     pass

    # response_template = f"/brackets/view-bracket-{bracket_size}.html"
    return templates.TemplateResponse("/brackets/view-bracket-64.html", {"request": request, "bracket": bracket_data})
