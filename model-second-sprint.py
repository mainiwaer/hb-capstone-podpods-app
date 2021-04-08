"""Models for movie ratings app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String)
    email = db.Column(db.String)
    created_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'User id={self.user_id} username={self.username}'

class Podcast(db.Model):
    """A podcast."""

    __tablename__ = 'podcasts'

    podcast_id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)
    name = db.Column(db.String)
    website = db.Column(db.String)
    cover = db.Column(db.String)
    language = db.Column(db.String)
    explicit_content = db.Column(db.Boolean)
    number_of_eps = db.Column(db.Integer)

    def __repr__(self):
        return f'Podcast id={self.podcast_id} name={self.name}'

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

# class Podcaster(db.Model):
#     """A back-end user, can access and edit podcast pages."""

#     podcaster_id = db.Column(db.Integer,
#                    autoincrement=True,
#                    primary_key=True)

# class Host(db.Model):
#     """A podcast host."""

#     host_id = db.Column(db.Integer,
#                    autoincrement=True,
#                    primary_key=True)

# class PodcastHost(db.Model):
#     """"""

#     podcast_host_id = db.Column(db.Integer,
#                    autoincrement=True,
#                    primary_key=True)
#     podcast_id = db.Column(db.Integer,
#                            db.ForeignKey('podcast.podcast_id'),
#                            nullable=False)


# class PodcastEpisodes(db.Model):
#     """"""

#     podcast_episode_id = db.Column(db.Integer,
#                    autoincrement=True,
#                    primary_key=True)

# class Collection(db.Model):
#     """"""

#     collection_id = db.Column(db.Integer,
#                    autoincrement=True,
#                    primary_key=True)


# class PodcastCaster(db.Model):
#     """"""

#     podcast_caster_id = db.Column(db.Integer,
#                    autoincrement=True,
#                    primary_key=True)

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
