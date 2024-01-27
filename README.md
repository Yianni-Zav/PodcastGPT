# Cast

- A Podcast generator for celebrity personalities


# Setup

- Clone the repo
`git clone https://github.com/Yianni-Zav/PodcastGPT.git`

- Setup virtual environment
```
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

- Run the app
`python3 app.py`

# Requests

- Curl reques example
- This make a test call to the api. It should download a demo.mp4 file into the current directory
```
curl --location --request POST 'http://10.121.221.183:5002/cast' --output demo.mp4
```


- The url for local testing is 
- `http://127.0.0.1:5002/cast`

- The url for LAN testing will look something like this
- `http://10.121.221.183:5002/cast`

# CAST API

`http://<ip:5002>/cast`
### POST 

Request:
```
{
        "guest": "personality_1",
        "host": "personality_2",
        "topic": "topic",
        "duration": 5
}
```

Response:
```
{
    "duration": 5,
    "guest": "personality_1",
    "host": "personality_2",
    "topic": "topic",
    "video_url": "http://127.0.0.1:5002/static/podcasts/JoeRoganBenShapiro.mp4"
}
```



### GET Request

Request:
```
~
```
Response:
```
{
    "barack_obama": "http://127.0.0.1:5002/static/profiles/barack_obama.jpg",
    "ben_shapiro": "http://127.0.0.1:5002/static/profiles/ben_shapiro.jpg",
    "donald_trump": "http://127.0.0.1:5002/static/profiles/donald_trump.jpg",
    "elon_musk": "http://127.0.0.1:5002/static/profiles/elon_musk.jpg",
    "joe_biden": "http://127.0.0.1:5002/static/profiles/joe_biden.jpg",
    "joe_rogan": "http://127.0.0.1:5002/static/profiles/joe_rogan.jpg"
}
```


