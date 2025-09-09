# Ngā Manu
#### Video Demo:  https://vimeo.com/841818386
#### Description:

“Ngā Manu” is a Flask web application to visualize maps with up-to-date bird sightings around New Zealand. It focuses on some of the country’s most remarkable and endangered, endemic bird species. This app leverages an API (Cornell University’s eBird) and a particular library (GMplot’s map generator) to work in conjunction with Flask, Python, SQL as well as HTML/CSS to make a user-friendly application.

I chose this for my project because as a Kiwi (New Zealander) who has been living abroad for longer than I’d like, I’ve come to be hugely proud and fond of our native bird species. From the unique-shaped Kiwi bird to the bizarre Kakapo parrot (who’s inopportune mating behavior you might have seen on BBC’s YouTube), they are quite fascinating! New Zealand’s geographical isolation has created a habitat which fostered the most interesting of mutations but sadly left these species extremely vulnerable upon to introduced mammal species like cats and stoats.

So out of love for these jewels of Aotearoa and a desire to promote their appreciation and conservation, I put together “Ngā Manu” which quite simply means “Birds” in Maori, the indigenous language of New Zealand.

#### eBird API
Let’s get into the weeds of the app. First, a bit about the API this application uses. Cornell’s eBird API allows users to pull up-to-date records of bird sightings from all over the world, submitted by scientists and bird watchers. The API offers data in the form of dictionaries with information like species, specimen count, date, time, location (eg. a place name, address, GPS coordinates or a mix of these) and the person who submitted them. Data can be requested by specifying the species, location and date.


#### Gmplot Library
This program uses the GMplot library, which allows users to plot data onto a Google Maps page. In the vein of matplotlib, by submitting a few parameters like GPS coordinates, labels and location names, you can generate interactive Google Maps pages which can then be used as HTML files that are recast each time they are called by a user of the app. This library requires a Google Maps Static API key to work.
You will need to pip install gmplot.


