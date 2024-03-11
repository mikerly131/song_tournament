# About Bracket Voter Simple
A python web app to create tournaments to decide which song is best, bracket style.

## Built Using
- FastAPI web framework
- Postgresql DB connected with SQLAlchemy 2.0
- Vanilla JS scripts
- Jinja2 HTML templates
- HTMX to make templates dynamic
- Bootstrap CSS (CDN)

## Status
Users are able to:
* Create account, login and logout.
* Create an 8, 16, 32 or 64 song tournament, and fill out the title and artist for each contestant.
* View the tournaments that have been created.
* View your own and others filled out brackets for tournaments.
* Fill out a bracket for an 8, 16, 32 or 64 song tournament
  * Your own and other users.
  * Every selection of a match winner is saved as it is made.

Features being worked on:
* My Account page, to view summary or list of tournaments you created, and brackets you filled out

Known issue:
* Refreshing page while filling it out resets all choices, possible created new bracket entry. Don't refresh right now.
* Going back in the middle of filling out a bracket does interesting things.


## Future Plans
Add some stats about tournaments:
* Give points to a song for each time its selected as a winner in a tournament
* Song Rank:  avg across brackets for tournament
Do some data analysis across tournaments:
* Most popular songs included in tournaments
* Most voted for songs