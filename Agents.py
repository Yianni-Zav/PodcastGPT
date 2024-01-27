import os
from copy import copy
from dataclasses import dataclass
from typing import List, Dict, Any
import json 
import API_Keys

import openai
import tiktoken

openai.api_key = API_Keys.OPENAI_KEY
OPENAI_MODEL = "gpt-3.5-turbo"

@dataclass
class Message:
    role: str
    content: str

@dataclass
class Exchange:
    prompt: Message
    response: Dict[str, Any]

# look into presence penalties!!!!!
def call_GPT(agent):

    response = openai.ChatCompletion.create(model=OPENAI_MODEL, 
                                            messages=agent.get_messages_for_call(),
                                            temperature=agent.temperature)
    return response


class PodcastAgent:
    def __init__(self):
        self.name = ""
        self.conversations = {}
        self.cur_conversation_id = None
        self.new_conversation_id = 0
        self.message_to_prompt = ""
        self.temperature = 0
        self.system_settings = {}

    # GETTERS
    def get_cur_convo(self) -> List[Message]:
        messages = self._parse_conversation(self.cur_conversation_id)
        if self.message_to_prompt:
            messages += [Message(role="user", content=self.message_to_prompt)]
            
        return messages

    def get_messages_for_call(self): 
        messages = [{"role":message.role,"content":message.content} for message in self.get_cur_convo()]
        if self.cur_conversation_id in self.system_settings:
            messages = [{"role":"system","content":self.system_settings[self.cur_conversation_id]}] + messages
        return messages 

    def get_latest_message(self) -> Message:
        cur_conversation = self.conversations.get(self.cur_conversation_id, None)
        if cur_conversation is None:
            return Message(role="", content="")

        messages = self.get_cur_convo()
        if messages:
            return messages[-1]

        return Message(role="", content="")

    # SETTERS
    def set_personality(self,personality):
        self.system_settings[self.cur_conversation_id] = personality

    # PUBLIC METHODS
    def prompt(self,prompt,new_conversation: bool = False):
        if new_conversation or self.cur_conversation_id is None:
            self.cur_conversation_id = self.new_conversation_id
            self.new_conversation_id += 1

        self.message_to_prompt = prompt
        response = call_GPT(self)

        self.conversations.setdefault(self.cur_conversation_id, [])
        self.conversations[self.cur_conversation_id] += [Exchange(prompt=Message(role="user",content=prompt), response=response)]

        self.message_to_prompt = ""
        return self.get_latest_message().content

    # PRIVATE METHODS
    def _parse_conversation(self, conversation_id: int) -> List[Message]:
        # print(self.)
        conversation = self.conversations.get(conversation_id, [])
        messages = []
        
        for exchange in conversation:
            prompt = exchange.prompt
            response = exchange.response

            user_message = Message(role="user", content=prompt.content)
            assistant_message = Message(role="assistant", content=response["choices"][0]["message"]["content"])
            
            messages.append(user_message)
            messages.append(assistant_message)

        return messages
        


    
    