import os
from cs50 import SQL
from datetime import date
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import gmplot
from helpers import extract, get_data
import os
import requests
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Initialize SQL database
db = SQL("sqlite:///birdbase.db")

# Initialize API key and token
load_dotenv()  # loads .env file into environment
apikey = os.getenv("APIKEY")
TOKEN = os.getenv("TOKEN")
print(apikey, TOKEN)

#Home route
@app.route("/", methods=["GET", "POST"])
def home():
  if request.method == "GET":
    return render_template("index.html")


#kokako sightings
@app.route("/kokako_sightings", methods=["GET", "POST"])
def kokako_sightings():
  if request.method == "GET":

    # initialize, extract and process the data
    url = "https://api.ebird.org/v2/data/nearest/geo/recent/kokako3?lat=-36.8871&lng=174.7474"
    data = get_data(url)
    long, lat, names, latitudes, longitudes, locations = extract(data)

    # plot the data and generate the map
    gmap = gmplot.GoogleMapPlotter(lat, long, 6, apikey=apikey)
    gmap.scatter(latitudes, longitudes, 'yellow', label = names, size = 40, title = locations)
    gmap.draw('templates/kokako_sightings.html')
    return render_template("kokako_sightings.html", apikey=apikey)


#notable sightings map
@app.route("/map", methods=["GET", "POST"])
def map():
  if request.method == "GET":

    # initialize, extract and process the data
    url = "https://api.ebird.org/v2/data/obs/NZ/recent/notable"
    data = get_data(url)
    long, lat, names, latitudes, longitudes, locations = extract(data)

    # plot the data and generate the map
    gmap = gmplot.GoogleMapPlotter(-41.276825, 174.777969, 6, apikey=apikey)
    gmap.scatter(latitudes, longitudes, 'yellow', label = names, size = 40, title = locations)
    gmap.draw('templates/map.html')
    return render_template("map.html", apikey=apikey)


#bellbird sightings / korimako
@app.route("/bellbird_sightings", methods=["GET", "POST"])
def bellbird_sightings():
  if request.method == "GET":

    # initialize, extract and process the data
    url = "https://api.ebird.org/v2/data/nearest/geo/recent/nezbel1?lat=-36.8871&lng=174.7474"
    data = get_data(url)
    long, lat, names, latitudes, longitudes, locations = extract(data)

    #plot the data and generate the map
    gmap = gmplot.GoogleMapPlotter(-41.276825, 174.777969, 6, apikey=apikey)
    gmap.scatter(latitudes, longitudes, 'yellow', label = names, size = 40, title = locations)
    gmap.draw('templates/bellbird_sightings.html')
    return render_template("bellbird_sightings.html", apikey=apikey)


#spotted kiwi sightings
@app.route("/skiwi_sightings", methods=["GET", "POST"])
def skiwi_sightings():
  if request.method == "GET":

    # initialize, extract and process the data
    url = "https://api.ebird.org/v2/data/nearest/geo/recent/liskiw1?lat=-36.8871&lng=174.7474"
    data = get_data(url)

    # since Spotted Kiwi sightings are quite rare, be prepared for no data to be returned
    if len(data) < 1:
      message = "⛔ No recent sightings."
      link = "skiwi_sightings"
      return render_template("apology.html", message = message, link = link)
    long, lat, names, latitudes, longitudes, locations = extract(data)

    # plot the data and generate the map
    gmap = gmplot.GoogleMapPlotter(lat, long, 6, apikey=apikey)
    gmap.scatter(latitudes, longitudes, 'yellow', label = names, size = 40, title = locations)
    gmap.draw('templates/skiwi_sightings.html')
    return render_template("skiwi_sightings.html", apikey=apikey)


#North Island Brown kiwi sightings
@app.route("/nbkiwi_sightings", methods=["GET", "POST"])
def nbkiwi_sightings():
  if request.method == "GET":

    # initialize, extract and process the data
    url = "https://api.ebird.org/v2/data/nearest/geo/recent/nibkiw1?lat=-36.8871&lng=174.7474"
    data = get_data(url)

    # handle a case where there haven't been any recent sightings
    if len(data) < 1:
      message = "⛔ No recent sightings."
      link = "nbkiwi_sightings"
      return render_template("apology.html", message = message, link = link)
    long, lat, names, latitudes, longitudes, locations = extract(data)

    # plot the data and generate the map
    gmap = gmplot.GoogleMapPlotter(lat, long, 7, apikey=apikey)
    gmap.scatter(latitudes, longitudes, 'yellow', label = names, size = 40, title = locations)
    gmap.draw('templates/nbkiwi_sightings.html')
    return render_template("nbkiwi_sightings.html", apikey=apikey)