#### App.py
App.py is the main file for this app it is structured as follows:
First the libraries used by this program are imported (Flask, Datetime, CS50 (for SQL), Requests, Flask Sessions, Werkzeug.security and GMplot. Then the Flask app is initialized and configured along with the SQL database used by this app. Then we have the auxiliary helpers.py program.
#### Index
 Next, we initialize the route for each of the pages for our website. The first is the bare-bones index route which serves as our home page. From there we have the routes for each of the nine featured bird species and the notable sightings map pages.

### Kokako_sightings, etc.
These bird sightings map pages are the main focus of the program. They work by checking the method is a GET request, then providing a URL to pass to the API request. The data pull is handled by two functions from the helpers.py program that  “get _data” and  “extract” the data, passing in the url and tokens and getting a JSON file in return. The data is then checked for length and is looped through, appending as it goes the important data points to our lists (Latitudes, Longitudes, Locations and Species Names, etc.) which are then returned, ready to be plotted to a map.

These processed data lists are then passed to the GMplot library’s GoogleMapPlotter function, creating a Gmap object with GPS coordinates and the Google API key. As some bird species are seen all over the country while others are limited to the South Island (eg. Yellow-Eyed Penguin, Kea) or the North Island (North Island Kiwi), the coordinates passed to each route vary somewhat. The GMplot .scatter() function then plots all the sightings over the map, with the given labels (Species name) and title (location name). Lastly the gmplot.draw() function generates a full HTML file with the desired Google Maps page, which can be zoomed in and out of, viewed as a map or satellite view, etc.

Note: Some species are so rarely sighted due to their endangered status or seasonal/migratory reasons that they are prepared with hard coded error messages and return the apology page if the call returns no recent sightings. I was pleased to note that from the beginning of this project, up until the last few days there were no Yellow-Eyed Penguin sightings at all and then at the last moment about 4 animals were sighted in just a few days.

### Notable_sightings
Next we have our Notable Sightings route which works just the same as the individual species routes but, instead of a single species, returns a collection of sightings of species considered unusual for the region, for the season or just rarely sighted in general. This is a specific call the eBird API provides by region. While many of the birds featured in it are not endemic to NZ or endangered, I thought it was too interesting not to include.


### Custom_search
After these simple routes, there is one with a little more interactivity to it. Custom_search a route where the user is given a page with a checklist of bird species they would like to see visualized on a map. If accessed via GET the user is given a simple HTML form with checkboxes. When the user clicks the Submit button the page passes a list of the desired species to the route, which checks for each species presence in the list and then works like the helpers.py’s get_data() and extract() functions. The difference is, depending on the species selected, each data pull is appended to the next and then they are looped through as a list of lists (ie. number of species selected), then the sightings for each species  themselves . The relevant data is appended to our list of Latitudes, Longitudes, Locations and Species Names before plotting them with GMplot as described above.

### My Sightings
We then move on to My Sightings, where a user can register for an account, login, change their password and record their own endangered bird sightings. The user can also visualize their own sightings on Google Map like the other routes.

### Login
The first route is the Login route which, if reached via GET, presents a form asking for a username and a password, or prompting the user to click register if they haven’t made an account yet. If the route is reached via POST after clicking submit, the input is checked for the presence of text in both fields. If something is missing, it returns an apology page with a message advising the user of the problem and a link to try again. If both fields are filled out, the
username is used to query the SQL database’s Users table for a row with that username. The table includes an auto-incrementing unique id, username and hash(ed password).

If a matching username is not found, the user is given another apology page, error message and link to try again. If the username is in the database, the password is hashed with the Werkzeug check_password_hash function which compares the input to the hashed version saved in the users table. A wrong password will also return an apology page. If all is as it should be, the user table row id is saved as the Session user_id which will come in handy for submitting the users sightings to the Sightings table later on. Upon a successful login, the user is presented with the Submit page where they can log their own sightings, see a table of these sightings and generate a map of them.

### Register
The next route is the Register route which, like Login, via GET presents the user with a form to fill out with their desired username, password and password confirmation. Once submitted via POST, the input is checked for completeness. The Users table is checked in case the username already exists and finally the passwords entered are checked to make sure they are the same. Any of these errors will return an apology page, relevant error message and redirect link.
Once all is well, the password is hashed using Werkzeug and we update the table with the username and hash. The user is then returned to the Login page.

### Submit
After registering and logging in successfully the user has access to the Submit route. If the page is reached via GET the user is shown a form to submit their own sightings and a table which displays the users previously recorded sightings which are pulled from the Sightings table of our SQL database.
There is also a link to change the password and one to visualize their own sightings on a map.
If the page is submitted via POST, the form is checked for completeness, the Location text box is checked for certain characters that can cause errors in our code. Finally the details are  inserted into the Sightings table. The page then redirects to itself where it will display this submission on the  HTML table which uses Jinja to draw from the SQL database.

### Visualize
The Visualize route also draws from this Sightings table and if there are sightings recorded by that user, their rows are selected via SQL, turned into dictionaries and then looped through and put into lists to submit to the GMplot library as described above. The user is presented with a Google Map that has their sightings plotted over it. The GMplot geocode function gets GPS coordinates based on the place name and region, sometimes it has less accuracy than desired depending on the information given. Eg the Hunua Ranges return the Auckland city center whereas others have better specificity. A solution would be to have the user input the coordinates themselves, but that is beyond the scope of this project for now.

### Changepw

Finally there is also a ‘change password’ route which works like a combination of the login and register routes. It checks the form for completeness, that the old password is correct, hashes the new password and updates the new hash into the Users table. Irregular input also returns apology pages with error messages and redirects to the change password page.

#### Other Files
Being a Flask application, the project has its layout file and other HTML files in the Templates folder and the CSS file is saved along with the images used for the project (from Creative Commons) in the Static folder. There is also the Birdbase.db SQL file and the Flask Session folder.

#### CSS and Design
As for the design on the page, it has a simple sidebar with the app’s different features and a landing page with picture links to the different bird species. I chose to keep it simple, relatively clean and with an emphasis on the visual since not everyone may be familiar with these species. I thought it would be useful to have the pictures as a reference on the page most of the time.
For the CSS I drew from the examples featured on W3Schools CSS templates pages which proved a hugely helpful resource.

#### What’s Next
In the future I’d like to improve the app by embedding the maps in the page rather than linking away, add more information about the bird species as well as expanding the scope of species covered. I would also install SQLite properly without the training wheels of CS50’s library SQL module.

Thanks for reading! Kia ora!


