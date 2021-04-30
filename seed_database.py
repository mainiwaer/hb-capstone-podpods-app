"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime
from faker import Faker

import crud
import model
import server

fake = Faker()

os.system('dropdb pod')
os.system('createdb pod')

model.connect_to_db(server.app)
model.db.create_all()

REVIEW_TEXT = [
    "Really fun and informative podcast!",
    "I feel like there aren't enough cats in this podcast...",
    "THANK you to this podcast for existing, I commute 8 hours \
        a day to ub*rmelon hq and I would be a mess without it",
    "The star war would of been a dream",
    "LOLLLLL this is so funny I'm gonna tell all my friends"
]


with open('data/mock_podcast.json') as f:
    test_podcast_data = json.loads(f.read())

podcasts_in_db = []

for podcast in test_podcast_data:
    podcast_id, title, cover = (podcast['id'],
                                podcast['title'],
                                podcast['cover'])

    db_podcast = crud.create_podcast(podcast_id=podcast_id,
                                     title=title,
                                     cover=cover)

    podcasts_in_db.append(db_podcast)

all_users = []

for n in range(10):

    username = fake.simple_profile()['username']
    email = f'{username}@podcast.com'
    password = 'rest'
    created_on = datetime.now()
    profile_picture = '/static/images/anon_whale.png'
    user_bio = fake.sentence(nb_words=50)
    website = fake.profile()['website']
    birthday = fake.profile()['birthdate']

    new_user = crud.create_user(username,
                                email,
                                password,
                                created_on,
                                profile_picture,
                                user_bio,
                                website,
                                birthday)

    all_users.append(new_user)

    for p in range(5):
        random_podcast = choice(podcasts_in_db)
        score = randint(1, 5)
        review_text = fake.sentence(nb_words=80)
        crud.create_review(new_user, random_podcast, review_text, score)

    new_collection = crud.create_collection(new_user, "Top Favs")
    second_new_collection = crud.create_collection(new_user, "Informative")
    collects = [new_collection, second_new_collection]

    for collect in collects:

        for r in range(5):
            random_podcast = choice(podcasts_in_db)
            crud.add_to_podcast_collection(collect,
                                           random_podcast)


for user in all_users:
    crud.become_friends(user.user_id, choice(range(9)))
