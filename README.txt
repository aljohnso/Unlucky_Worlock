This is the code for the POA website it contains the following:
├── app.wsgi
	-Web server gateway interface IE an nightmare to deal with
├── POA_Website
	-This is the main directory where all code lives
│   ├── bin
	-This is where the Live DB lives
│   │   └── POA.db
│   ├── DatabaseConnection
	-This class handles all database interactions
│   │   ├── DatabaseConnection.py
		-Implementation and interface of the Database interactions 
│   │   ├── Database.py
		-Initializes Database 
│   │   ├── DatabaseSubmissionConstructors.py
		-Takes in form data and process it to be submitted to the database 
│   │   ├── __init__.py
│   ├── Documentation
	-Explains how things work
│   │   ├── DatabaseConnection.txt
│   │   ├── Forms.txt
│   │   └── Setting Up Website Hosting On AWS EC2.txt
│   ├── Forms
	-Implementations of forms for web interface with validation
│   │   ├── __init__.py
│   │   ├── POAForms.py
│   ├── Pitzer_Outdoor_Adventure
	-Where heart of app lives contains the routes for web traffic 
│   │   ├── Admin
	-Will contain all admin controls
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── Main
	-Contains all routes not requiring authentication
│   │   │   ├── controllers.py
│   │   │   ├── __init__.py
│   │   │   └── templates
│   │   │       ├── Add_Particpant.html
│   │   │       ├── CreateTrip.html
│   │   │       ├── HomePage.html
│   │   │       └── TripPage.html
│   ├── POA.db

    
