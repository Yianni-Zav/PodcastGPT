
# CONFIGURATION SETTINGS
from os import path

APP_PORT = 5002


PODCASTS_PATH = f'{path.dirname(path.realpath(__file__))}/static/podcasts'
PROFILES_PATH = f'{path.dirname(path.realpath(__file__))}/static/profiles'

# The list of personalities that are available for the podcast generator
# the profile photos paths are <personality>.jpg
PERSONALITIES = [
  'joe_rogan',
  'ben_shapiro',
  'elon_musk',
  'joe_biden',
  'donald_trump',
  'barack_obama',
]