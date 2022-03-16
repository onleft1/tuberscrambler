#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# from importlib.metadata import files
import os
import pickle
import random
import time
# from signal import pause
# import google_auth_oauthlib.flow
# import googleapiclient.discovery
import googleapiclient.errors

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


### Authentication
def auth():
    ### Setting Variables
    # Authentication
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl","https://www.googleapis.com/auth/youtube.readonly"]
    credentials = None
    picklefile = "token.pickle"

    currentpath = os.getcwd()

    ### Finding json file for Google OAuth2 in the same folder
    jsonlist = []
    for file in os.listdir(currentpath):
        if file.endswith(".json"):
            #jsonfile = os.path.join(currentpath, file)
            jsonfile = os.path.join(file)
            jsonlist.append(jsonfile)

    if len(jsonlist) == 0:
        print()
        print("-----> ERROR: OAuth key JSON file not found in folder.")
        print()
        print("Please save your JSON file into the same folder as TubeScrambler.")
        print()
        print("If you haven't created one, access https://console.cloud.google.com/apis/credentials and click on + Create Credentails --> OAuth Client ID and follow the key creation process. Download and save the JSON file into the same folder as TuberScrambler and run it again.")
        print()
        print()
        print()
        print()
        input("Press Enter to exit...")
        exit()

    elif len(jsonlist) == 1:
        jsonfile = jsonlist[0]

    else:
        print("Choose the correct OAuth key JSON file:")
        for index, i in zip(range(0,len(jsonlist)),jsonlist):
            print(str(index + 1)+ "  " + i)
        
        while True:
            try:
                number1 = int(input("Choose your JSON key file [1 to "+ str(len(jsonlist))+"]:"))
                if number1 < 1 or number1 > len(jsonlist):
                    raise ValueError #this will send it to the print message and back to the input option
                jsonfile = jsonlist[number1 - 1]
                break
            except ValueError:
                print("Invalid answer. It must be in a number within the range of 1-" + str(len(jsonlist)) + ".")
        
    print("=== Arquivo JSON selecionado: " + jsonfile)


    ### Authentication ---------------------------------------------------------------------------------------
    # token.pickle stores the user's credentials from previously successful logins - from the file
    print("Authenticating -----------")
    if os.path.exists(picklefile):
        print('Loading Credentials From File...')
        with open(picklefile, 'rb') as token: #rb sends for read bite file (not a text)
            credentials = pickle.load(token)

    # If there are no valid credentials available, then either refresh the token or log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token: #credentials are not valid anymore
            print('Refreshing Access Token...')
            credentials.refresh(Request())
        else:
            print('Fetching New Tokens...') #credentials are not there at all
            flow = InstalledAppFlow.from_client_secrets_file(
                jsonfile,
                scopes=scopes
            )

            flow.run_local_server(port=8080, prompt='consent',
                                authorization_prompt_message='')
            credentials = flow.credentials

            # Save the credentials for the next run
            with open(picklefile, 'wb') as f:
                print('Saving Credentials for Future Use...')
                pickle.dump(credentials, f)

    global youtube
    youtube = build("youtube", "v3", credentials=credentials)
    print("Authenticaton complete ---")

auth()

print("")
print("Requesting and reordering...")

### Playlists
def reqplaylists():
    pllist = youtube.playlists().list( ### Requesting a list of playlists
            part="snippet,contentDetails",
            maxResults="50",
            mine=True).execute()

    nextPageToken = pllist.get('nextPageToken')
    while ('nextPageToken' in pllist):
        nextPage = youtube.playlists().list(
        part="snippet,contentDetails",
        maxResults="50",
        pageToken=nextPageToken
        ).execute()
        pllist['items'] = pllist['items'] + nextPage['items']

        if 'nextPageToken' not in nextPage:
            pllist.pop('nextPageToken', None)
        else:
            nextPageToken = nextPage['nextPageToken']

    #### Print output to a file
    # with open("playlist.txt", "w") as external_file:
    #     #add_text = "This text will be added to the file"
    #     print(pllist, file=external_file)
    #     external_file.close()

    ### Printing ther list of playlists
    b=0
    print ("{:<2} {:<69} {:<28}".format("#",'Title', 'Id'))
    for rep in pllist["items"]:
        print("{:<2} {:<69} {:<28}".format(b, rep["snippet"]["title"], rep["id"])) #, rep["etag"],rep["snippet"]["resourceId"]["videoId"],rep["snippet"]["title"][0:30]))
        b=b+1

    choose=int(input("Type the number of the playlist: "))
    global plist
    plist = pllist["items"][choose]["id"]

    print("You've chosen the playlist '" +  pllist["items"][choose]["snippet"]["title"] + "'")

reqplaylists()

### Shuffling
def shufflepl():
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

    # Set the number of videos to randomize
    try:
        print("Your playlist has "+ str(len(res["items"])) +" videos.")
        n = int(input("How many videos would you like to randomize? [No/invalid answer = 3]"))
        if n > len(res["items"]):
            print("Your playlist has less videos than " + str(n) + " video. Your playlist has " + str(len(res["items"])) + " videos. Therefore, I will randomize them all.")
            n = len(res["items"])
    except ValueError:
        print()
        print()
        print("Your answer was 'in blank' or 'invalid'. Assuming 3 videos to randomize...")
        print()
        n = 3

    print()
    print("----> Videos to randomize: "+ str(n))
    print()
    time.sleep(2) # Pause

    ### Create a random list and print
    rdlist = random.sample(range(len(res["items"])), n)
    #print(rdlist)
    #print ("{:<3} {:<69} {:<28} {:<12} {:<28}".format("#",'id', 'etag','Video Id', 'Title'))
    print ("{:<3} {:<12} {:<28}".format("#",'Video Id','Title'))
    for x in rdlist:
        print("{:<3} {:<12} {:<28}".format(
            x,
            #res["items"][x]["id"], 
            #res["items"][x]["etag"],
            res["items"][x]["snippet"]["resourceId"]["videoId"],
            res["items"][x]["snippet"]["title"][0:60])
            )

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
    print()
    print()
    print("Done, enjoy! =)")

shufflepl()
