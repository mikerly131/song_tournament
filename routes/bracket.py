"""
Has routes for creating and viewing brackets
"""
from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse, HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from data.database import get_db_session
from services import bracket_svc, auth_svc


templates = Jinja2Templates(directory='templates')
templates.env.filters['handle_stupid_chars'] = bracket_svc.handle_stupid_chars

router = APIRouter()


# For creating a new tournament - get form for name, size, seeding type, list of songs to seed
@router.get("/create/bracket")
async def get_bracket_setup(request: Request, user_id: int = Depends(auth_svc.get_user_id_via_auth_cookie)):
    return templates.TemplateResponse("/brackets/create-bracket.html", {"request": request, "user_id": user_id})


# For creating a new tournament - post form with name, size, seeding type, list of songs to seed
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

    # create the songs  in the database, get back a list of songs dictionaries with song ids
    songs = bracket_svc.create_songs(db, form_songs)

    # create the song list in the database, get back the song list id
    song_list_id = bracket_svc.create_song_list(db, songs, pool_size, user_id)

    # create the bracket in the database, get back the bracket id
    bracket_id = bracket_svc.create_new_bracket(db, song_list_id, songs, name, seeding_type, pool_size, user_id)

    # redirect user to fill out bracket
    return RedirectResponse(url=f"/fill-out/bracket/{bracket_id}", status_code=303)


# For viewing all tournaments that have been created
@router.get("/view/tournaments")
async def view_tournaments(request: Request, db: Session = Depends(get_db_session),
                           user_id: int = Depends(auth_svc.get_user_id_via_auth_cookie)):

    if not user_id:
        return None

    tournaments = bracket_svc.view_tournaments(db)
    return templates.TemplateResponse('/view_tournaments.html', {"request": request, "user_id": user_id,
                                                                 "tournaments": tournaments})


# For viewing all the filled out brackets for a given tournament
@router.get("/view/tournament/{bracket_id}/filled-out-brackets")
async def view_tournament_brackets(request: Request, bracket_id: int, tournament_name: str, db: Session = Depends(get_db_session),
                                   user_id: int = Depends(auth_svc.get_user_id_via_auth_cookie)):

    if not user_id:
        return None

    filled_brackets = bracket_svc.get_f_bracket_data(db, bracket_id)
    if filled_brackets:
        bracket_name = tournament_name
    else:
        bracket_name = "No Brackets Yet"

    return templates.TemplateResponse('/view_tournament_brackets.html', {"request": request, "user_id": user_id,
                                                                         "filled_brackets": filled_brackets,
                                                                         "bracket_name": bracket_name})


# For viewing a single bracket filled out for a tournament
@router.get("/view/tournament/{bracket_id}/filled-out-bracket/{f_brkt_id}")
async def view_filled_out_bracket(request: Request, f_brkt_id: int, db: Session = Depends(get_db_session),
                                  user_id: int = Depends(auth_svc.get_user_id_via_auth_cookie)):

    if not user_id:
        return None

    single_f_bracket = bracket_svc.view_single_f_bracket_(db, f_brkt_id)
    return templates.TemplateResponse('/view_tournament_brackets.html', {"request": request, "user_id": user_id,
                                                                         "bracket": single_f_bracket})


# For getting a bracket to fill out for a tournament
@router.get("/fill-out/bracket/{bracket_id}")
async def fill_out_bracket(request: Request, bracket_id: int, db: Session = Depends(get_db_session),
                           user: int = Depends(auth_svc.get_user_id_via_auth_cookie)):

    if not user:
        return None

    bracket_data = bracket_svc.get_bracket_data(db, bracket_id)

    pool_size = bracket_data.pool_size
    seed_list = bracket_data.seed_list
    brkt_id = bracket_data.id
    brkt_name = f'My Bracket For: {bracket_data.name}'
    saved_bracket_id = bracket_svc.create_filled_bracket(db, brkt_id, seed_list, brkt_name, pool_size, user)

    response_template = f"/brackets/fill-bracket-{bracket_data.pool_size}.html"

    return templates.TemplateResponse(response_template, {"request": request, "user_id": user,
                                                          "bracket": bracket_data, "f_brkt_id": saved_bracket_id,
                                                          "f_brkt_name": brkt_name})


# For updating the next match in the tournament with the selected team from the previous match
@router.post("/update_match/{f_brkt_id}", response_class=HTMLResponse)
async def update_match(request: Request, f_brkt_id: int, db: Session = Depends(get_db_session),
                                        user: int = Depends(auth_svc.get_user_id_via_auth_cookie)):

    if not user:
        return None

    # Start simple, don't worry about cascading changes from previous rounds into later rounds yet.
    form_data = await request.form()
    s_id = form_data.get('id')
    s_title = form_data.get('title')
    s_artist = form_data.get('artist')
    target = form_data.get('target')
    a_song = {"song_id": s_id, "title": s_title, "artist": s_artist}

    update_bracket_winners = bracket_svc.save_bracket_data(db, f_brkt_id, target, a_song)

    if update_bracket_winners is False:
        return None

    n_target = bracket_svc.get_target_location(target)

    if target != 'champion-team':
        esc_title = bracket_svc.handle_stupid_chars(s_title)
        esc_artist = bracket_svc.handle_stupid_chars(s_artist)

        html_content = f"""
        <button hx-post="/update_match/{f_brkt_id}" hx-target="#{n_target}" hx-swap="outerHTML" hx-trigger="click"
                hx-params="id, title, artist, target"
                hx-vars="id: '{s_id}', title: '{esc_title}' , artist: '{esc_artist}', target: '{n_target}'"
                class="team" id="{target}">
            <div id="song_{s_id}"> {s_title} - {s_artist}</div>
        </button>
        """
    else:
        html_content = f"""
        <div class="team" id="champion-team"> 
            <div id="song_{s_id}">{s_title} - {s_artist}</div>
        </div>
        """

    return HTMLResponse(content=html_content)


# (Not using right now, just saving after each selection)
# @router.post("/save_bracket/{bracket_id}")
# async def save_bracket(response: Response, bracket_id: int, db: Session = Depends(get_db_session),
#                        user: int = Depends(auth_svc.get_user_id_via_auth_cookie)):
#
#     if not user:
#         return None
#
#     orig_bracket = bracket_svc.get_bracket_data(db, bracket_id)
#     pool_size = orig_bracket.pool_size
#     seed_list = orig_bracket.seed_list
#     brkt_id = orig_bracket.id
#     brkt_name = orig_bracket.name
#     saved_bracket_id = bracket_svc.create_filled_bracket(db, brkt_id, seed_list, brkt_name, user)
#
#     response.headers['HX-Redirect'] = f'/view/filled-out-bracket/{saved_bracket_id}'
#     return {"success": "Filled out bracket saved"}

# Add this to html when uncommenting ( and modify accordinngly with function )
# <div class ="sav-btn row">
#     <button hx-post = "/save_bracket/{{ bracket_data.id }}" hx-target = "none">
#         Save Bracket
#     </button>
# </div>
