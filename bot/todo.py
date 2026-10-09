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
        return "ToDo list initialized! 📝"
    if words[2] == "list":
        res = bot_handler.storage.get("list")
        if not res:
            return "Your ToDo list is empty! 📭"
        val = ""
        values = res.split("~")
        i = 1
        for temp in values:
            if temp.strip():
                val = val + str(i) + ". " + temp + "\n"
                i += 1
        return val.strip() if val else "Your ToDo list is empty! 📭"
    elif words[2] == "add":
        res = bot_handler.storage.get("list")
        res = res + " ".join(words[3::]) + "~"
        bot_handler.storage.put("list", res)
        return "Added to list. ✅"
    elif words[2] == "remove":
        index = int(words[3])
        res = bot_handler.storage.get("list")
        if not res:
            return "Your ToDo list is already empty. 📭"
        val = ""
        values = res.split("~")
        i = 1
        removed = False
        for temp in values:
            if not temp.strip():
                continue
            if i != index:
                val = val + temp + "~"
            else:
                removed = True
            i += 1
        bot_handler.storage.put("list", val)
        return "Removed from list. ✅" if removed else "Item not found in list. ⚠️"
