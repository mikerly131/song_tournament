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

    # create the songs  in the database, get back a list of songs dictionaries with song ids
    songs = bracket_svc.create_songs(db, form_songs)

    # create the song list in the database, get back the song list id
    song_list_id = bracket_svc.create_song_list(db, songs, pool_size, user_id)

    # create the bracket in the database, get back the bracket id
    bracket_id = bracket_svc.create_new_bracket(db, song_list_id, songs, name, seeding_type, pool_size, user_id)

    # redirect user to fill out bracket
    return RedirectResponse(url=f"/fill-out/bracket/{bracket_id}", status_code=303)


@router.get("/view/filled-out-bracket/{bracket_id}")
async def view_filled_out_bracket(request: Request, bracket_id: int, user_id: int = Depends(auth_svc.get_user_id_via_auth_cookie)):
    return {"Message": "Filled Out Bracket Will Be Here Eventually"}


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


# Trying out HTMX, idea is to let users click on a team in a match and that updates the next match with the team
# Round of 64 match rout to put winners into round of 32 matches
@router.get("/update_match_round_thirty_two/{f_brkt_id}", response_class=HTMLResponse)
async def update_match_round_thirty_two(request: Request, f_brkt_id: int, db: Session = Depends(get_db_session),
                                        user: int = Depends(auth_svc.get_user_id_via_auth_cookie)):

    if not user:
        return None

    # Start simple, don't worry about cascading changes from previous rounds into later rounds yet.
    s_id = request.query_params.get('id')
    s_title = request.query_params.get('title')
    s_artist = request.query_params.get('artist')
    target = request.query_params.get('target')
    a_song = {"song_id": s_id, "title": s_title, "artist": s_artist}

    update_bracket_winners = bracket_svc.save_bracket_data(db, f_brkt_id, target, a_song)

    if update_bracket_winners is False:
        return None

    esc_title = bracket_svc.handle_stupid_chars(s_title)
    esc_artist = bracket_svc.handle_stupid_chars(s_artist)

    # targets - rnd 32 left top 1, rnd 32 left bottom 1, rnd 32 left top 2, rnd 32 left bottom 2,
    #           rnd 32 left top 3, rnd 32 left bottom 3, rnd 32 left top 4, rnd 32 left bottom 4,
    #           rnd 32 left top 5, rnd 32 left bottom 5, rnd 32 left top 6, rnd 32 left bottom 6,
    #           rnd 32 left top 7, rnd 32 left bottom 7, rnd 32 left top 8, rnd 32 left bottom 8,
    #           repeat for right
    n_target = ''
    if target == 'rnd32-left-top-1' or target == 'rnd32-left-bottom-1':
        n_target = 'swt-left-top-1'
    elif target == 'rnd32-left-top-2' or target == 'rnd32-left-bottom-2':
        n_target = 'swt-left-bottom-1'
    elif target == 'rnd32-left-top-3' or target == 'rnd32-left-bottom-3':
        n_target = 'swt-left-top-2'
    elif target == 'rnd32-left-top-4' or target == 'rnd32-left-bottom-4':
        n_target = 'swt-left-bottom-2'
    elif target == 'rnd32-left-top-5' or target == 'rnd32-left-bottom-5':
        n_target = 'swt-left-top-3'
    elif target == 'rnd32-left-top-6' or target == 'rnd32-left-bottom-6':
        n_target = 'swt-left-bottom-3'
    elif target == 'rnd32-left-top-7' or target == 'rnd32-left-bottom-7':
        n_target = 'swt-left-top-4'
    elif target == 'rnd32-left-top-8' or target == 'rnd32-left-bottom-8':
        n_target = 'swt-left-bottom-4'
    elif target == 'rnd32-right-top-1' or target == 'rnd32-right-bottom-1':
        n_target = 'swt-right-top-1'
    elif target == 'rnd32-right-top-2' or target == 'rnd32-right-bottom-2':
        n_target = 'swt-right-bottom-1'
    elif target == 'rnd32-right-top-3' or target == 'rnd32-right-bottom-3':
        n_target = 'swt-right-top-2'
    elif target == 'rnd32-right-top-4' or target == 'rnd32-right-bottom-4':
        n_target = 'swt-right-bottom-2'
    elif target == 'rnd32-right-top-5' or target == 'rnd32-right-bottom-5':
        n_target = 'swt-right-top-3'
    elif target == 'rnd32-right-top-6' or target == 'rnd32-right-bottom-6':
        n_target = 'swt-right-bottom-3'
    elif target == 'rnd32-right-top-7' or target == 'rnd32-right-bottom-7':
        n_target = 'swt-right-top-4'
    elif target == 'rnd32-right-top-8' or target == 'rnd32-right-bottom-8':
        n_target = 'swt-right-bottom-4'

    html_content = f"""
    <button hx-get="/update_match_sweet/{f_brkt_id}" hx-target="#{n_target}" hx-swap="outerHTML" hx-trigger="click"
            hx-params="id, title, artist, target"
            hx-vars="id: '{s_id}', title: '{esc_title}' , artist: '{esc_artist}', target: '{n_target}'"
            class="team" id="{target}">
        <div id="song_{s_id}"> {s_title} - {s_artist}</div>
    </button>
    """

    return HTMLResponse(content=html_content)


