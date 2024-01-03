# spotify
Convert iTunes Library to Spotify

### Project description
Migrate iTunes albums, playlists and tracks to Spotify. 

### Tech Stack
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

### Pre-requisite
Spotify developer account with app added, developer account is free (example app below)
![app.jpg](screenshots%2Fapp.jpg)

Ensure app has the following settings
 - Redirect URI's: http://example.com
 - API's used: Web API
 - If you are using the app to convert additional users (Not the user where the app is added), add the user in User Management

![user_added_to_app.jpg](screenshots%2Fuser_added_to_app.jpg)

Note the Client ID and Client Secret (used below in .env file)

### Setup
Clone the repo
```commandline
git clone https://github.com/lmash/spotify.git
```

Create virtual env 
```
cd spotify
python -m venv env
source env/bin/activate
```

Install code
```commandline
pip install -r requirements.txt
```

Populate .env file
Edit .env_backup, populate SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET

```commandline
mv .env_backup .env
```

### Usage
 - From iTunes get Library.xml
   File --> Library --> Export Library
   (Save as Library.xml, move Library.xml to spotify/.data/playlist)
 - Ensure you are logged into Spotify as the user being converted

#### Extracting all tracks, albums and playlists from Library.xml
```commandline
cd spotify
python main.py --run
```
