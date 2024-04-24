from typing import Iterable
import os
import io
import time
from datetime import datetime
from pathlib import Path


from AgentSettings import AgentSettings

from openai.types.beta.threads.message_content_image_file import MessageContentImageFile
from openai.types.beta.threads.message_content_text import MessageContentText
from openai.types.beta.threads.messages import MessageFile
from openai.types import FileObject
from PIL import Image
from ArgumentException import ArgumentExceptionError


class AssistantAgent:
    def __init__(self, settings, client, name, instructions, data_folder, tools_list, keep_state: bool = False, fn_calling_delegate=None):
        if name is None:
            raise ArgumentExceptionError("name parameter missing")
        if instructions is None:
            raise ArgumentExceptionError("instructions parameter missing")
        if tools_list is None:
            raise ArgumentExceptionError("tools_list parameter missing")

        self.assistant = None
        self.settings = settings
        self.client = client
        self.name = name
        self.instructions = instructions
        self.data_folder = data_folder
        self.tools_list = tools_list
        self.fn_calling_delegate = fn_calling_delegate
        self.keep_state = keep_state
        self.ai_threads = []
        self.ai_files = []
        self.file_ids = []
        self.get_agent()

    def upload_file(self, path: str) -> FileObject:
        print(path)
        with Path(path).open("rb") as f:
            return self.client.files.create(file=f, purpose="assistants")

    def upload_all_files(self):
        files_in_folder = os.listdir(self.data_folder)
        local_file_list = []
        for file in files_in_folder:
            filePath = self.data_folder + file
            assistant_file = self.upload_file(filePath)
            self.ai_files.append(assistant_file)
            local_file_list.append(assistant_file)
        self.file_ids = [file.id for file in local_file_list]

    def get_agent(self):
        # Implement the get agent logic here
    

    def process_prompt(self, user_name: str, user_id: str, prompt: str) -> None:

        # Implement the process prompt logic here

    def read_assistant_file(self, file_id: str):
        # Implement the read logic here

    def print_messages(self, name: str, messages: Iterable[MessageFile]) -> None:
        # Implement the print logic here

    def cleanup(self):
        print(self.client.beta.assistants.delete(self.assistant.id))
        print("Deleting: ", len(self.ai_threads), " threads.")
        for thread in self.ai_threads:
            print(self.client.beta.threads.delete(thread.id))
        print("Deleting: ", len(self.ai_files), " files.")
        for file in self.ai_files:
            print(self.client.files.delete(file.id))
