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
        return "Please specify a todo command. Examples: `@Jarvis todo start`, `@Jarvis todo add <task>`, `@Jarvis todo list`, or `@Jarvis todo remove <task_number>`"

    try:
        res = bot_handler.storage.get("list")
    except KeyError:
        res = None

    if words[2] == "start":
        bot_handler.storage.put("list", "")
        return "Todo list initialized. Type `@Jarvis todo add <task>` to add a task."

    if res is None and words[2] in ["list", "add", "remove"]:
        return "Todo list not initialized. Type `@Jarvis todo start` to begin."

    if words[2] == "list":
        if not res:
            return "Your Todo list is empty. Add tasks using `@Jarvis todo add <task>`."

        val = ""
        values = [t for t in res.split("~") if t.strip()]
        if not values:
            return "Your Todo list is empty. Add tasks using `@Jarvis todo add <task>`."

        for i, temp in enumerate(values, 1):
            val += str(i) + ". " + temp + "\n"
        return val.strip()

    elif words[2] == "add":
        task = " ".join(words[3:])
        if not task.strip():
             return "Please specify a task to add. Example: `@Jarvis todo add Buy milk`"
        res = res + task + "~"
        bot_handler.storage.put("list", res)
        return f"Added '{task}' to your list."

    elif words[2] == "remove":
        try:
            index = int(words[3])
        except (IndexError, ValueError):
            return "Please specify a valid task number to remove. Example: `@Jarvis todo remove 1`"

        values = [t for t in res.split("~") if t.strip()]

        if index < 1 or index > len(values):
            return f"Task number {index} not found. Type `@Jarvis todo list` to see your tasks."

        removed_task = values[index - 1]

        val = ""
        for i, temp in enumerate(values, 1):
            if i != index:
                val = val + temp + "~"

        bot_handler.storage.put("list", val)
        return f"Removed '{removed_task}' from your list."
    else:
        return "Invalid todo command. Available commands: start, list, add, remove."
