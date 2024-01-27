from Agents import PodcastAgent
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import re
import sys
import subprocess
from datetime import datetime
from tempfile import gettempdir
from moviepy.editor import concatenate_audioclips, AudioFileClip
import API_Keys



class Podcast:
    def __init__(self, input_string):
        try:
            with open(input_string, 'r') as f:
                self.filename = input_string.split('/')[-1]
                self.file_text = f.read()
        except FileNotFoundError:
            self.filename = ""
            self.file_text = input_string
        
        self.host = PodcastAgent()
        self.guest = PodcastAgent()

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
        out += [conversation[0].response["choices"][0]["message"]["content"] + "\n"]
        for exchange in conversation[1:]:
            prompt = exchange.prompt.content
            response = exchange.response["choices"][0]["message"]["content"]
            
            out += [f"{prompt}"]
            out += [f"{response}"]

        return out

    def generate_podcast(self):
        self.init_agents()
        for i in range(10):
            self.guest.prompt(self.host.get_latest_message().content.replace("as an AI language model",""))
            self.host.prompt(self.guest.get_latest_message().content.replace("as an AI language model",""))
        self.save_podcast()

    def init_agents(self):
        narator = PodcastAgent()
        
        narator.prompt(f"""
        Read the following text

        {self.file_text}

        You are going to be hosting a Podcast on the topics described in the text. I have three questions for you
        1. Give me a summary of the text including any information that you think could be helpful while you’re interviewing your guest.
        2. describe your ideal podcast guest, but direct it at "you" like "you are someone with strong knowledge of the topic....
        3. describe an ideal podcast host, again direct it at "you"
        4. generate me a filename for this text.

        Answer in the following format

        SUMMARY: [answer to questions 1]

        GUEST: [Answer to question 2]

        HOST: [Answer to question 3]

        FILENAME: [Answer to question 4]
        """)

        input_string = narator.get_latest_message().content

        # Extracting the summary, traits, and guest sections
        summary = re.search(r'SUMMARY: (.*?)GUEST:', input_string, re.DOTALL).group(1).strip()
        guest_desc = re.search(r'GUEST: (.*?)HOST:', input_string, re.DOTALL).group(1).strip()
        host_desc = re.search(r'HOST: (.*?)FILENAME:', input_string, re.DOTALL).group(1).strip()
        filename = re.search(r'FILENAME: (.*)', input_string, re.DOTALL).group(1).strip()

        if not self.filename:
            self.filename = filename
            dir = "../TestTexts/"
            filepath = os.path.join(dir,filename)
            with open(filepath, 'w') as file:
                file.write(self.file_text)

        self.host.prompt(f"you are going to interview me about: {summary} {host_desc} To start the interview, what would your first question be?")
        self.guest.prompt(f"Today, I am going to interview you. here is the general topic of the interview: {summary}. {guest_desc} are you ready to start your interview? my next message will be my first question.")
        



    def save_podcast(self,podcast_description=""):
        # Create the "podcasts" folder if it doesn't exist
        os.makedirs("../Podcasts", exist_ok=True)
        # Save conversation to file
        dir = os.path.join("../Podcasts/", self.filename)
        os.makedirs(dir, exist_ok=True)

        filepath = os.path.join(dir, "script")
        
        conversation = self.host.conversations[self.host.cur_conversation_id]
        with open(filepath, "w") as file:
            file.write("Podcast Conversation\n")
            file.write(f"Description: {podcast_description}\n\n")
            file.write(str(self))

        print(f"Podcast script saved to {filepath}")


# 1. It is a verb that means to give or grant something to someone.
# 2. It is often used in the context of honor, recognition, or a special privilege.
# 3. The word starts with the letter "B" and has seven letters in total.
# 4. Synonyms for this word include confer, present, and grant.
# 5. The opposite of this word is "withhold."
    def concatenate_audioclips(self, audio_clip_paths, output_path):
        clips = [AudioFileClip(c) for c in audio_clip_paths]
        final_clip = concatenate_audioclips(clips)
        final_clip.write_audiofile(output_path)


    def to_mp3(self):
        session = Session(aws_access_key_id=API_Keys.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=API_Keys.AWS_SECRET_ACCESS_KEY, 
                          region_name="us-east-1")
        polly = session.client("polly")

        pod = self.get_podcast()
        mp3_count = 1
        mp3_paths = []
        directory = f"../Podcasts/{self.filename.replace('.txt','')}/"

        host_b = True
        
        for message in pod:
            if host_b:
                response = polly.synthesize_speech(VoiceId='Kendra',
                                                OutputFormat='mp3', 
                                                Text = message,
                                                Engine = 'neural')
            else:
                response = polly.synthesize_speech(VoiceId='Joey',
                                                OutputFormat='mp3', 
                                                Text = message,
                                                Engine = 'neural')

            filename = "clip" + str(mp3_count) + ".mp3"
            
            filepath = os.path.join(directory, filename)
            mp3_paths += [filepath]

            if not os.path.exists(directory):
                os.makedirs(directory)

            with open(filepath, 'wb') as f:
                f.write(response['AudioStream'].read())

            mp3_count+=1
            host_b = not host_b
        
        self.concatenate_audioclips(mp3_paths, directory + "podcast.mp3")

        pattern = r"clip\d+\.mp3"  # Regular expression pattern to match file names
        for filename in os.listdir(directory):
            if re.match(pattern, filename):
                file_path = os.path.join(directory, filename)
                os.remove(file_path)
                print(f"Removed file: {file_path}")



