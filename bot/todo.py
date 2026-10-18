import sys
import os
sys.path.insert(0, os.getcwd())

import copy
import importlib
import random
from math import log10, floor

import re
from converter import utils
from typing import Any, Dict, List

'''
class todo(object):

	def usage(self) -> str:
		return "This plugin is a ToDo App"

	def handle_message(self, message: Dict[str, str], bot_handler: Any) -> None:
		bot_response = self.get_todo_response(message, bot_handler)
		bot_handler.send_reply(message, bot_response)

handler_class = todo
'''


def get_todo_response(message: Dict[str, str], bot_handler: Any) -> str:
    content = message["content"]
    words = content.split()

    if len(words) < 3:
        return "Invalid command. Try `@Jarvis help`"

    if words[2] == "start":
        bot_handler.storage.put("list", "")
        return "todo initialized"
    elif words[2] == "list":
        res = bot_handler.storage.get("list")
        if not res:
            return "Your todo list is empty! Add tasks using `@Jarvis todo add <task>`"
        val = ""
        values = res.split("~")[:-1]
        i = 1
        for temp in values:
            val = val + str(i) + ". " + temp + "\n"
            i += 1
        return val.strip()
    elif words[2] == "add":
        if len(words) < 4:
            return "Please provide a task to add. Example: `@Jarvis todo add Buy milk`"
        res = bot_handler.storage.get("list")
        if res is None:
            res = ""
        task = " ".join(words[3::])
        res = res + task + "~"
        bot_handler.storage.put("list", res)
        return f"Added '{task}' to list."
    elif words[2] == "remove":
        try:
            index = int(words[3])
        except (IndexError, ValueError):
            return "Please provide a valid task number to remove. Example: `@Jarvis todo remove 1`"
        res = bot_handler.storage.get("list")
        if not res:
            return "Your todo list is already empty!"
        values = res.split("~")[:-1]
        if index < 1 or index > len(values):
            return f"Invalid task number. Please provide a number between 1 and {len(values)}."
        val = ""
        i = 1
        for temp in values:
            if i != index:
                val = val + temp + "~"
            i += 1
        bot_handler.storage.put("list", val)
        return f"Task {index} removed from list."
