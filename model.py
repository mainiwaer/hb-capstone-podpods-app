"""Models for movie ratings app."""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

######################################################################


class Collection(db.Model):
    """A user's collection of podcasts."""

    __tablename__ = 'collections'

    collection_id = db.Column(db.Integer,
                              autoincrement=True,
                              primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)

    name = db.Column(db.String)

    user_collection = db.relationship('User', backref='collections')

    def __repr__(self):
        return f'Collection id={self.collection_id} name={self.name}'


class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String)
    email = db.Column(db.String)
    created_on = db.Column(db.DateTime)

    pod_collection = db.relationship("Collection", backref='users')

    def __repr__(self):
        return f'User id={self.user_id} username={self.username}'


class Podcast(db.Model):
    """A podcast."""

    __tablename__ = 'podcasts'

    podcast_id = db.Column(db.String,
                           primary_key=True)
    title = db.Column(db.String)

    def __repr__(self):
        return f'Podcast id={self.podcast_id} name={self.title}'


class Review(db.Model):
    """A review."""

    __tablename__ = 'reviews'

    review_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    score = db.Column(db.Integer)
    review_text = db.Column(db.Text)
    podcast_id = db.Column(db.String,
                           db.ForeignKey('podcasts.podcast_id'),
                           nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)

    podcast = db.relationship('Podcast', backref='reviews')
    user = db.relationship('User', backref='reviews')

    def __repr__(self):
        return f'Review id={self.review_id} score={self.score}'


class CollectionPodcasts(db.Model):
    """The podcasts in a user's collection of podcasts."""

    __tablename__ = 'collection_podcasts'

    collection_podcasts_id = db.Column(db.Integer,
                                       autoincrement=True,
                                       primary_key=True)
    collection_id = db.Column(db.Integer,
                              db.ForeignKey('collections.collection_id'),
                              nullable=False)
    podcast_id = db.Column(db.String,
                           db.ForeignKey('podcasts.podcast_id'),
                           nullable=False)

    collection = db.relationship('Collection', backref='collection_podcasts')
    podcast = db.relationship('Podcast', backref='collection_podcasts')

    def __repr__(self):
        return f'CollectionPodcasts id={self.collection_podcasts_id}'


######################################################################


def connect_to_db(flask_app, db_uri='postgresql:///pod', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    connect_to_db(app)
