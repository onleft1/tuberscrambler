# -*- coding: utf-8 -*-

import os
import pickle
import random
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

### Setting Variables
# Authentication
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl","https://www.googleapis.com/auth/youtube.readonly"]
credentials = None

# Request
n=input("How many videos would you like to randomize? ") #number of items to randomize
plist = input("Insert the playplist code: ")

### Authentication ---------------------------------------------------------------------------------------
# token.pickle stores the user's credentials from previously successful logins - from the file
print("Authenticating ---")
if os.path.exists('token.pickle'):
    print('Loading Credentials From File...')
    with open('token.pickle', 'rb') as token: #rb sends for read bite file (not a text)
        credentials = pickle.load(token)

# If there are no valid credentials available, then either refresh the token or log in.
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token: #credentials are not valid anymore
        print('Refreshing Access Token...')
        credentials.refresh(Request())
    else:
        print('Fetching New Tokens...') #credentials are not there at all
        flow = InstalledAppFlow.from_client_secrets_file(
            'key.json',
            scopes=scopes
        )

        flow.run_local_server(port=8080, prompt='consent',
                              authorization_prompt_message='')
        credentials = flow.credentials

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as f:
            print('Saving Credentials for Future Use...')
            pickle.dump(credentials, f)

youtube = build("youtube", "v3", credentials=credentials)
print("Authenticaton complete ---")
### -------------------------------------------------------------------
print("")
print("Request and reordering...")
### List of videos > 50
### From https://stackoverflow.com/questions/18804904/retrieve-all-videos-from-youtube-playlist-using-youtube-v3-api

res = youtube.playlistItems().list(
    part="snippet",
    playlistId=plist,
    maxResults="50"
    ).execute()

nextPageToken = res.get('nextPageToken')
while ('nextPageToken' in res):
    nextPage = youtube.playlistItems().list(
    part="snippet",
    playlistId=plist,
    maxResults="50",
    pageToken=nextPageToken
    ).execute()
    res['items'] = res['items'] + nextPage['items']

    if 'nextPageToken' not in nextPage:
        res.pop('nextPageToken', None)
    else:
        nextPageToken = nextPage['nextPageToken']

### Create a random list and print
rdlist = random.sample(range(len(res["items"])-1), n)
#print(rdlist)
print ("{:<3} {:<69} {:<28} {:<12} {:<28}".format("#",'id', 'etag','Video Id', 'Title'))
for x in rdlist:
    print("{:<3} {:<69} {:<28} {:<12} {:<28}".format(x,res["items"][x]["id"], res["items"][x]["etag"],res["items"][x]["snippet"]["resourceId"]["videoId"],res["items"][x]["snippet"]["title"][0:30]))

for x in rdlist:
    request = youtube.playlistItems().update(
            part="snippet",
            body={
            "id": res["items"][x]["id"],
            "snippet": {
                "playlistId": plist,
                "position": 0,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": res["items"][x]["snippet"]["resourceId"]["videoId"]
                }
            }
            }
        )
    response = request.execute()

# print(response)
print("DONE!")