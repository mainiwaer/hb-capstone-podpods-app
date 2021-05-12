<p>![logo] ![logo] ![logo] ![logo] ![logo]</p>

PodPods: A Social Podcast Review Website 
===

PodPods is a full stack social podcast review application powered by the ListenNotes podcast API. A user can search for podcasts by name, see random recommendations, and look at popular podcasts by genre. The user can go to a podcast's page to see further details like episode counts, language, and a link to the podcast's homepage. The user can also listen to recent episodes within the app, and see reviews by other PodPods users.

After signing in, a user can also leave their own review or add the podcast to one of their collections. Users can search for other users and see their profiles, including their reviews, podcast collections, and bios. Adding a user to the friends list will populate their username on your own profile under "Your Pod Squad".

![sign_in]
![user_profile]
![podcast_details]
![signin]

# Technologies Used

Python, JavaScript, Flask, Jinja2, PostgreSQL, HTML, CSS, Bootstrap, ListenNotes API

# Frontend 

The PodPods frontend was build using the Bootstrap 5.0 framework and connected directly back to the python based server. Jinja2 templating is used across the html files. The navbar button hover effect was derived from __iamraviteja__ on codepen: https://codepen.io/iamraviteja/pen/PzboKd

# Backend

PodPods runs on a python-based server using a Flask framework (server.py). the database is managed via  SQLAlchemy data tables in model.py and is implemented by running seeding_database.py, with crud.py containing CRUD function used across the python files. The flask key and API key are stored in secrets.sh, which are not provided in this repository. 

# Miscellaneous

__Overview Presentation:__
<p>
<a href="http://www.youtube.com/watch?feature=player_embedded&v=wjypy_4cU9s
" target="_blank"><img src="http://img.youtube.com/vi/wjypy_4cU9s/0.jpg" 
alt="Youtube Link to PodPods Presentation" width="240" height="180" border="10" /></a>
<p>

[logo]: https://github.com/mainiwaer/hb-capstone-podpods-app/blob/master/static/images/pod_favicon_new.png 

[sign_in]:https://github.com/mainiwaer/hb-capstone-podpods-app/blob/master/static/images/sign-in.png
[user_profile]:https://github.com/mainiwaer/hb-capstone-podpods-app/blob/master/static/images/user-profile.png
[podcast_details]:https://github.com/mainiwaer/hb-capstone-podpods-app/blob/master/static/images/podcast-details.png
[signin]: https://github.com/mainiwaer/hb-capstone-podpods-app/blob/master/static/images/sign-in.png