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
    if words[2] == "start":
        bot_handler.storage.put("list", "")
        return "todo initialized"
    if words[2] == "list":
        res = bot_handler.storage.get("list")
        if not res:
            return "Your TODO list is empty! Add a task with `@Jarvis todo add <task>`"

        values = [v for v in res.split("~") if v.strip()]
        if not values:
            return "Your TODO list is empty! Add a task with `@Jarvis todo add <task>`"

        val = ""
        for i, temp in enumerate(values, 1):
            val += f"{i}. {temp}\n"
        return val.strip()
    elif words[2] == "add":
        res = bot_handler.storage.get("list")
        res = res + " ".join(words[3::]) + "~"
        bot_handler.storage.put("list", res)
        return "Added to list."
    elif words[2] == "remove":
        try:
            index = int(words[3])
        except (IndexError, ValueError):
            return "Please provide a valid task number to remove. Usage: `@Jarvis todo remove <task_number>`"

        res = bot_handler.storage.get("list")
        values = [v for v in res.split("~") if v.strip()]

        if not (1 <= index <= len(values)):
            return f"Task number {index} not found. You have {len(values)} tasks in your list."

        values.pop(index - 1)
        val = "~".join(values) + "~" if values else ""
        bot_handler.storage.put("list", val)
        return "Removed from list."
