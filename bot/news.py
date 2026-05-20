import sys, os
sys.path.insert(0,os.getcwd())

import requests
import json
from typing import Any,Dict,List
'''
class news(object):

	def usage(self) -> str:
		return "This plugin is a News App"

	def handle_message(self, message: Dict[str, str], bot_handler: Any) -> None:
		bot_response = self.get_news_response(message, bot_handler)
		bot_handler.send_reply(message, bot_response)

handler_class = news
'''

def get_news_response(message: Dict[str, str], bot_handler: Any) -> str:
	content = message['content']
	words = content.lower().split()
	api_key = os.environ.get('NEWS_API_KEY')
	if not api_key:
		return "Error: NEWS_API_KEY environment variable is not set."
	articles = requests.get('https://newsapi.org/v2/everything?q=' + words[2] + '&apiKey=' + api_key).json()
	res = "" 
	i = 1
	if 'articles' not in articles:
		return "Error: Could not retrieve articles."
	for article in articles['articles'] :
		res = res + article['title'] + "\n" + article['url'] + "\n\n"
		i += 1
		if i == 5 :
			break  
	return res