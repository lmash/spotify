# spotify
Convert iTunes Library to Spotify

#### Project description
Migrate iTunes albums, playlists and tracks to Spotify. 

#### Tech Stack
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

#### Pre-requisite
Spotify developer account with app added
The following app settings
 - Redirect URI's: http://example.com
If you are adding for anotehr user, ensure that user is listed in User Management
The Client ID and Client Secret noted (used below in .env file)

#### Setup
Create virtual env 
```
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

#### Usage
 - From iTunes get Library.xml
   File --> Library --> Export Library
   (Save as Library.xml, move Library.xml to spotify/.data/playlist)

##### Extracting all tracks, albums and playlists from Library.xml
```commandline
cd spotify
python main.py --run
```
