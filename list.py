import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    #os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "key.json"

    # pip install google-auth-oauthlib
    from google_auth_oauthlib.flow import InstalledAppFlow

    # https://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html

    #flow = InstalledAppFlow.from_client_secrets_file('key.json',
    #scopes=['https://www.googleapis.com/auth/youtube.readonly'])

    #cred = flow.run_local_server(
    #    host='localhost',
    #    port=8088,
    #    authorization_prompt_message='Please visit this URL: {url}',
    #    success_message='The auth flow is complete; you may close this window.',
    #    open_browser=True)

    #with open('refresh.token', 'w+') as f:
    #    f.write(cred._refresh_token)

    #print('Refresh Token:', cred._refresh_token)
    #print('Saved Refresh Token to file: refresh.token')

    from google.oauth2.credentials import Credentials
    from apiclient.discovery import build

    credentials = Credentials(
        None,
        refresh_token="refresh.token",
        token_uri="https://accounts.google.com/o/oauth2/token",
        client_id="346737772235-v6s58al5rlo7hs942o79up36ot936pfo.apps.googleusercontent.com",
        client_secret="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"
    )

    # Get credentials and create an API client
    #flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    #    client_secrets_file, scopes)
    #credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
       api_service_name, api_version, credentials=credentials)

    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=25,
        playlistId="PLmMU0IJAD9NpiZfCSYIE_qMvTLxGx8yk-"
    )
    response = request.execute()

    print(response)

if __name__ == "__main__":
    main()
