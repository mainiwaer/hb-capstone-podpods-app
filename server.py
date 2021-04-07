"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, redirect)

from model import connect_to_db

import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = b'\x0c\xc8#\xf1TCJ\xfa\xa3F\xfc\x9e\xf4{\xe6\xd7'
app.jinja_env.undefined = StrictUndefined 

@app.route('/')
def show_homepage():
    """View homepage."""

    return render_template('homepage.html')




# @app.route('/search')
# def show_search_results():
#     """Shows podcast search results."""
    
#     q = request.args.get('search', '') 


#     data = response.json()
#     search_results = data['results']['items']


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)


