
# CONFIGURATION SETTINGS
from os import path

APP_PORT = 5002



PODCASTS_PATH = f'{path.dirname(path.realpath(__file__))}/static/podcasts'
PROFILES_PATH = f'{path.dirname(path.realpath(__file__))}/static/profiles'
AUDIO_PATH = f'{path.dirname(path.realpath(__file__))}/static/audio'
CLIENT_DEV_PATH = f'{path.dirname(path.realpath(__file__))}/frontend/'
STATIC_FOLDER_PATH = f'{path.dirname(path.realpath(__file__))}/static'


# The list of personalities that are available for the podcast generator
# the profile photos paths are <personality>.jpg
PERSONALITIES = [
  'lex_fridman',
  'morgan_freeman',
  'joe_biden',
  # 'joe_rogan',
  # 'ben_shapiro',
  # 'elon_musk',
  # 'donald_trump',
  # 'barack_obama',
]

PERSONALITY_PROFILES = { personality: f'{PROFILES_PATH}/{personality}.jpg' for personality in PERSONALITIES }

