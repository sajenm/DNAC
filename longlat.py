import requests
import urllib.parse
import csv
import time


def get_long_lat():
    with open('csvfile_for_creating_sites_11-10-2020.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                url_long_lat = "https://api.mapbox.com/geocoding/v5/mapbox.places/"+urllib.parse.quote(line[7])+".json?types=address&access_token=XXX" #XXX = Token for the api
                #print(url_long_lat)
                #test = urllib.parse.quote(line[6])
                #print(test)
                #url = "https://api.mapbox.com/geocoding/v5/mapbox.places/26901%20Agoura%20Rd%20Calabasa%20CA%2091301.json?types=address&access_token=pk.eyJ1Ijoic2FqbWFoIiwiYSI6ImNraHA1NHFrODA5eWUycm1zNDk2MWZ0OGEifQ.01Xf-p7XooIEu6LeN_F3mw"
                response = requests.get(url=url_long_lat).json()
                long = response["features"][0]["center"][0]
                lat = response["features"][0]["center"][1]
                print(long," ",lat)
                time.sleep(1)

    


if __name__ == "__main__":
    get_long_lat()
    
