#!/usr/bin/env python3
import os

from trello import TrelloClient

from .consts import *
from .log import log

#
# File utils
#


def try_read(file_path):
	try:
		return open(file_path).read().strip()
	except:
		return None


def read(filename):
	if (result := try_read(filename)) is not None:
		return result

	path_in_directory = os.path.join(os.path.dirname(__file__), filename)
	if (result := try_read(path_in_directory)) is not None:
		return result

	path_in_secrets = os.path.join(MAIN_FOLDER, "secrets", filename)
	return try_read(path_in_secrets)


#
# Client utils
#
CLIENT = None


def get_client():
	global CLIENT

	if CLIENT is None:
		CLIENT = TrelloClient(
			api_key=read("key"),
			api_secret=read("secret"),
			token=read("token"),
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
		return next(filter(filter_function, all_list))
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
	for attachment in card.attachments:
		# youtube cover
		if attachment["name"] == "0.jpg":
			continue

		return attachment

	return None
