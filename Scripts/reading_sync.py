#!/usr/bin/env python3

from TrelloScripts.consts                import *
from TrelloScripts.log                   import log, log_initialize, set_logfile
from TrelloScripts.utils                 import *

set_verbose(20)

"""
TODO

1) iterate boards on organization "Reading"
2) check if respective board exists on "Reading - Done"
3) if so, sync both ways
	3.1) "Reading"           has a label "done"

Similarly for "Reading" and "Reading - Backlog"
	3.2) "Reading"           has a label "ToBacklog"
	3.3) "Reading - Backlog" has a label "ToReading"

"""


def sync_boards(source_board, dest_board, label_name):
	log(f".[*] Synching : \"{source_board.name}\" --> \"{dest_board.name}\"")

	label = get_item(source_board.get_labels(), label_name)
	dest_lists = dest_board.all_lists()

	log("...[*] Iterating cards")
	counter = 0

	for c in source_board.all_cards():
		if is_labeled(c, label_name):
			log(f".....[*] found card - {c.name} - {label_name}")

			# remove the label
			log(".........[*] Removing label")
			c.remove_label(label)

			# find the dest list
			log(".........[*] Getting destination list")
			list_name = c.get_list().name

			destination_list = get_item(dest_lists, list_name)
			if destination_list is None:
				log(".............[*] Creating destination list")
				destination_list = dest_board.add_list(list_name, "bottom")
				# update the variable
				dest_lists = dest_board.all_lists()

			log(".........[*] Changing board")
			c.change_board(dest_board.id, destination_list.id)

			log(".........[*] Done")
			counter += 1

	log(f"...[*] moved {counter} cards")


def sync(board_reading, board_done, board_backlog):
	# sync reading -> done
	# 	label: "Done"
	# sync reading -> backlog
	# 	label: "ToBacklog"
	# sync backlog -> reading
	# 	label: "ToReading"

	if (board_reading is not None) and (board_done is not None):
		sync_boards(board_reading, board_done, "Done")

	if (board_reading is not None) and (board_backlog is not None):
		sync_boards(board_reading, board_backlog, "ToBacklog")
		sync_boards(board_backlog, board_reading, "ToReading")

def get_board_triplet(board_name, boards):
	# if a board doesn't exist - get_item returns None
	board_reading = get_item(boards, f"Reading - {board_name}")
	board_done    = get_item(boards, f"Reading - {board_name} - Done")
	board_backlog = get_item(boards, f"Reading - {board_name} - Backlog")

	return board_reading, board_done, board_backlog

def main():
	set_logfile("reading_sync")

	log_initialize()

	client = get_client()

	# get all the boards
	log("[*] Getting reading boards")
	all_boards = client.list_boards()

	# take only the reading boards
	reading_boards = [b for b in all_boards if "Reading" in b.name]

	# extract the names of the boards
	reading_board_names = list(set([
		b.name.split(" - ")[1]
		for b in reading_boards
	]))

	# iterate each name, and sync it.
	for name in reading_board_names:
		boards = get_board_triplet(name, reading_boards)
		sync(*boards)

	log("[*] Done")


if __name__ == '__main__':
	main()