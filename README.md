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
