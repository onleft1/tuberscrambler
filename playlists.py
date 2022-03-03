# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlists.update
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl","https://www.googleapis.com/auth/youtube.readonly"]

credentials = None

# token.pickle stores the user's credentials from previously successful logins - from the file
if os.path.exists('token2.pickle'):
    print('Loading Credentials From File...')
    with open('token2.pickle', 'rb') as token: #rb sends for read bite file (not a text)
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
        with open('token2.pickle', 'wb') as f:
            print('Saving Credentials for Future Use...')
            pickle.dump(credentials, f)

youtube = build("youtube", "V3", credentials=credentials)

### -------------------------------------------------------------------

request = youtube.playlistItems().insert(
        part="snippet",
        body={
          "snippet": {
            "playlistId": "PLmMU0IJAD9NpiZfCSYIE_qMvTLxGx8yk-",
            "position": 0,
            "resourceId": {
              "kind": "youtube#video",
              "videoId": "M7FIvfx5J10"
            }
          }
        }
    )

response = request.execute()
print(response)


