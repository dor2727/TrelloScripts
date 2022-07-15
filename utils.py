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


#
# Card utils
#

def get_item(all_list, item_name):
	try:
		return next(
			filter(
				lambda i: i.name == item_name,
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
