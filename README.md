# About Bracket Voter Simple
A python web app to create tournaments to decide which song is best, bracket style.

### Status
Users can create accounts, create tournaments  
Users can fill out a bracket for an 8 song tournament, winners get saved  
Users cannot do this for 16, 32, and 64 song tournaments yet  
Users cannot view their filled out brackets  
Users cannot view other's tournaments to fill out a bracket  


### Built Using
- FastAPI web framework
- Postgresql DB connected with SQLAlchemy 2.0
- Vanilla JS scripts
- Jinja2 HTML templates
- HTMX to make templates dynamic
- Bootstrap CSS (CDN)

### Issue Log
Issue 1:  Title and artist with special HTML characters are causing issues, apostrophes in this case.   
Failed Fix: Replacing the apostrophe with the escaped character code via function before passing data to the template.  
Failed Fix: Replacing the apostrophe in the first route handling HTMX trigger to populate next match
Resolved: Using a function to escape the special characters for HTMX vals but not display elements before returning HTML.

Issue 2:  Saving selected winners as choices are made by user or after all choices  
Failed Fix: Making the entire tournament bracket a form - every HTMX trigger submits all the data in the form.  
Didn't Try: Making each element with HTMX its own form, use hx-post or hx-put on all of them.  
Resolved (for now):  Using a function in route for each HTMX call to update a bracket.  

Issue 3: Winners not being saved to DB, can see query is not executing  
Resolved:  SQLAlchemy session doesn't know I changed mutable JSON object, need to flag the change to get update.  
