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

#### Usage
There are 2 ways this can be used. Both ways require Library.xml
 - From iTunes get Library.xml
   File --> Library --> Export Library
   (Save as Library.xml, move Library.xml to spotify/.data/playlist)

##### Extracting all tracks, albums and playlists from Library.xml (Use when no access to users physical library)
 - Extract, Clean, Load (run from spotify folder using cmd line)
```commandline
python main.py -efl

```