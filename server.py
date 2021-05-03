"""Server for movie ratings app."""

import requests

from random import choice

from flask import (Flask, request, render_template,
                   flash, session, redirect, Markup)

from model import connect_to_db

from datetime import datetime

import crud

import os

from jinja2 import StrictUndefined

os.system("source secrets.sh")

app = Flask(__name__)
os.environ["FLASK_KEY"]
app.secret_key = os.environ["FLASK_KEY"]
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.jinja_env.undefined = StrictUndefined

API_KEY = os.environ["LISTENNOTES_KEY"]


@app.route('/')
def show_homepage():
    """View homepage."""

    podcasts = crud.get_hot_pods()[0:5]
    first_pod = podcasts.pop(0)

    return render_template('homepage.html',
                           first_pod=first_pod,
                           podcasts=podcasts)


@app.route('/hot')
def show_hot_podcasts():
    """View current popular podcasts."""

    podcasts = crud.get_hot_pods()

    return render_template('hot_podcasts.html', podcasts=podcasts)


@app.route('/recommended')
def give_user_random_podcast_rec():
    """Give a user a random podcast recommendation based on their collection."""

    if session:
        if session['collections']:

            collection_list = sorted(session['collections'])

            random_collection_id = choice(collection_list)

            random_collection = crud.get_collection_by_id(random_collection_id)

            reference_pod_id = choice(random_collection.collection_podcasts).podcast_id

        else:
            reference_pod_id = choice(crud.get_hot_pods()).podcast_id

    else:
        reference_pod_id = choice(crud.get_hot_pods()).podcast_id

    url = f'https://listen-api.listennotes.com/api/v2/podcasts/{reference_pod_id}/recommendations?safe_mode=0'

    headers = {'X-ListenAPI-Key': API_KEY}

    response = requests.request('GET', url, headers=headers)

    results = response.json()['recommendations']

    return render_template('recommendations.html',
                           result=results)


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
    profile_picture = '/static/images/anon_whale.png'
    user_bio = ''
    website = ''
    birthday = datetime.now()

    username_check = crud.get_user_by_username(username)
    email_check = crud.get_user_by_email(email)

    if username_check:
        flash('Sorry, that username is already taken. Try again.')
        return redirect('/signup')

    elif email_check:
        flash('An account with that email already exists. Try again.')
        return redirect('/signup')

    else:
        crud.create_user(username,
                         email,
                         password,
                         created_on,
                         profile_picture,
                         user_bio,
                         website,
                         birthday)

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
        session['profile_picture'] = crud.get_user_by_email(email).profile_picture
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
    user_profile_picture = account.profile_picture
    user_bio = account.user_bio
    created_on = account.created_on
    birthday = account.birthday
    website = account.website

    user_friends = []
    user_friendships = account.added_friends
    for friendship in user_friendships:
        user_friend_id = friendship.friend_id
        friend_account = crud.get_user_by_user_id(user_friend_id)
        user_friends.append(friend_account)

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
                           birthday=birthday,
                           website=website,
                           profile_picture=user_profile_picture,
                           user_bio=user_bio,
                           friends=user_friends,
                           created_on=created_on,
                           collections=user_collections,
                           collections_details=user_collections_pods)


@app.route('/user/<username>')
def show_other_user_profile(username):
    """Show the user profile of other registered users"""

    account = crud.get_user_by_username(username)
    reviews = account.reviews
    collections = account.collections
    profile_picture = account.profile_picture
    user_bio = account.user_bio
    created_on = account.created_on
    user_id = account.user_id
    birthday = account.birthday
    website = account.website

    user_friends = []
    user_friendships = account.added_friends
    for friendship in user_friendships:
        user_friend_id = friendship.friend_id
        friend_account = crud.get_user_by_user_id(user_friend_id)
        user_friends.append(friend_account)

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
                           profile_picture=profile_picture,
                           birthday=birthday,
                           website=website,
                           user_bio=user_bio,
                           friends=user_friends,
                           created_on=created_on,
                           collections=collections,
                           collections_details=collections_pods,
                           profile_user_id=user_id)


