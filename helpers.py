import requests
from dotenv import load_dotenv
import os


load_dotenv()  # loads .env file into environment
apikey = os.getenv("APIKEY")
TOKEN = os.getenv("TOKEN")
print(apikey, TOKEN)

# function loop through data, clean irregular user imput on location strings and create lists to pass to GMPlot
def extract(data):

    # initialize lists
    latitudes = []
    longitudes = []
    locations = []
    names = []

    #get number of sightings in the returned data
    length = len(data)
    for i in range(length):

      # get relevant data from each dictionary and append it to the lists
      bird = data[i]["comName"]
      names.append(bird)
      date = data[i]["obsDt"]
      lat = data[i]['lat']
      latitudes.append(lat)
      long = data[i]['lng']
      longitudes.append(long)
      location = data[i]["locName"]

      #check and clean data for characters that can cause bugs in code
      for old, new in [("_", "__"), ("?", "~q"), ("’", "'"), ("(", " "), (")", " "),("%", "~p"), ("#", "~h"), ("/", "~s"),
                       ('\u014c', "a"), (u"\u014D", "O"), (u"\u012B", "i"), (u"\u016B", "u"),(u"\u0101", "a"), ("\"", "''"), ("\n", "''")]:
          location = location.replace(old, new)
      locations.append(location)
    return long, lat, names, latitudes, longitudes, locations

# function to use Requests to get the data from eBird API calls
def get_data(url):

    payload={}
    headers = {'X-eBirdApiToken': TOKEN}
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    return data