# Kea
@app.route("/kea_sightings", methods=["GET", "POST"])
def kea_sightings():
  if request.method == "GET":

    # initialize, extract and process the data
    url = "https://api.ebird.org/v2/data/nearest/geo/recent/kea1?lat=-36.8871&lng=174.7474"
    data = get_data(url)
    long, lat, names, latitudes, longitudes, locations = extract(data)

    # plot the data and generate the map
    gmap = gmplot.GoogleMapPlotter(-42.8643059, 171.7512568, 7, apikey=apikey)
    gmap.scatter(latitudes, longitudes, 'yellow', label = names, size = 40, title = locations)
    gmap.draw('templates/kea_sightings.html')
    return render_template("kea_sightings.html", apikey=apikey)


# Kākāriki
@app.route("/kakariki_sightings", methods=["GET", "POST"])
def kakariki_sightings():
  if request.method == "GET":

    # initialize, extract and process the data
    url = "https://api.ebird.org/v2/data/nearest/geo/recent/refpar4?lat=-36.8871&lng=174.7474"
    data = get_data(url)
    long, lat, names, latitudes, longitudes, locations = extract(data)

    # plot the data and generate the map
    gmap = gmplot.GoogleMapPlotter(-41.276825, 174.777969, 6, apikey=apikey)
    gmap.scatter(latitudes, longitudes, 'yellow', label = names, size = 40, title = locations)
    gmap.draw('templates/kakariki_sightings.html')
    return render_template("kakariki_sightings.html", apikey=apikey)


# Hihi / stitchbird
@app.route("/hihi_sightings", methods=["GET", "POST"])
def hihi_sightings():
  if request.method == "GET":

    # initialize, extract and process the data
    url = "https://api.ebird.org/v2/data/nearest/geo/recent/stitch1?lat=-36.8871&lng=174.7474"
    data = get_data(url)
    long, lat, names, latitudes, longitudes, locations = extract(data)

    # plot the data and generate the map
    gmap = gmplot.GoogleMapPlotter(-41.276825, 174.777969, 6, apikey=apikey)
    gmap.scatter(latitudes, longitudes, 'yellow', label = names, size = 40, title = locations)
    gmap.draw('templates/hihi_sightings.html')
    return render_template("hihi_sightings.html", apikey=apikey)


# Yellow-Eyed Penguin
@app.route("/penguin_sightings", methods=["GET", "POST"])
def penguin_sightings():
  if request.method == "GET":

    # initialize, extract and process the data
    url = "https://api.ebird.org/v2/data/nearest/geo/recent/yeepen1?lat=-36.8871&lng=174.7474"
    data = get_data(url)
    print(len(data))

    # handle the case where no penguins have been sighted
    if len(data) < 1:
      message = "⛔ No recent sightings."
      link = "penguin_sightings"
      return render_template("apology.html", message = message, link = link)
    long, lat, names, latitudes, longitudes, locations = extract(data)

    # plot the data and generate the map
    gmap = gmplot.GoogleMapPlotter(-43.8833298, 170.5166646, 7, apikey=apikey)
    gmap.scatter(latitudes, longitudes, 'yellow', label = names, size = 40, title = locations)
    gmap.draw('templates/penguin_sightings.html')
    return render_template("penguin_sightings.html", apikey=apikey)


# Blue duck Whio
@app.route("/whio_sightings", methods=["GET", "POST"])
def whio_sightings():
  if request.method == "GET":

    # initialize, extract and process the data
    url = "https://api.ebird.org/v2/data/nearest/geo/recent/bluduc1?lat=-36.8871&lng=174.7474"
    data = get_data(url)

    # handle the case where no whio ducks have been sighted
    if len(data) < 1:
      message = "No recent sightings."
      return render_template("apology.html", message = message)
    long, lat, names, latitudes, longitudes, locations = extract(data)

    # plot the data and generate the map
    gmap = gmplot.GoogleMapPlotter(-41.28666552, 174.772996908, 6, apikey=apikey)
    gmap.scatter(latitudes, longitudes, 'yellow', label = names, size = 40, title = locations)
    gmap.draw('templates/whio_sightings.html')
    return render_template("whio_sightings.html", apikey=apikey)


