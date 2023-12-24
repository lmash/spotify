# spotify
Convert iTunes Library to Spotify

#### Project description
Migrate iTunes albums, playlists and tracks to Spotify. 

#### Tech Stack
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)


#### Setup
Create virtual env 
```
python3.11 -m venv env
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
