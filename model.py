"""Models for movie ratings app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

######################################################################

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

    def __repr__(self):
        return f'User id={self.user_id} username={self.username}'


class Podcast(db.Model):
    """A podcast."""

    __tablename__ = 'podcasts'

    podcast_id = db.Column(db.Integer,
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
    podcast_id = db.Column(db.Integer,
                           db.ForeignKey('podcasts.podcast_id'),
                           nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)

    podcast = db.relationship('Podcast', backref='reviews')
    user = db.relationship('User', backref='reviews')

    def __repr__(self):
        return f'Review id={self.review_id} score={self.score}'

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

