"""
Has routes for creating and viewing brackets
"""
from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from data.database import get_db_session
from services import bracket_svc, auth_svc


templates = Jinja2Templates(directory='templates')
router = APIRouter()


@router.get("/create/bracket")
async def get_bracket_setup(request: Request, user_id: int = Depends(auth_svc.get_user_id_via_auth_cookie)):
    return templates.TemplateResponse("/brackets/create-bracket.html", {"request": request, "user_id": user_id})


@router.post("/create/bracket")
async def create_bracket(request: Request, db: Session = Depends(get_db_session),
                         user: int = Depends(auth_svc.get_user_id_via_auth_cookie)):

    # get the form data
    form_data = await request.form()

    # get user from cookie or token
    if user:
        user_id = user
    else:
        return {"Failure": "Not logged in"}

    name = form_data.get("bracket_name")
    seeding_type = form_data.get("bracket_seed")
    pool_size = int(form_data.get("bracket_size"))
    form_songs = []
    for s in range(pool_size):
        song = {
            "title": form_data.get(f"songs[{s}][title]"),
            "artist": form_data.get(f"songs[{s}][artist]")
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
async def fill_out_bracket(request: Request, bracket_id: int, db: Session = Depends(get_db_session),
                           user: int = Depends(auth_svc.get_user_id_via_auth_cookie)):

    if not user:
        return None

    bracket_data = bracket_svc.get_bracket_data(db, bracket_id)

    for song in bracket_data.seed_list:
        song['title'] = bracket_svc.escape_html_chars(song['title'])
        song['artist'] = bracket_svc.escape_html_chars(song['artist'])

    response_template = f"/brackets/fill-bracket-{bracket_data.pool_size}.html"

    return templates.TemplateResponse(response_template, {"request": request, "user_id": user, "bracket": bracket_data})


# Trying out HTMX, idea is to let users click on a team in a match and that updates the next match with the team
# Broken:  Title and Artist with apostrophes, creating issues
@router.get("/update_match_semifinal", response_class=HTMLResponse)
async def update_match_semifinal(request: Request, user: int = Depends(auth_svc.get_user_id_via_auth_cookie)):

    if not user:
        return None

    # Start simple, don't worry about cascading changes from previous rounds into later rounds yet.
    s_id = request.query_params.get('id')
    s_title = request.query_params.get('title')
    s_artist = request.query_params.get('artist')
    target = request.query_params.get('target')

    if target == 'semi-final-left-top' or 'semi-final-left-bottom':
        n_target = 'finals-top'
    elif target == 'semi-final-right-top' or 'semi-final-right-bottom':
        n_target = 'finals-bottom'

    html_content = f"""
    <button hx-get="/update_match_final" hx-target="#{n_target}" hx-swap="outerHTML" hx-trigger="click"
            hx-params="id, title, artist, target"
            hx-vars="id: '{s_id}', title: '{s_title}', artist: '{s_artist}', target: '{n_target}'"
            class="team top" id="{target}">
        <div id="song_{s_id}"> {s_title} - {s_artist}</div>
    </button>
    """

    return HTMLResponse(content=html_content)


@router.get("/update_match_final", response_class=HTMLResponse)
async def update_match_final(request: Request, user: int = Depends(auth_svc.get_user_id_via_auth_cookie)):

    if not user:
        return None

    s_id = request.query_params.get('id')
    s_title = request.query_params.get('title')
    s_artist = request.query_params.get('artist')
    target = request.query_params.get('target')

    html_content = f"""
    <button hx-get="/update_champion" hx-target="#champion-team" hx-swap="innerHTML" hx-trigger="click"
            hx-params="id, title, artist"
            hx-vars="id: '{s_id}', title: '{s_title}', artist: '{s_artist}'"
            class="team top" id="{target}">
        <div id="song_{s_id}"> {s_title} - {s_artist}</div>
    </button>
    """

    return HTMLResponse(content=html_content)


@router.get("/update_champion", response_class=HTMLResponse)
async def update_champion(request: Request, user: int = Depends(auth_svc.get_user_id_via_auth_cookie)):

    if not user:
        return None

    s_id = request.query_params.get('id')
    s_title = request.query_params.get('title')
    s_artist = request.query_params.get('artist')

    html_content = f"""
    <h3 class="text-center">Champion</h3>
    <div class="team" id="song_{s_id}"> {s_title} - {s_artist}</div>
    """

    return HTMLResponse(content=html_content)