#!/usr/bin/env python3
from trello import TrelloClient
import os

from TrelloScripts.consts import *
from TrelloScripts.log import log, set_verbose
from TrelloScripts.utils_web import read_link, is_url


#
# File utils
#

def read(filename):
	try:
		return open(filename).read().strip()
	except:
		filename = os.path.join(
			os.path.dirname(__file__),
			filename
		)
		return open(filename).read().strip()

#
# Client utils
#
CLIENT = None
def get_client():
	global CLIENT

	if CLIENT is None:
		CLIENT = TrelloClient(
			api_key    = read("key"),
			api_secret = read("secret"),
			token      = read("token"),
		)

	return CLIENT

def get_all_boards():
	client = get_client()
	log("[*] Getting boards")
	all_boards = client.list_boards()
	return all_boards

#
# Card utils
#

def get_item(all_list, item_name, case_sensitive=True):
	if case_sensitive:
		filter_function = lambda obj: obj.name == item_name
	else:
		item_name_lower = item_name.lower()
		filter_function = lambda obj: obj.name.lower() == item_name_lower

	try:
		return next(
			filter(
				filter_function,
				all_list
			)
		)
	except:
		return None


def is_labeled(card, label_name=None):
	# if label_name is a string, check if the card has that label
	if label_name:
		return any(l.name == label_name for l in card.labels)
	# Otherwise, simply check if there are any labels
	else:
		return bool(card.labels)

def get_first_attachment(card):
	for attachment in self.card.attachments:
		# youtube cover
		if attachment["name"] == "0.jpg":
			continue

		return attachment

	return None
