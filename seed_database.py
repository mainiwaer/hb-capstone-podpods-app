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
    podcast_data = json.loads(f.read())

podcasts_in_db = []

for podcast in podcast_data:
    title, description, website, cover, = (podcast['title'],
                                           podcast['description'],
                                           podcast['website'],
                                           podcast['thumbnail'])
    
    language, explicit_content, total_episodes = (podcast['language'],
                                                  podcast['explicit_content'],
                                                  podcast['total_episodes'])

    db_podcast = crud.create_podcast(title=title,
                                     description=description,
                                     website=website,
                                     cover=cover,
                                     language=language,
                                     explicit_content=explicit_content,
                                     total_episodes=total_episodes)
    
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