# Round of 32 match route to put winners into sweet round match
@router.get("/update_match_sweet/{f_brkt_id}", response_class=HTMLResponse)
async def update_match_sweet(request: Request, f_brkt_id: int, db: Session = Depends(get_db_session),
                             user: int = Depends(auth_svc.get_user_id_via_auth_cookie)):

    if not user:
        return None

    # Start simple, don't worry about cascading changes from previous rounds into later rounds yet.
    s_id = request.query_params.get('id')
    s_title = request.query_params.get('title')
    s_artist = request.query_params.get('artist')
    target = request.query_params.get('target')
    a_song = {"song_id": s_id, "title": s_title, "artist": s_artist}

    update_bracket_winners = bracket_svc.save_bracket_data(db, f_brkt_id, target, a_song)

    if update_bracket_winners is False:
        return None

    esc_title = bracket_svc.handle_stupid_chars(s_title)
    esc_artist = bracket_svc.handle_stupid_chars(s_artist)

    # targets - swt 16 left top 1, swt 16 left bottom 1, swt 16 left top 2, swt 16 left bottom 2,
    #           swt 16 left top 3, swt 16 left bottom 3, swt 16 left top 4, swt 16 left bottom 4,
    #           repeat for right
    n_target = ''
    if target == 'swt-left-top-1' or target == 'swt-left-bottom-1':
        n_target = 'elite-left-top-1'
    elif target == 'swt-left-top-2' or target == 'swt-left-bottom-2':
        n_target = 'elite-left-bottom-1'
    elif target == 'swt-left-top-3' or target == 'swt-left-bottom-3':
        n_target = 'elite-left-top-2'
    elif target == 'swt-left-top-4' or target == 'swt-left-bottom-4':
        n_target = 'elite-left-bottom-2'
    elif target == 'swt-right-top-1' or target == 'swt-right-bottom-1':
        n_target = 'elite-right-top-1'
    elif target == 'swt-right-top-2' or target == 'swt-right-bottom-2':
        n_target = 'elite-right-bottom-1'
    elif target == 'swt-right-top-3' or target == 'swt-right-bottom-3':
        n_target = 'elite-right-top-2'
    elif target == 'swt-right-top-4' or target == 'swt-right-bottom-4':
        n_target = 'elite-right-bottom-2'

    html_content = f"""
    <button hx-get="/update_match_elite/{f_brkt_id}" hx-target="#{n_target}" hx-swap="outerHTML" hx-trigger="click"
            hx-params="id, title, artist, target"
            hx-vars="id: '{s_id}', title: '{esc_title}' , artist: '{esc_artist}', target: '{n_target}'"
            class="team" id="{target}">
        <div id="song_{s_id}"> {s_title} - {s_artist}</div>
    </button>
    """

    return HTMLResponse(content=html_content)


# Sweet match route to put winner into elite round match
@router.get("/update_match_elite/{f_brkt_id}", response_class=HTMLResponse)
async def update_match_elite(request: Request, f_brkt_id: int, db: Session = Depends(get_db_session),
                             user: int = Depends(auth_svc.get_user_id_via_auth_cookie)):

    if not user:
        return None

    # Start simple, don't worry about cascading changes from previous rounds into later rounds yet.
    s_id = request.query_params.get('id')
    s_title = request.query_params.get('title')
    s_artist = request.query_params.get('artist')
    target = request.query_params.get('target')
    a_song = {"song_id": s_id, "title": s_title, "artist": s_artist}

    update_bracket_winners = bracket_svc.save_bracket_data(db, f_brkt_id, target, a_song)

    if update_bracket_winners is False:
        return None

    esc_title = bracket_svc.handle_stupid_chars(s_title)
    esc_artist = bracket_svc.handle_stupid_chars(s_artist)

    # targets - elite 8 left top 1, elite 8 left bottom 1, elite 8 left top 2, elite 8 left bottom 2, repeat for right
    n_target = ''
    if target == 'elite-left-top-1' or target == 'elite-left-bottom-1':
        n_target = 'semi-final-left-top'
    elif target == 'elite-left-top-2' or target == 'elite-left-bottom-2':
        n_target = 'semi-final-left-bottom'
    elif target == 'elite-right-top-1' or target == 'elite-right-bottom-1':
        n_target = 'semi-final-right-top'
    elif target == 'elite-right-top-2' or target == 'elite-right-bottom-2':
        n_target = 'semi-final-right-bottom'

    html_content = f"""
    <button hx-get="/update_match_semifinal/{f_brkt_id}" hx-target="#{n_target}" hx-swap="outerHTML" hx-trigger="click"
            hx-params="id, title, artist, target"
            hx-vars="id: '{s_id}', title: '{esc_title}' , artist: '{esc_artist}', target: '{n_target}'"
            class="team" id="{target}">
        <div id="song_{s_id}"> {s_title} - {s_artist}</div>
    </button>
    """

    return HTMLResponse(content=html_content)


