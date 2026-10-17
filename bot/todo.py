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
        return "Invalid todo command. Use `@Jarvis todo start`, `list`, `add <task>`, or `remove <task-number>`."

    if words[2] == "start":
        bot_handler.storage.put("list", "")
        return "Todo list initialized! Start adding tasks with `@Jarvis todo add <task>`."

    elif words[2] == "list":
        res = bot_handler.storage.get("list")
        if not res:
            return "Your todo list is currently empty. Add tasks using `@Jarvis todo add <task>`."

        values = [x for x in res.split("~") if x.strip()]
        if not values:
            return "Your todo list is currently empty. Add tasks using `@Jarvis todo add <task>`."

        val = "*Your To-Do List:*\n"
        for i, temp in enumerate(values, 1):
            val += f"{i}. {temp}\n"
        return val.strip()

    elif words[2] == "add":
        if len(words) < 4:
            return "Please specify a task to add. Usage: `@Jarvis todo add <task>`"

        task = " ".join(words[3:])
        res = bot_handler.storage.get("list")
        if res is None:
            res = ""

        res += f"{task}~"
        bot_handler.storage.put("list", res)
        return f"Added '{task}' to your list."

    elif words[2] == "remove":
        if len(words) < 4:
            return "Please provide a task number to remove. Usage: `@Jarvis todo remove <task-number>`"

        try:
            index = int(words[3])
        except ValueError:
            return "Please provide a valid task number to remove. Usage: `@Jarvis todo remove <task-number>`"

        res = bot_handler.storage.get("list")
        if not res:
            return "Your todo list is already empty."

        values = [x for x in res.split("~") if x.strip()]
        if not (1 <= index <= len(values)):
            return f"Task number {index} not found. You currently have {len(values)} task{'s' if len(values) != 1 else ''}."

        removed_task = values.pop(index - 1)
        val = "~".join(values) + ("~" if values else "")
        bot_handler.storage.put("list", val)
        return f"Removed '{removed_task}' from your list."

    else:
        return "Unknown todo command. Use `start`, `list`, `add <task>`, or `remove <task-number>`."
