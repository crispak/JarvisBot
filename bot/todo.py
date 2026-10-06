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


def get_todo_response(message: Dict[str, str], bot_handler: Any) -> str:
    content = message["content"]
    words = content.split()

    if len(words) < 3:
        return "Please specify a todo command (start, add, remove, list). Try `@Jarvis help` for more details."

    if words[2] == "start":
        bot_handler.storage.put("list", "")
        return "todo initialized"

    if words[2] == "list":
        res = bot_handler.storage.get("list")
        if not res:
            return "Your todo list is empty. Add a task using `@Jarvis todo add <task>`"

        val = ""
        values = res.split("~")
        i = 1
        for temp in values:
            if temp.strip():
                val = val + str(i) + ". " + temp + "\n"
                i += 1

        if not val:
            return "Your todo list is empty. Add a task using `@Jarvis todo add <task>`"

        return val.strip()

    elif words[2] == "add":
        if len(words) < 4:
            return "Please specify a task to add. Example: `@Jarvis todo add Buy milk`"

        res = bot_handler.storage.get("list")
        if not res:
            res = ""
        res = res + " ".join(words[3::]) + "~"
        bot_handler.storage.put("list", res)
        return "Added to list."

    elif words[2] == "remove":
        if len(words) < 4:
            return "Please specify the task number to remove. Example: `@Jarvis todo remove 1`"

        try:
            index = int(words[3])
        except ValueError:
            return "Please provide a valid task number to remove. Example: `@Jarvis todo remove 1`"

        res = bot_handler.storage.get("list")
        if not res:
            return "Your todo list is already empty."

        val = ""
        values = res.split("~")
        i = 1
        removed = False
        for temp in values:
            if temp.strip():
                if i != index:
                    val = val + temp + "~"
                else:
                    removed = True
                i += 1

        if not removed:
            return f"Task {index} not found in your todo list."

        bot_handler.storage.put("list", val)
        return "Removed from list."

    return "Invalid todo command. Try `@Jarvis todo list` or `@Jarvis help`"