# Elite match route to put winners into semi-final round match
@router.get("/update_match_semifinal/{f_brkt_id}", response_class=HTMLResponse)
async def update_match_semifinal(request: Request, f_brkt_id: int, db: Session = Depends(get_db_session),
                                 user: int = Depends(auth_svc.get_user_id_via_auth_cookie)):

    if not user:
        return None

    # Start simple, don't worry about cascading changes from previous rounds into later rounds yet.
    s_id = request.query_params.get('id')
    s_title = request.query_params.get('title')
    s_artist = request.query_params.get('artist')
    target = request.query_params.get('target')
    a_song = {"song_id": s_id, "title": s_title, "artist": s_artist}

    update_bracket_winners = bracket_svc.save_bracket_data(db, f_brkt_id, target, a_song)

    if update_bracket_winners is False:
        return None

    esc_title = bracket_svc.handle_stupid_chars(s_title)
    esc_artist = bracket_svc.handle_stupid_chars(s_artist)

    n_target = ''
    if target == 'semi-final-left-top' or target == 'semi-final-left-bottom':
        n_target = 'finals-top'
    elif target == 'semi-final-right-top' or target == 'semi-final-right-bottom':
        n_target = 'finals-bottom'

    html_content = f"""
    <button hx-get="/update_match_final/{f_brkt_id}" hx-target="#{n_target}" hx-swap="outerHTML" hx-trigger="click"
            hx-params="id, title, artist, target"
            hx-vars="id: '{s_id}', title: '{esc_title}' , artist: '{esc_artist}', target: '{n_target}'"
            class="team" id="{target}">
        <div id="song_{s_id}"> {s_title} - {s_artist}</div>
    </button>
    """

    return HTMLResponse(content=html_content)


# Semi-final match route to put winners into finals round match
@router.get("/update_match_final/{f_brkt_id}", response_class=HTMLResponse)
async def update_match_final(request: Request, f_brkt_id: int, db: Session = Depends(get_db_session),
                             user: int = Depends(auth_svc.get_user_id_via_auth_cookie)):

    if not user:
        return None

    s_id = request.query_params.get('id')
    s_title = request.query_params.get('title')
    s_artist = request.query_params.get('artist')
    target = request.query_params.get('target')
    a_song = {"song_id": s_id, "title": s_title, "artist": s_artist}

    update_bracket_winners = bracket_svc.save_bracket_data(db, f_brkt_id, target, a_song)

    if update_bracket_winners is False:
        return None

    esc_title = bracket_svc.handle_stupid_chars(s_title)
    esc_artist = bracket_svc.handle_stupid_chars(s_artist)

    html_content = f"""
    <button hx-get="/update_champion/{f_brkt_id}" hx-target="#champion-team" hx-swap="outerHTML" hx-trigger="click"
            hx-params="id, title, artist"
            hx-vars="id: '{s_id}', title: '{esc_title}', artist: '{esc_artist}'"
            class="team" id="{target}">
        <div id="song_{s_id}"> {s_title} - {s_artist}</div>
    </button>
    """

    return HTMLResponse(content=html_content)


# Finals match route to put winner into champion
@router.get("/update_champion/{f_brkt_id}", response_class=HTMLResponse)
async def update_champion(request: Request, f_brkt_id: int, db: Session = Depends(get_db_session),
                          user: int = Depends(auth_svc.get_user_id_via_auth_cookie)):

    if not user:
        return None

    s_id = request.query_params.get('id')
    s_title = request.query_params.get('title')
    s_artist = request.query_params.get('artist')
    target = "champion-team"
    a_song = {"song_id": s_id, "title": s_title, "artist": s_artist}

    update_bracket_winners = bracket_svc.save_bracket_data(db, f_brkt_id, target, a_song)

    if update_bracket_winners is False:
        return None

    html_content = f"""
    <div class="team" id="song_{s_id}"> {s_title} - {s_artist}</div>
    """

    return HTMLResponse(content=html_content)


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
