# QSource

This project is the source code for a website hosted at: http://qsource.parksa2.webfactional.com/
Code authors: Lydia Nevin, Daryian Rhysing, Samuel Wenninger, Andrew Parks

QSource is a social media website for asking and responding to simple polls. Questions are displayed
and answered on a feed page with the option to sort by most recent or most votes, and the additional
option to display only questions asked by the current user. Results are revealed only after a user 
answers a question. Users can submit their own questions with the default Yes or No choices, or 
supply their own answer choices. 

To run a local version of this project on Django's lightweight development server, navigate to 
the parent directory of this file and type: 
python manage.py runserver

To run the automated tests, naviage to the parent directory of this file and type:
python manage.py test polls
python manage.py test qsource_user

The file structure of this project follows the Django conventions. Most of the important Python code 
is located in the following files (paths relative to this directory): 
polls/models.py
polls/views.py
qsource_user/models.py
qsource_user/views.py

The front-end runs on Bootstrap. Bootstrap files are included in this project as static files. 
The most important templates are:
polls/templates/polls/index.html
templates/base.html
templates/navbar.html