@app.route('/addfriend', methods=['POST'])
def add_another_user_as_friend():
    """Adds another user as a friend."""

    friend_username = request.form['friend-username']
    user_email = request.form['user-email']
    friend_id = request.form['friend-id']

    current_user_id = crud.get_user_by_email(user_email).user_id

    crud.become_friends(current_user_id, friend_id)

    flash(f'You have become friends with {friend_username}!')

    return redirect(f'/user/{friend_username}')


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
                               result=search_result,
                               keyword=keyword)

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

    if reviews:
        reviews = reversed(reviews)

    if explicit_tag:
        tag = 'Yes'
    else:
        tag = 'No'

    if session:
        if session.get('collections', 0) == 0:
            collections = None
        else:
            collections = session['collections']
    else:
        collections = None

    return render_template('podcast_details.html',
                           podcast=pod,
                           explicit=tag,
                           reviews=reviews,
                           collections=collections)


@app.route('/genres')
def show_genre_page():
    """Shows user page of all genres."""

    genres = crud.get_genres()

    return render_template('all_genres.html',
                           genres=genres)


@app.route('/genre/<id>')
def show_podcasts_by_genre(id):
    """Shows user podcasts by selected genre."""

    url = f'https://listen-api.listennotes.com/api/v2/best_podcasts?genre_id={id}&page=1&region=us&safe_mode=0'

    headers = {'X-ListenAPI-Key': API_KEY}

    response = requests.request('GET', url, headers=headers)
    results = response.json()
    genre_name = results['name']
    podcasts = results['podcasts']

    return render_template('genre_results.html',
                           genre_name=genre_name,
                           podcasts=podcasts)


@app.route('/review', methods=['POST'])
def submit_podcast_review():
    """Create user submitted review."""

    email = request.form['user-email']
    podcast_id = request.form['podcast-id']
    podcast_name = request.form['podcast-title']
    cover = request.form['podcast-cover']
    score = request.form['score']
    review = request.form['review-text']

    if email == 'no user':
        flash('Please sign in to leave a review.')
        return redirect(f'/podcast/{podcast_id}')

    if crud.get_podcast_by_id(podcast_id) is None:
        crud.create_podcast(podcast_id, podcast_name, cover)

    user = crud.get_user_by_email(email)
    podcast = crud.get_podcast_by_id(podcast_id)

    crud.create_review(user, podcast, review, score)

    flash('Thank you for leaving a review!')

    return redirect(f'/podcast/{podcast_id}')


@app.route('/addtonewcollection', methods=['POST'])
def create_new_collection():
    """Adds a new collection for the user."""

    email = request.form['user-email']
    user = crud.get_user_by_email(email)

    name = request.form['new-collection-name']

    new_collection = crud.create_collection(user, name)

    podcast_id = request.form['podcast-id']
    podcast_name = request.form['podcast-title']
    podcast_cover = request.form['podcast-cover']

    if crud.get_podcast_by_id(podcast_id) is None:
        crud.create_podcast(podcast_id, podcast_name, podcast_cover)

    podcast = crud.get_podcast_by_id(podcast_id)

    crud.add_to_podcast_collection(new_collection, podcast)

    flash(f'Added {podcast_name} to {new_collection.name}!')

    redirect('/user-profile')

    return redirect(f'/podcast/{podcast_id}')


@app.route('/addtocollection', methods=['POST'])
def add_podcast_to_user_collections():
    """Adds a podcast to a user's collection"""

    collection_id = request.form['collection-id']
    podcast_id = request.form['podcast-id']
    podcast_name = request.form['podcast-title']
    podcast_cover = request.form['podcast-cover']

    if crud.get_podcast_by_id(podcast_id) is None:
        crud.create_podcast(podcast_id, podcast_name, podcast_cover)

    collection = crud.get_collection_by_id(collection_id)
    podcast = crud.get_podcast_by_id(podcast_id)

    crud.add_to_podcast_collection(collection, podcast)

    flash(f'Added {podcast_name} to {collection.name}!')

    return redirect(f'/podcast/{podcast_id}')


@app.route('/delete-review', methods=['POST'])
def delete_review():
    """Deletes user's review."""


@app.route('/remove-from-collection', methods=['POST'])
def remove_podcast_from_collection():
    """Removes a podcast from a user's collection."""


@app.route('/delete-collection', methods=['POST'])
def delete_collection():
    """Deletes a user's a collection"""


@app.route('/logout')
def log_user_out():
    """Logs user out of their account."""

    session.clear()
    flash('You have been signed out.')
    return redirect('/')


@app.route('/about')
def about_page():
    """Renders about page."""

    return render_template('about.html')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
