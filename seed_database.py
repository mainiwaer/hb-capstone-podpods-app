"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system('dropdb pod')
os.system('createdb pod')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/mock_podcast.json') as f:
    test_podcast_data = json.loads(f.read())

podcasts_in_db = []

for podcast in test_podcast_data:
    podcast_id, title = (podcast['id'],
                         podcast['title'])

    db_podcast = crud.create_podcast(podcast_id=podcast_id,
                                     title=title)
    
    podcasts_in_db.append(db_podcast)

for n in range(10):
    
    username = f'listener{n}'
    email = f'listener{n}@podcast.com'
    password = 'rest'
    created_on = datetime.now()

    user = crud.create_user(username, email, password, created_on)

    for p in range(10):
        random_podcast = choice(podcasts_in_db)
        score = randint(1, 5)
        review_text = 'the star war would of been a dream'
        crud.create_review(user, random_podcast, review_text, score)