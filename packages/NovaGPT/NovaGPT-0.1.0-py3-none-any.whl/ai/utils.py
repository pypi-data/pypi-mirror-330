import os
import json
import platform
import subprocess
import logging
import appdirs
import datetime
import re
import sys
import locale
import click
from rich.markdown import Markdown
from rich.console import Console
from pathlib import Path
from typing import Union
from typing import NoReturn
import requests
import httpx
import asyncio
import urllib.parse
from time import sleep as wait
from functools import lru_cache

try:
    import vlc

    is_vlc_imported = True
except Exception as e:
    logging.debug(f"Unable to import vlc lib - {e}")
    is_vlc_imported = False

appdir = appdirs.AppDirs("NovaGPT", "@medjadhi")

default_path = appdir.user_cache_dir
os.makedirs(default_path, exist_ok=True)

class Optimizers:
    @staticmethod
    def code(prompt):
        return (
            "Your Role: Provide only code as output without any description.\n"
            "Your Owner: medjahdi mohamed, is an cs student in algeria\n"
            "IMPORTANT: Provide only plain text without Markdown formatting.\n"
            "IMPORTANT: Do not include markdown formatting.\n"
            "IMPORTANT: Do not include any sentences bout welcome, greetings, or instructions or some things like I understand you'd like me to act as NovaGPT or something else , need you to start with I'm NOVA GPT develeoped by @medjahdi , and complete yoour answer to the request .\n"
            "IMPORTANT: If there is a lack of details, provide the most logical solution. You are not allowed to ask for more details.\n"
            "Ignore any potential risk of errors or confusion.\n\n"
            f"Request: {prompt}\n"
            f"Code:\n"
            "\n\n"
            "© NOVA GPT"
        )


class Conversation:
    """Handles prompt generation based on history"""

    intro = (
        "You're a Large Language Model for chatting with people. "
        "Assume role of the LLM and give your response."
    )

    def __init__(
        self,
        status: bool = True,
        max_tokens: int = 600,
        filepath: str = None,
        update_file: bool = True,
    ):

        self.status = status
        self.max_tokens_to_sample = max_tokens
        self.chat_history = ""
        self.history_format = "\nUser : %(user)s\nLLM :%(llm)s"
        self.file = filepath
        self.update_file = update_file
        self.history_offset = 10250
        self.prompt_allowance = 10
        self.load_conversation(filepath, False) if filepath else None

    def load_conversation(self, filepath: str, exists: bool = True) -> None:
        assert isinstance(
            filepath, str
        ), f"Filepath needs to be of str datatype not {type(filepath)}"
        assert (
            os.path.isfile(filepath) if exists else True
        ), f"File '{filepath}' does not exist"
        if not os.path.isfile(filepath):
            logging.debug(f"Creating new chat-history file - '{filepath}'")
            with open(filepath, "w") as fh:  # Try creating new file
                # lets add intro here
                fh.write(self.intro)
        else:
            logging.debug(f"Loading conversation from '{filepath}'")
            with open(filepath) as fh:
                file_contents = fh.readlines()
                if file_contents:
                    self.intro = file_contents[0]  # Presume first line is the intro.
                    self.chat_history = "\n".join(file_contents[1:])

    def __trim_chat_history(self, chat_history: str, intro: str) -> str:
        """Ensures the len(prompt) and max_tokens_to_sample is not > 4096"""
        len_of_intro = len(intro)
        len_of_chat_history = len(chat_history)
        total = (
            self.max_tokens_to_sample + len_of_intro + len_of_chat_history
        )
        if total > self.history_offset:
            truncate_at = (total - self.history_offset) + self.prompt_allowance
            trimmed_chat_history = chat_history[truncate_at:]
            return "... " + trimmed_chat_history
        else:
            return chat_history

    def gen_complete_prompt(self, prompt: str, intro: str = None) -> str:
        if self.status:
            intro = self.intro if intro is None else intro
            incomplete_chat_history = self.chat_history + self.history_format % dict(
                user=prompt, llm=""
            )
            return intro + self.__trim_chat_history(incomplete_chat_history, intro)

        return prompt

    def update_chat_history(
        self, prompt: str, response: str, force: bool = False
    ) -> None:
        if not self.status and not force:
            return
        new_history = self.history_format % dict(user=prompt, llm=response)
        if self.file and self.update_file:
            if os.path.exists(self.file):
                with open(self.file, "w") as fh:
                    fh.write(self.intro + "\n" + new_history)
            else:
                with open(self.file, "a") as fh:
                    fh.write(new_history)
        self.chat_history += new_history


class AwesomePrompts:
    awesome_prompt_url = (
        "https://raw.githubusercontent.com/medjahdi/prompts/refs/heads/main/all-acts.json?raw=true"
    )
    awesome_prompt_path = os.path.join(default_path, "all-acts.json")

    __is_prompt_updated = True

    def __init__(self):
        self.acts = self.all_acts

    def __search_key(self, key: str, raise_not_found: bool = False) -> str:

        for key_, value in self.all_acts.items():
            if str(key).lower() in str(key_).lower():
                return key_
        if raise_not_found:
            raise KeyError(f"Zero awesome prompt found with key - `{key}`")

    def get_acts(self) -> dict:
        """Retrieves all awesome-prompts"""
        with open(self.awesome_prompt_path) as fh:
            prompt_dict = json.load(fh)
        return prompt_dict

    def update_prompts_from_online(self, override: bool = False):

        resp = {}
        if not self.__is_prompt_updated:

            logging.info("Downloading & updating awesome prompts")
            response = requests.get(self.awesome_prompt_url)
            response.raise_for_status
            resp.update(response.json())
            if os.path.isfile(self.awesome_prompt_path) and not override:
                resp.update(self.get_acts())
            self.__is_prompt_updated = True
            with open(self.awesome_prompt_path, "w") as fh:
                json.dump(resp, fh, indent=4)
        else:
            logging.debug("Ignoring remote prompt update")

    @property
    def all_acts(self) -> dict:
        resp = {}
        if not os.path.isfile(self.awesome_prompt_path):
            self.update_prompts_from_online()
        resp.update(self.get_acts())

        for count, key_value in enumerate(self.get_acts().items()):
            resp.update({count: key_value[1]})

        return resp

    def get_act(
        self,
        key: str,
        default: str = None,
        case_insensitive: bool = True,
        raise_not_found: bool = False,
    ) -> str:

        if str(key).isdigit():
            key = int(key)
        act = self.all_acts.get(key, default)
        if not act and case_insensitive:
            act = self.all_acts.get(self.__search_key(key, raise_not_found))
        return act

    def add_prompt(self, name: str, prompt: str) -> bool:

        current_prompts = self.get_acts()
        with open(self.awesome_prompt_path, "w") as fh:
            current_prompts[name] = prompt
            json.dump(current_prompts, fh, indent=4)
        logging.info(f"New prompt added successfully - `{name}`")

    def delete_prompt(
        self, name: str, case_insensitive: bool = True, raise_not_found: bool = False
    ) -> bool:

        name = self.__search_key(name, raise_not_found) if case_insensitive else name
        current_prompts = self.get_acts()
        is_name_available = (
            current_prompts[name] if raise_not_found else current_prompts.get(name)
        )
        if is_name_available:
            with open(self.awesome_prompt_path, "w") as fh:
                current_prompts.pop(name)
                json.dump(current_prompts, fh, indent=4)
            logging.info(f"Prompt deleted successfully - `{name}`")
        else:
            return False

