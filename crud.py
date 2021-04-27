"""CRUD operations."""

from model import db, User, Podcast, Review, Collection, UserFriendship
from model import CollectionPodcasts, connect_to_db

if __name__ == '__main__':
    from server import app
    connect_to_db(app)


def create_user(username, email, password, created_on, profile_picture, user_bio):
    """Create and return a new user."""

    user = User(username=username,
                email=email,
                password=password,
                created_on=created_on,
                profile_picture=profile_picture,
                user_bio=user_bio)

    db.session.add(user)
    db.session.commit()

    return user


def get_user_by_username(username):
    """Return a user by username."""

    return User.query.filter(User.username == username).first()


def search_for_user(search_term):
    """Return a list of users by search term."""

    return User.query.filter(User.username.like(f'%{search_term}%')).all()


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()


def get_user_by_user_id(user_id):
    """Return a user by user id."""

    return User.query.filter(User.user_id == user_id).first()


def check_user_password_by_email(email, password):
    """Check if the password associated with the email is correct."""

    user = get_user_by_email(email)
    user_password = user.password

    return user_password == password


def create_podcast(podcast_id, title, cover):
    """Create and return a new podcast."""

    podcast = Podcast(podcast_id=podcast_id,
                      title=title,
                      cover=cover)

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


# def get_users_friends(user_id):
#     """Return a list of the active user's friends."""

#     return User.query.filter(User.user_id == user_id).all()


def create_review(user, podcast, review_text, score):

    review = Review(user=user,
                    podcast=podcast,
                    review_text=review_text,
                    score=score)

    db.session.add(review)
    db.session.commit()

    return review


def create_collection(user_collection, name):
    """Creates a collection of podcasts for a user."""

    collect = Collection(user_collection=user_collection, name=name)

    db.session.add(collect)
    db.session.commit()

    return collect


def get_collection_by_id(collection_id):
    """Returns a collection by its id."""

    return Collection.query.filter(Collection.collection_id == collection_id).first()


def add_to_podcast_collection(collection, podcast):
    """Adds podcasts to a user's podcast collection."""

    collection_podcasts = CollectionPodcasts(collection=collection,
                                             podcast=podcast)

    db.session.add(collection_podcasts)
    db.session.commit()

    return collection_podcasts


def become_friends(user_id, friend_id):
    """Adds friendship with another user."""

    friendship_1 = UserFriendship(current_user_id=user_id,
                                  friend_id=friend_id)
    db.session.add(friendship_1)
    db.session.commit()

    friendship_2 = UserFriendship(current_user_id=friend_id,
                                  friend_id=user_id)
    db.session.add(friendship_2)
    db.session.commit()


def remove_friend(user_id, friend_id):
    """Removes friendship with another user"""

    to_remove_1 = db.session.query(UserFriendship).filter_by(current_user_id=user_id,
                                                             friend_id=friend_id).all()
    for friend in to_remove_1:
        db.session.delete(friend)
        db.session.commit()

    to_remove_2 = db.session.query(UserFriendship).filter_by(current_user_id=friend_id,
                                                             friend_id=user_id).all()
    for friend in to_remove_2:
        db.session.delete(friend)
        db.session.commit()