# Custom Search
@app.route("/custom_search", methods=["GET", "POST"])
def custom_search():

  # display the search page
  if request.method == "GET":
    return render_template("custom_search.html")

  #carry out the search via GET
  else:

    # check for correct usage and return error message and redirect link
    if not request.form.get("bird"):
      message = "⛔ Must select a bird."
      link = "custom_search"
      return render_template("apology.html", message = message, link = link)
    else:

      # get the list of birds the user wishes to search for
      search_birds = request.form.getlist("bird")
      payload={}
      data = []
      headers = {'X-eBirdApiToken': TOKEN}

      # check for each bird and get their sightings data
      if "bellbird" in search_birds:
        url = "https://api.ebird.org/v2/data/nearest/geo/recent/nezbel1?lat=-36.8871&lng=174.7474"
        response = requests.request("GET", url, headers=headers, data=payload)
        data.append(response.json())
      if "hihi" in search_birds:
        url = "https://api.ebird.org/v2/data/nearest/geo/recent/stitch1?lat=-36.8871&lng=174.7474"
        response = requests.request("GET", url, headers=headers, data=payload)
        data.append(response.json())
      if "kakariki" in search_birds:
        url = "https://api.ebird.org/v2/data/nearest/geo/recent/refpar4?lat=-36.8871&lng=174.7474"
        response = requests.request("GET", url, headers=headers, data=payload)
        data.append(response.json())
      if "kea" in search_birds:
        url = "https://api.ebird.org/v2/data/nearest/geo/recent/kea1?lat=-36.8871&lng=174.7474"
        response = requests.request("GET", url, headers=headers, data=payload)
        data.append(response.json())
      if "kokako" in search_birds:
        url = "https://api.ebird.org/v2/data/nearest/geo/recent/kokako3?lat=-36.8871&lng=174.7474"
        response = requests.request("GET", url, headers=headers, data=payload)
        data.append(response.json())
      if "nbkiwi" in search_birds:
        url = "https://api.ebird.org/v2/data/nearest/geo/recent/nibkiw1?lat=-36.8871&lng=174.7474"
        response = requests.request("GET", url, headers=headers, data=payload)
        data.append(response.json())
      if "penguin" in search_birds:
        url = "https://api.ebird.org/v2/data/nearest/geo/recent/yeepen1?lat=-36.8871&lng=174.7474"
        response = requests.request("GET", url, headers=headers, data=payload)
        data.append(response.json())
      if "sbkiwi" in search_birds:
        url = "https://api.ebird.org/v2/data/nearest/geo/recent/liskiw1?lat=-36.8871&lng=174.7474"
        response = requests.request("GET", url, headers=headers, data=payload)
        data.append(response.json())
      if "whio" in search_birds:
        url = "https://api.ebird.org/v2/data/nearest/geo/recent/bluduc1?lat=-36.8871&lng=174.7474"
        response = requests.request("GET", url, headers=headers, data=payload)
        data.append(response.json())
        
      latitudes = []
      longitudes = []
      names = []
      locations = []
      length = len(data)

      # handle case where no birds at all have been sighted
      if len(data) < 1:
        message = "⛔ No recent sightings for one or more your selected species."
        link = "custom_search"
        return render_template("apology.html", message = message, link = link)

      # loop through and create lists of the data to plot
      for i in range(length):
        leng = len(data[i])
        for h in range(leng):
          bird = data[i][h]["comName"]
          names.append(bird)
          date = data[i][h]["obsDt"]
          lat = data[i][h]['lat']
          latitudes.append(lat)
          long = data[i][h]['lng']
          longitudes.append(long)
          location = data[i][h]["locName"]
          for old, new in [("_", "__"), ("?", "~q"), ("(", " "), (")", " "),("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''"), ("\n", "''")]:
            location = location.replace(old, new)
          locations.append(location)

      # plot the data and generate the custom map
      gmap = gmplot.GoogleMapPlotter(-41.276825, 174.777969, 6, apikey=apikey)
      gmap.scatter(latitudes, longitudes, 'yellow', label = names, size = 40, title = locations)
      gmap.draw('templates/searched.html')
      return render_template("searched.html", apikey=apikey)


#Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    # Check for correct usage and if incorrect return custom error message and return link
    if request.method == "POST":
        if not request.form.get("username"):
            message = "⛔ Must provide username."
            link = "login"
            return render_template("apology.html", message = message, link = link)
        elif not request.form.get("password"):
            message = "⛔ Must provide password."
            link = "login"
            return render_template("apology.html", message = message, link = link)

        # Get info from database for the user
        rows = db.execute("SELECT * FROM users WHERE name = ?", request.form.get("username"))

        # if the user hasn't registered or uses the wrong password, prompt them to register
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            message = "⛔ Something went wrong, please try again."
            link = "login"
            return render_template("apology.html", message = message, link = link)

        # Save the user id as a variable
        session["user_id"] = rows[0]["id"]
        return redirect("/submit")
    else:
        return render_template("login.html")

