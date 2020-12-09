import requests
import json
import csv
import urllib.parse
import time
from requests.auth import HTTPBasicAuth
from dnac_config import DNAC, DNAC_PORT, DNAC_USER, DNAC_PASSWORD

requests.packages.urllib3.disable_warnings()

def create_areas():
    """
    Building out function to create sites (areas). Using requests.post to make a call to DNA.
    """
    token = get_auth_token() # Get Token
    url = DNAC+"/dna/intent/api/v1/site"
    hdr = {'x-auth-token': token, 'content-type' : 'application/json'}
    with open('csvfile.csv', 'r') as csvfile:    #csvfile.csv is the csv file that has the details fro the site to be created. Changed the line[X] as it relates to the csv file
        reader = csv.reader(csvfile)
        area = []
        for line in reader:
            area.append(line[4])
        area_set = set(area)    #change the list of all areas to a set to remove any duplicates
        area_list = list(area_set)   #change the set back to list
        for items in range(len(area_list)):
            payload = json.dumps({"type": "area", "site": {"area": {"name": area_list[items],"parentName": "global/XXX"}}})   # XXX = parent path, update as needed
            resp = requests.post(url, headers=hdr, data = payload, verify = False)
        time.sleep(1)            


def create_building():
    """
    Building out function to create sites(buildings). Using requests.post to make a call to DNA
    """
    token = get_auth_token() # Get Token
    url = DNAC+"/dna/intent/api/v1/site"
    #print(url) #check if the url is correct
    hdr = {'x-auth-token': token, 'content-type' : 'application/json'}
    payload = {}

    with open('csvfile.csv', 'r') as csvfile:   #csvfile.csv is the csv file that has the details fro the site to be created. Changed the line[X] as it relates to the csv file
        reader = csv.reader(csvfile)
          
        for line in reader:
            url_site = DNAC+"/dna/intent/api/v1/site?name=global/abcsite8/"+line[4] #url to get state ID
            resp = requests.get(url=url_site, headers=hdr, verify = False)  
            getsite = resp.json()
            siteId = getsite['response'][0]['id']    # get the site ID 
            #print(siteId) #check to see if site id is correct. Can be checked through GUI url as well, by selecting any particular site
            
            url_bldg = DNAC+"/api/v1/group/"   #url to post building/sites
            address = line[6]
            #print(address) #check to see if the address is being exacted correctly
            """
            Url to make api call using mapbox api. We are trying to geocode for the address from the csv file.
            The token used is a temporary token, which will expire, and will have to be updated.
            """
            url_long_lat = "https://api.mapbox.com/geocoding/v5/mapbox.places/"+urllib.parse.quote(line[6])+".json?types=address&access_token=XXX" # XXX = token for the api, update as needed.
            response_long_lat = requests.get(url=url_long_lat).json()
            longitude = response_long_lat["features"][0]["center"][0]
            latitude = response_long_lat["features"][0]["center"][1]
            
            """
            Posting building, with all the required fields, including address, latitude and longitude.
            """
            payload_bldg = json.dumps({"groupTypeList":["SITE"],"parentId":siteId,"childIds":[""],"name":line[0],"id":"","additionalInfo":[{"nameSpace":"Location","attributes":{"latitude":latitude,"longitude":longitude,"address":line[6],"country":"United States","type":"building"}}]})
            #print(payload_bldg) #check if payload is correct

            resp_bldg = requests.post(url = url_bldg, headers=hdr, data = payload_bldg, verify = False)  # Make the Post Request            
            #response_code = resp_bldg.status_code    #check the response to see if the post was successful
            #print(response_code)
            #response = resp_bldg.content
            #print(response)
        

            
def get_auth_token():
    """
    Building out Auth request. Using requests.post to make a call to the Auth Endpoint
    """
    url = DNAC+'/dna/system/api/v1/auth/token'       # Endpoint URL
    resp = requests.post(url, auth=HTTPBasicAuth(DNAC_USER, DNAC_PASSWORD), verify = False)  # Make the POST Request
    token = resp.json()['Token']    # Retrieve the Token from the returned JSONhahhah
    return token    # Create a return statement to send the token back for later use

if __name__ == "__main__":
    create_areas()
    create_building()
    