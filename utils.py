#!/usr/bin/env python3
from trello import TrelloClient
import os

from TrelloScripts.consts import *
from TrelloScripts.log import log, set_verbose


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
def get_client():
	client = TrelloClient(
		api_key    = read("key"),
		api_secret = read("secret"),
		token      = read("token"),
	)
	return client


#
# Card utils
#

def get_item(all_list, item_name):
	return next(
		filter(
			lambda i: i.name == item_name,
			all_list
		)
	)


def is_labeled(card, label_name=None):
	# if label_name is a string, check if the card has that label
	if label_name:
		if card.labels:
			for l in card.labels:
				if l.name == label_name:
					return True
		return False
	# Otherwise, simply check if there are any labels
	else:
		return bool(card.labels)


# TODO: fix this one
def move_boards(all_boards, source_board_name, dest_board_name, label_name):
	log(f"[*] Moving cards : {source_board_name} --> {dest_board_name}")
	for subject in SUBJECTS:
		log(f"..[*] Subject - {subject}")

		log(f".....[*] Reading board \"{source_board_name}\"")
		source_board = get_board(all_boards, source_board_name, subject)
		label        = get_item(source_board.get_labels(), label_name)

		log(f".....[*] Reading board \"{dest_board_name}\"")
		dest_board = get_board(all_boards, dest_board_name  , subject)
		dest_lists = dest_board.all_lists()

		log(".....[*] Iterating cards")
		counter = 0
		for c in source_board.all_cards():
			if is_labeled(c, label_name):
				log(f"...[*] found card - {c.name} - {label_name}")
				# remove the label
				log(".......[*] Removing label")
				c.remove_label(label)

				# find the dest list
				log(".......[*] Getting destination list")
				list_name = c.get_list().name
				try:
					destination_list = get_item(dest_lists, list_name)
				except:
					log("...........[*] Creating destination list")
					destination_list = dest_board.add_list(list_name, "bottom")

				log(".......[*] Changing board")
				c.change_board(dest_board.id, destination_list.id)

				log(".......[*] Done")
				counter += 1
		log(f"....[*] moved {counter} cards")
