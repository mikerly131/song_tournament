# About Bracket Voter Simple
A python web app to create tournaments to decide which song is best, bracket style.

### Status
In-progress: Trying out HTMX to update bracket as filled out. 
Issue:  Title and artist with special HTML characters are causing issues, apostrophes in this case. 
Failed Fix: Replacing the apostrophe with the escaped character code via function before passing data to the template.
Failed Fix: Replacing the apostrophe in the first route handling HTMX trigger to populate next match

### Built Using
- FastAPI web framework
- Postgresql DB connected with SQLAlchemy 2.0
- Vanilla JS scripts
- Jinja2 HTML templates
- HTMX to make templates dynamic
- Bootstrap CSS (CDN)