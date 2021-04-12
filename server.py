"""Server for movie ratings app."""
import requests

from flask import (Flask, request, render_template, flash, session, redirect)

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
    email_check = crud.get_user_by_email(email)

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

# @app.route('/users', methods)


@app.route('/user-profile')
def show_user_profile():
    """Render profile page of user that is logged in."""

    return render_template('user_profile.html')

@app.route('/search')
def show_search_results():
    """Show first 10 podcasts based on a keyword search"""

    keyword = request.args.get('q', '')
    
    url = 'https://listen-api.listennotes.com/api/v2/search'

    headers = {'X-ListenAPI-Key': '46220315dbab4391b5efd8e27fcde507',}

    payload = {'q': keyword, 'type':'podcast'
    }

    response = requests.request('GET', url, headers=headers, params=payload)

    print(response)
    search_result = response.json()['results']

    return render_template('search_results.html',
                           result=search_result)

@app.route('/podcast/<id>')
def show_podcast_details(id):
    """Show details on podcast as well as reviews"""

    url = f'https://listen-api.listennotes.com/api/v2/podcasts/{id}'

    headers = {'X-ListenAPI-Key': '46220315dbab4391b5efd8e27fcde507',}


    response = requests.request('GET', url, headers=headers)
    pod = response.json()
    explicit_tag = pod['explicit_content']

    reviews = crud.get_reviews_by_podcast_id(id)

    if explicit_tag == True:
        tag = 'Yes'
    else:
        tag = 'No'

    return render_template('podcast_details.html',
                             podcast=pod,
                             explicit=tag,
                             reviews=reviews)

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)


