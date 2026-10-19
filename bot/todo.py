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
    if words[2] == "start":
        bot_handler.storage.put("list", "")
        return "todo initialized"
    if words[2] == "list":
        res = bot_handler.storage.get("list")
        if not res:
            return "Your todo list is empty."

        values = [v for v in res.split("~") if v]
        if not values:
            return "Your todo list is empty."

        val = ""
        i = 1
        for temp in values:
            val += str(i) + ". " + temp + "\n"
            i += 1
        return val.strip()
    elif words[2] == "add":
        res = bot_handler.storage.get("list") or ""
        res = res + " ".join(words[3::]) + "~"
        bot_handler.storage.put("list", res)
        return "Added to list."
    elif words[2] == "remove":
        try:
            index = int(words[3])
        except (IndexError, ValueError):
            return "Please provide a valid task number to remove."

        res = bot_handler.storage.get("list") or ""
        values = [v for v in res.split("~") if v]

        if not (1 <= index <= len(values)):
            return "Task number not found."

        del values[index - 1]
        val = "~".join(values) + "~" if values else ""
        bot_handler.storage.put("list", val)
        return "Removed from list."
