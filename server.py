"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, redirect)

from model import connect_to_db

from datetime import datetime

import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = b'\x0c\xc8#\xf1TCJ\xfa\xa3F\xfc\x9e\xf4{\xe6\xd7'
app.jinja_env.undefined = StrictUndefined 

@app.route('/')
def show_homepage():
    """View homepage."""

    return render_template('homepage.html')

@app.route('/hot')
def show_hot_podcasts():
    """View current popular podcasts."""

    podcasts = crud.get_hot_pods()

    return render_template('hot_podcasts.html', podcasts=podcasts)

@app.route('/signup')
def show_sign_up_page():
    """View sign up page."""

    return render_template('sign_up.html')

@app.route('/users', methods=['POST'])
def register_user():
    """Create a new user."""
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    created_on = datetime.now()

    username_check = crud.get_user_by_username(username)
    email_check = crud.get_email_by_username(email)

    if username_check:
        flash('Sorry, that username is already taken. Try again.')
        return redirect('/signup')

    elif email_check:
        flash('An account with that email already exists. Try again.')
        return redirect('/signup')

    else:
        crud.create_user(username, email, password, created_on)
        flash('Account created!')
        return redirect('/user-profile')


@app.route('/user-profile')
def show_user_profile():
    """Render profile page of user that is logged in."""

    return render_template('user_profile.html')

# @app.route('/search')
# def show_search_results():
#     """Shows podcast search results."""
    
#     q = request.args.get('search', '') 


#     data = response.json()
#     search_results = data['results']['items']


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)


