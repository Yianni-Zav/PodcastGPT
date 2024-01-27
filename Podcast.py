from Agents import PodcastAgent
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import re
import sys
from gtts import gTTS

import subprocess
import requests
from datetime import datetime
from tempfile import gettempdir
from moviepy.editor import concatenate_audioclips, AudioFileClip
import API_Keys


class Podcast:
    def __init__(self, input_prompt, filename):
        self.filemname = filename
        
        
        
        self.host = PodcastAgent()
        self.guest = PodcastAgent()
        self.host.voice_id = '89Hgu8DLVJRN9KMdp3YX'
        self.guest.voice_id = 'DuPq5RcxRjhgnMPfHutO'

        self.process_initial_prompt(input_prompt)
        print("Generate Podcast")
        self.generate_podcast()

    def __str__(self):
        out = ""
        host_b = True
        for message in self.get_podcast():
            if host_b:
                out+=("Host: " + message + "\n\n")
            else:
                out+=("Guest: " + message + "\n\n")
            host_b = not host_b
        return out
        
    def get_podcast(self):
        conversation = self.host.conversations[self.host.cur_conversation_id]
        out = []
        out += [conversation[0].response.choices[0].message.content + "\n"]
        for exchange in conversation[1:]:
            prompt = exchange.prompt.content
            response = exchange.response.choices[0].message.content
            
            out += [f"{prompt}"]
            out += [f"{response}"]

        return out

    def generate_podcast(self):
        for i in range(10):
            print(f'iteration: {i}')
            self.guest.prompt(self.host.get_latest_message().content.replace("as an AI language model",""))
            self.host.prompt(self.guest.get_latest_message().content.replace("as an AI language model",""))
        # self.save_podcast()

    def process_initial_prompt(self, input_prompt):
        narator = PodcastAgent()

        narator.prompt(f"""You are going to help me come up with an outline for a podcast.
The theme for the podcast is {input_prompt}
Extract specific keywords or phrases that are central to the theme. Note any specific names, places, events, or concepts mentioned. Based on the theme, brainstorm a list of potential topics that would interest the target audience. Ensure topics are varied yet cohesive within the podcast's theme. For each topic, develop subtopics or questions that would provoke discussion or provide informative content. Include potential anecdotes, data points, or relevant stories that could be incorporated.

Give me your answer in this exact format.
HOST:
A blurb of information for the host and 10 bullet points including specific questions they should ask

GUEST:
A blurb of informaiton for the guest and  10 bullet points with key information for the guest to be able the host’s questions with stories, anecdotes, facts, and opinion.


Feel free to make up any information you want. 
""")



        input_string = narator.get_latest_message().content.split('GUEST')

        self.host.prompt(f"you are going to interview me about: {input_string[0]} To start the interview, what would your first question be?")
        self.guest.prompt(f"Today, I am going to interview you. here is the general topic of the interview: {input_string[1]}.  are you ready to start your interview? my next message will be my first question.")
        



    def save_podcast(self,podcast_description=""):
        # Create the "podcasts" folder if it doesn't exist
        os.makedirs("./Podcasts", exist_ok=True)
        # Save conversation to file
        dir = os.path.join("./Podcasts/", self.filename)
        os.makedirs(dir, exist_ok=True)

        filepath = os.path.join(dir, "script")
        
        conversation = self.host.conversations[self.host.cur_conversation_id]
        with open(filepath, "w") as file:
            file.write("Podcast Conversation\n")
            file.write(f"Description: {podcast_description}\n\n")
            file.write(str(self))

        print(f"Podcast script saved to {filepath}")


    def concatenate_audioclips(self, audio_clip_paths, output_path):
        clips = [AudioFileClip(c) for c in audio_clip_paths]
        final_clip = concatenate_audioclips(clips)
        final_clip.write_audiofile(output_path)


    def to_mp3(self):
        pod = self.get_podcast()
        mp3_count = 1
        mp3_paths = []
        directory = f"./Podcasts/{self.filename.replace('.txt','')}/"

        host_b = True

        for message in pod:
            if host_b:
                tts = gTTS(message)
                # response = podcast.tts(message,podcast.host.voice_id)
            else:
                tts = gTTS(message)
                # response = podcast.tts(message,podcast.guest.voice_id)

            filename = "clip" + str(mp3_count) + ".mp3"
            
            filepath = os.path.join(directory, filename)
            mp3_paths += [filepath]

            if not os.path.exists(directory):
                os.makedirs(directory)

            tts.save(filepath)

            mp3_count+=1
            host_b = not host_b

        self.concatenate_audioclips(mp3_paths, directory + "podcast.mp3")

        pattern = r"clip\d+\.mp3"  # Regular expression pattern to match file names
        for filename in os.listdir(directory):
            if re.match(pattern, filename):
                file_path = os.path.join(directory, filename)
                os.remove(file_path)
        print(f"Removed file: {file_path}")


    def tts(self,text,voice_id):
        CHUNK_SIZE = 1024
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": API_Keys.ELEVENLABS_API_KEY
        }

        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }

        return requests.post(url, json=data, headers=headers)

