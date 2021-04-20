"""CRUD operations."""

from model import db, User, Podcast, Review, Collection
from model import CollectionPodcasts, connect_to_db

if __name__ == '__main__':
    from server import app
    connect_to_db(app)


def create_user(username, email, password, created_on):
    """Create and return a new user."""

    user = User(username=username,
                email=email,
                password=password,
                created_on=created_on)

    db.session.add(user)
    db.session.commit()

    return user


def get_user_by_username(username):
    """Return a user by username."""

    return User.query.filter(User.username == username).first()


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()


def check_user_password_by_email(email, password):
    """Check if the password associated with the email is correct."""

    user = get_user_by_email(email)
    user_password = user.password

    return user_password == password


def create_podcast(podcast_id, title):
    """Create and return a new podcast."""

    podcast = Podcast(podcast_id=podcast_id,
                      title=title,)

    db.session.add(podcast)
    db.session.commit()

    return podcast


def get_podcast_by_id(podcast_id):
    """Return a Podcast by its id."""

    return Podcast.query.filter(Podcast.podcast_id == podcast_id).first()


def get_hot_pods():
    """Returns list of hot podcasts."""

    return Podcast.query.all()


def get_reviews_by_podcast_id(podcast_id):
    """Return a review by podcast id."""

    return Review.query.filter(Review.podcast_id == podcast_id).all()


def create_review(user, podcast, review_text, score):

    review = Review(user=user,
                    podcast=podcast,
                    review_text=review_text,
                    score=score)

    db.session.add(review)
    db.session.commit()


def create_collection(user_collection, name):
    """Creates a collection of podcasts for a user."""

    collect = Collection(user_collection=user_collection, name=name)

    db.session.add(collect)
    db.session.commit()

    return collect


def add_to_podcast_collection(collection, podcast):
    """Adds podcasts to a user's podcast collection."""

    collection_podcasts = CollectionPodcasts(collection=collection,
                                             podcast=podcast)

    db.session.add(collection_podcasts)
    db.session.commit()
