# TuberScrambler

A simple Python script to randomize a limited number of videos in a YouTube playlist to save YouTube API Quota.

Since it changes the playlist on YouTube, your devices like TV, phone, tablet, etc. will play the playlist using the new order. This solves the problem of some smart TVs (and other devices) that don't have the "Shuffle" button.

## How to use it

**Prerequites**: 
  1. At this stage of TuberScrambler development you will need an *OAuth 2.0 Client IDs* JSON file (https://console.cloud.google.com/apis/credentials) downloaded to the same folder as Python script.
  2. Python 3.8+ installed (https://www.python.org).
 
**How to Run**
  1. Run this in your command prompt: ``"%userprofile%\AppData\Local\Programs\Python\Python38\python.exe" "playlists.py"``
  2. The first time you run it, authenticate using your Google Account.
  3. Set the number of videos to be changed (max of 190 videos/day)
  4. Paste the playlist ID you want to be randomized.
  5. Enjoy!
