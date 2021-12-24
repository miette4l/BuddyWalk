# CFG Project: BuddyWalk


BuddyWalk is a web app created by a group of CodeFirst Girls Nanodegree students for our final project on the course.

BuddyWalk responds to to a growing public mood of a lack of safety when walking alone the city. By pairing up lone walkers, BuddyWalk allows users to find safety in numbers. This buddy system is accompanied by an integrated mapping tool that clearly plots the users' journeys.

Installing / Getting started:
-----------------------------

BuddyWalk is a Flask web app, written in Python, and utilising MySQL. It currently runs with a Flask development server, but offers multiple-user support with a view to further development and deployment. The following steps are needed to get started and run BuddyWalk:

- Install all packages listed in 'requirements.txt'.

- Create a root directory file entitled 'config.py' to enable the MySQL connection, with the following global variables from your own MySQL server connection:  
    HOST = 'host'   
    USER = 'user'   
    PASSWORD = 'password'   

- Initialise the BuddyWalk database by running 'buddywalk_database.sql' in MySQL.

- Run 'src/app.py'.

BuddyWalk Demo Guide
--------------------

*Welcome to BuddyWalk!*

Where are you going?

...Wait. There are a few rules. 

- Your Current Location and Destination must be within a 10 mile radius of the official latitudinal and longitudinal centre of London! (We've constrained the range of our app for now.)
- Your Time of Departure mustn't be in the past, or more than 20 minutes from now.

Once you've inputted the details for the journey you want to make, click 'Submit'.

There will be silence, because you are the only user. This is a demo, remember.

To see how the app works, open an incognito or private browser window and input a similar journey. Under the hood, we are trying to match users with buddies who want to start and end their journeys within 1 mile of each other. You should receive a match and the details of your buddy! (Ahem... you, with a different username.)

Back on the other browser, where you started, click 'Check' and you should be presented with the match from the initial user's point of view.

The video below demonstrates the process of how the app would work for two different users.

BuddyWalk Demo Video
--------------------

Credits
-------

BuddyWalk was created by Verena Tiede, Claudia Bridgens, Holly Farler and Aishah Hussain.