#Register
@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    if request.method == "POST":

        # Check for correct usage and return a custom error message and redirect link
        if not request.form.get("username"):
            message = "⛔ Must enter correct password."
            link = "register"
            return render_template("apology.html", message = message, link = link)
        elif not request.form.get("password") or not request.form.get("confirmation"):
            message = "⛔ Must enter correct password."
            link = "register"
            return render_template("apology.html", message = message, link = link)

        # save username and check it doesn't already exist in database
        username = request.form.get("username")
        rows = db.execute("SELECT * FROM users WHERE name = ?", username)
        if len(rows) == 1:
              message = "⛔ Choose another username."
              link = "register"
              return render_template("apology.html", message = message, link = link)

        # Check the two passwords are the same and if not return error message
        if request.form.get("password") != request.form.get("confirmation"):
            message = " ⛔ Must enter correct password."
            link = "register"
            return render_template("apology.html", message = message, link = link)

        # hash the users password for security
        hash = generate_password_hash(request.form.get("password"))

        # insert the users input into the database
        db.execute("INSERT INTO users (name, hash) VALUES (?, ?);", username, hash)
        return redirect("/login")
    else:
        return render_template("register.html")

# user can submit their own bird sightings to their personal database and
@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":

        #check for correct usage and return error code and redirect link
        if not request.form.get("location"):
            message = "Must select location"
            return render_template("apology.html", message = message)
        elif not request.form.get("count") or not request.form.get("bird"):
            message = "⛔ Must select Bird Species."
            link = "submit"
            return render_template("apology.html", message = message, link = link)

        # save the data from the form
        user = session["user_id"]
        bird = request.form.get("bird")
        count = int(request.form.get("count"))
        location = request.form.get("location")

        # check for and remedy and input which could cause bugs
        for old, new in [("_", "__"), ("?", "~q"), ("(", " "), (")", " "),("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''"), ("\n", "''")]:
           location = location.replace(old, new)
        today = date.today()

        # update the SQL database/sightings table and display the updated table of the users sightings
        db.execute("INSERT INTO sightings (user_id, bird, count, date, location) VALUES (?, ?, ?, ?, ?);", user, bird, count, today, location)
        database = db.execute("SELECT * FROM sightings WHERE user_id = ?", user)
        return render_template("submit.html", database = database)
    else:

      # if page reached via GET just display the users previous sightings (if any)
      user = session["user_id"]
      database = db.execute("SELECT * FROM sightings WHERE user_id = ?", user)
      return render_template("submit.html", database = database)

#visualize my sightings
@app.route("/visualize", methods=["GET", "POST"])
def visualize():
  if request.method == "GET":

    # gather the users data and pull their sightings from the SQL database
    user = session["user_id"]
    species = db.execute("SELECT * FROM sightings WHERE user_id = ?", user)
    length = len(species)

    # check they have sightings recorded and return error message and redirect link
    if length < 1:
      message = "⛔ Add some birds to your Sightings first!"
      link = "visualize"
      return render_template("apology.html", message = message, link = link)

    # process the data from the SQL database
    latitudes =[]
    longitudes = []
    locations = []
    names = []
    for i in range(length):
      bird = species[i]["bird"]
      names.append(bird)
      location = species[i]["location"]
      locations.append(location)

      # use the user input for the location together with the GMplot geocode function to get coordinates
      geo = gmplot.GoogleMapPlotter.geocode(location, apikey=apikey)
      latitudes.append(geo[0])
      longitudes.append(geo[1])

    # plot the data and generate the map
    gmap = gmplot.GoogleMapPlotter(-41.276825, 174.777969, 6, apikey=apikey)
    gmap.scatter(latitudes, longitudes, 'yellow', label = names, size = 40, title = locations)
    gmap.draw('templates/visualize.html')
    return render_template("visualize.html")

@app.route("/changepw", methods=["GET", "POST"])
def changepw():
    """Change users password"""
    if request.method == "POST":

        # Ensure password was submitted
        if not request.form.get("password1"):
            message = "⛔ Must provide current password."
            link = "changepw"
            return render_template("apology.html", message = message, link = link)

        elif not request.form.get("password2"):
            message = "⛔ Must provide new password."
            link = "changepw"
            return render_template("apology.html", message = message, link = link)
        # Query database for current password and check correct
        user = session["user_id"]
        hash = request.form.get("password1")
        rows = db.execute("SELECT * FROM users WHERE id = ?", user)
        # Ensure username exists and password is correct
        if not check_password_hash(rows[0]["hash"], hash):
            message = "⛔ Must enter correct password."
            link = "changepw"
            return render_template("apology.html", message = message, link = link)
        else:
            hash2 = generate_password_hash(request.form.get("password2"))
            db.execute("UPDATE users SET hash = ? WHERE id = ?;", hash2, user)
            # Redirect user to home page
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("changepw.html")
