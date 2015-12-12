# Kid-O

[![Build Status](https://travis-ci.org/vanesa/kid-o.svg?branch=master)](https://travis-ci.org/vanesa/kid-o)

<img src="app/static/images/kid-ologo.png" width="50%"" alt="Kid-O">

Kid-O helps Non-Profit children’s aid orgs keep an overview of their children.  

##### Winner of C-Base Hack 'N Tell HACK OF THE MONTH PRIZE

Check out my [LinkedIn](https://www.linkedin.com/in/vanesaortiz) profile for more information on my experience, education, and projects.

### Contents

- [Overview](#overview)
- [Technologies & Stack](#technologies-and-stack)
- [Features](#features)
	- [In-depth use cases](#in-depth-use-cases)
- [Future plans](#future-plans)
- [Technical choices](#technical-choices)
- [Screenshots](#screenshots)
- [Forking](#forking)


Overview
----------------

Kid-O solves these common problems for aid workers:
* keeping accurate and up-to-date information about each child in a central sharable CMS
* managing child profiles without internet access (via SMS)
* structures a child's information in an easily editable format
* organizes information such as name, age, home situation, etc.
* makes it easy to visualize a child's home location on a map even when no address is available

Kid-O will be tested in October 2015 by the children's aid project [Dominiño](http://www.dominino.de) in the Dominican Republic.



Technologies and stack
------------------------

#### Backend
Python, Flask, SQLAlchemy, PostgreSQL

Flask extensions: Flask-Login, Flask-Bcrypt, Flask-WTForms, Flask-SQLAlchemy.

Testing: unittest.

#### Frontend:
JavaScript, jQuery, Jinja2.
HTML5, CSS3, Twitter Bootstrap (html/css/js framework), RWD (responsive web design).

#### APIs:
Mapbox.js(OpenStreetMaps), Twilio.

Features
-------------------

- [x] Shows children's profiles

- [x] Previews and uploads images

- [x] Saves new or updated home location data from the map into the database and show it on the map.

- [x] Flask app routes requests to the database and manages form validation via Flask-WTForms.

- [x] Enables search by first-, last-, both names or part of the name.


##### Security with Bcrypt and Flask-Login
- [x] Encrypt and verify user passwords using hashes.

- [x] Secure user sessions let users stay logged in.


##### APIs
- [x] Twilio API integration allows users to create new child profiles through a text message, including the photo of the child(through MMS). No internet is required.


##### Data visualization and interaction
- [x] Shows what information is missing from the child's profile in the overview page.

- [x] Requests missing information in the child's profile.

- [x] Child's home location shown and editable on a map.

- [x] Child's age is calculated from their birth date.

- [x] Users can preview the image that will be uploaded to the child's profile.

- [x] Custom responsive web design (RWD) using CSS3.


### In-depth use cases

#### Overview page
- List's a short preview of the children's profiles
- Icons are displayed in green or red depending on what information in the child's profile is filled out or if there is information missing
- The heading title bar displays in green or red depending on available information
- The search function can search for any part of the child's name and stays fixed to the top side of the page for accessibility
- The "add child" button on the top right of the page makes it easy to add a new child to Kid-O
- Bottom navigation stays fixed for easier accessibility


#### Child page
- Shows the child's information in a structured, editable format
- When adding or editing a child's profile, the selected photo of the child is displayed as a preview on the page.
- If a photo of the child is missing, Kid-O displays a standard image.
- If information is missing, Kid-O displays requests to fill out the missing info on the profile pages.
- Child's age is calculated from their birth date.

#### Users can:
- Sign in/sign out/sign up (create an account)
- Add a child profile to Kid-O. They can add basic information such as name, birth date, the child's guardian name, home situation etc.
- Edit a child's profile
- Add the child's home location on a map
- Update the child's home location
- Search for a child on the search form at the top of the page
- Add a child's profile through SMS/MMS including the child's photo


Future plans
-----------------------
##### Adding more children
I limited the number of children in the app for development purposes, but in order to fully test the app in the Dominican Republic, I will seed the current 140 children who are being served to the database. By October, more children will have joined the project. The Dominiño aid workers can then create these new profiles, either through text message, or through the web app.

##### Verify existence of child when creating a new profile
Currently, the existence of the child been added to Kid-O is not verified. I plan to warn the user with a popup suggesting a possible child if the new child's name is similar to an existing child in the system.

##### Upload child photos to Amazon S3
For demo purposes, I save the photos of the children on my hard disk. I plan to upload them to Amazon S3.

##### Lazy Load
In order to limit the use of data, I want to include a Lazy Load to only preview a certain amount of children's profiles at a time.

##### Alerts for upcoming appointments/due updates
I plan to use the Twilio API to send a text message to the aid workers when a doctors appointment for a child is coming up or a home visit is due.
I also want the aid workers to receive an email when a child's profile has not been updated for a specific amount of months.

##### Additional security
To prevent brute-force hacking attempts, I will add an increasing time delay after multiple failed login attempts. 

##### Monitor which user edited which child's profile
Allow users to see their stats on their user profile pages, e.g. how many updates they have made, which child profile they last worked on, etc.  

##### Real time updates
Currently, the page must be refreshed to show updated children's profiles. This should be updated to happen in real-time with server-sent events.



Technical choices
-----------------------

##### Security
In any login system, security is important. I wanted to ensure that user passwords couldn't be stolen, especially considering that most people re-use their passwords all over the place (despite warnings against such a practice). Bcrypt offers a simple but effective encryption and verification system using hashes, requiring only a few lines of code.  

I chose Flask-Login to manage secure user sessions when they login. This Flask extension is well-known, well-documented, reliable, and offers exactly what I needed to implement that feature.  

##### PostgreSQL
I chose to use PostgreSQL to make use of the powerful SQLAlchemy ORM and ensure scalability.

##### Flask-WTForms
Partway through the project, I discovered Flask-WTForms, a Flask extension that offers form creation and validation. I switched to this method for all future forms on the site because of its simple and effective form management and validation options.

##### OpenStreetMaps
My app will be deployed for the Non-Profit  Dominiño in the Dominican Republic. For this reason, I decided to use OpenStreetMaps instead of Google Maps, since OpenStreetMaps offers much better coverage of the infrastructure in the Dominican Republic than Google Maps. 

##### Custom CSS
Using CSS3, I customized the checkboxes and select dropdowns.  I didn't like their default appearances, and wanted to change their colors and styles to better match that of the website. 

I used Bootstrap for certain things, like button shapes and the navbar, but found its responsive elements restrictive.  Because of this, I custom coded all the responsive design seen on the site (with the exception of the navbar).

##### JQuery
I used JQuery to dynamically shrink the navbar header on scroll by adding a CSS class to the nav element. I also used JQuery to allow the user to drop a pin on the home location of the child in the map.

##### Code structure

All my routes are in one file, views.py, and my database models are in a separate models.py file. I dabbled with child base views in child.py.
The Twilio API-related route is at the bottom of views.py.

For JavaScript, I separated the map JS, but had to include the code for editing the map into the html, in order to use Jinja2 for the coordinates. I separated the JS for the overview page in overview.js as it doesn't interact with the other JS.

On the overview page, I used Jinja to show alerting icons depending on what information is missing in the children's profile. 
The users are also asked to fill out missing information in the child's profile page.
On the frontend, rather than recode my nav bar for every web page, I used Jinja templates to simplify the process by extending from a base.html file that contains the nav bar.

Screenshots
-----------------------

###### Overview of the children
![Overview of the children](screenshots/overview1.jpg "Children's overview")

###### Display of missing information on the child profile preview
![Display of missing information on the child profile preview](screenshots/overview2.jpg "Missing Info")


###### Child profile
![Child profile](screenshots/childprofile.jpg "Child profile")



###### Add child profile
![Add child profile](screenshots/addchildprofile.jpg "Add child profile")



###### Edit child profile
![Edit child profile](screenshots/editchildprofile.jpg "Edit child profile")


###### Search function
![Search](screenshots/search.jpg "Search child profile")


###### Map
![Map](screenshots/map.jpg "Display children's home location on a map")


###### Login
![Login](screenshots/login.jpg "Login")


###### Signup with form validation
![Sign up](screenshots/signup.jpg "Sign up with form validation")


Forking?
-----------------------
You'll need your own API keys for Twilio!

	pip install -r requirements.txt

	python run.py
