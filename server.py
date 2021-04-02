"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, redirect)

from model import connect_to_db

# import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "\x0c\xc8#\xf1TCJ\xfa\xa3F\xfc\x9e\xf4{\xe6\xd7"
app.jinja_env.undefined = StrictUndefined 

@app.route('/')
def show_homepage():
    """Return homepage"""

    return render_template('homepage.html')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)


# url = 'https://listen-api.listennotes.com/api/v2/search?q=star%20wars&sort_by_date=0&type=episode&offset=0&len_min=10&len_max=30&genre_ids=68%2C82&published_before=1580172454000&published_after=0&only_in=title%2Cdescription&language=English&safe_mode=0'
# headers = {
#   'X-ListenAPI-Key': '442269846a724f61980e61d06c276edf',
# }
# response = requests.request('GET', url, headers=headers)
# print(response.json())