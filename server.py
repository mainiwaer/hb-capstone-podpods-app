"""Server for movie ratings app."""

import requests

from flask import (Flask, request, render_template,
                   flash, session, redirect, Markup)

from model import connect_to_db

from datetime import datetime

import crud

import os

from jinja2 import StrictUndefined

os.system("source secrets.sh")

app = Flask(__name__)
app.secret_key = b'\x0c\xc8#\xf1TCJ\xfa\xa3F\xfc\x9e\xf4{\xe6\xd7'
app.config['TEMPLATES_AUTO_RELOAD'] = True

# os.environ["FLASK_KEY"]

app.jinja_env.undefined = StrictUndefined

API_KEY = os.environ["LISTENNOTES_KEY"]


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
    """Show user sign up page."""

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
        flash(Markup('Account created! Please \
                     <a href="/signin"class="alert-link">Sign In</a>'))
        return redirect('/signup')


@app.route('/signin')
def show_sign_in_page():
    """Show user sign in page."""

    return render_template('sign_in.html')


@app.route('/signin', methods=['POST'])
def sign_user_in():
    """Sign user into website."""

    email = request.form['email']
    pw = request.form['password']

    email_check = crud.get_user_by_email(email)

    if email_check is None:

        flash(Markup('A user with this email does not exist. \
                    Please try again or <a href="/signup"class="alert-link">\
                    Sign Up For An Account</a>'))
        return redirect('/signin')

    pw_check = crud.check_user_password_by_email(email, pw)

    if pw_check:
        session['email'] = email
        session['username'] = crud.get_user_by_email(email).username
        return redirect('/user-profile')
    else:
        flash('Incorrect password. Please try again.')
        return redirect('/signin')


@app.route('/user-profile')
def show_user_profile():
    """Render profile page of user that is logged in."""

    if session.get('username', 0) == 0:
        return redirect('/signin')

    user = session['username']
    email = session['email']
    account = crud.get_user_by_email(email)
    user_reviews = account.reviews
    user_collections = account.collections

    user_collections_pods = {}

    session['collections'] = {}

    for collection in user_collections:

        session['collections'][collection.collection_id] = collection.name

        collection_pods = []

        for pod in collection.collection_podcasts:
            pod_object = crud.get_podcast_by_id(pod.podcast_id)
            collection_pods.append(pod_object)

        user_collections_pods[collection.name] = collection_pods

    return render_template('user_profile.html',
                           user=user,
                           email=email,
                           reviews=user_reviews,
                           collections=user_collections,
                           collections_details=user_collections_pods)


@app.route('/user/<username>')
def show_other_user_profile(username):
    """Show the user profile of other registered users"""

    account = crud.get_user_by_username(username)
    reviews = account.reviews
    collections = account.collections

    collection_names = {}
    collections_pods = {}

    for collection in collections:

        collection_names[collection.collection_id] = collection.name

        collection_pods = []

        for pod in collection.collection_podcasts:
            pod_object = crud.get_podcast_by_id(pod.podcast_id)
            collection_pods.append(pod_object)

        collections_pods[collection.name] = collection_pods

    return render_template('other_users.html',
                           user=username,
                           reviews=reviews,
                           collections=collections,
                           collections_details=collections_pods)


@app.route('/search')
def show_search_results():
    """Show first 10 podcasts based on a keyword search"""

    if request.args.get('search-type', '') == 'podcast-search':

        keyword = request.args.get('q', '')

        url = 'https://listen-api.listennotes.com/api/v2/search'

        headers = {'X-ListenAPI-Key': API_KEY}

        payload = {'q': keyword, 'type': 'podcast'}

        response = requests.request('GET', url,
                                    headers=headers,
                                    params=payload)

        search_result = response.json()['results']

        return render_template('search_results.html',
                               result=search_result)

    if request.args.get('search-type', '') == 'user-search':

        search_term = request.args.get('q', '')

        results = crud.search_for_user(search_term)

        if not results:

            results = 'no users'

            return render_template('user_search.html',
                                   results=results)

        else:
            users = []

            for obj in results:

                month_year = obj.created_on.strftime("%B %Y")

                user = {'username': obj.username,
                        'created_on': month_year}
                users.append(user)

            return render_template('user_search.html',
                                   results=users)


@app.route('/podcast/<id>')
def show_podcast_details(id):
    """Show details on podcast as well as reviews"""

    url = f'https://listen-api.listennotes.com/api/v2/podcasts/{id}'

    headers = {'X-ListenAPI-Key': API_KEY}

    response = requests.request('GET', url, headers=headers)
    pod = response.json()
    explicit_tag = pod['explicit_content']

    reviews = crud.get_reviews_by_podcast_id(id)

    if explicit_tag:
        tag = 'Yes'
    else:
        tag = 'No'

    if session:
        collections = session['collections']
    else:
        collections = None

    return render_template('podcast_details.html',
                           podcast=pod,
                           explicit=tag,
                           reviews=reviews,
                           collections=collections)


@app.route('/review', methods=['POST'])
def submit_podcast_review():
    """Create user submitted review."""

    email = request.form['user-email']
    podcast_id = request.form['podcast-id']
    podcast_name = request.form['podcast-title']
    score = request.form['score']
    review = request.form['review-text']

    if email == 'no user':
        flash('Please sign in to leave a review.')
        return redirect(f'/podcast/{podcast_id}')

    if crud.get_podcast_by_id(podcast_id) is None:
        crud.create_podcast(podcast_id, podcast_name)

    user = crud.get_user_by_email(email)
    podcast = crud.get_podcast_by_id(podcast_id)

    crud.create_review(user, podcast, review, score)

    flash('Thank you for leaving a review!')

    return redirect(f'/podcast/{podcast_id}')


@app.route('/addcollection', methods=['POST'])
def create_new_collection():
    """Adds a new collection for the user."""

    user_collection = session['collections']
    name = request.form['collection-name']

    crud.create_collection(user_collection, name)


@app.route('/logout')
def log_user_out():
    """Logs user out of their account."""

    session.clear()
    flash('You have been signed out.')
    return redirect('/')


@app.before_request
def before_request():
    if 'localhost' in request.host_url or '0.0.0.0' in request.host_url:
        app.jinja_env.cache = {}


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
