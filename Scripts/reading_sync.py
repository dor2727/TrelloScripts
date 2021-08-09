#!/usr/bin/env python3

from TrelloScripts.consts                import *
from TrelloScripts.log                   import log, log_initialize
from TrelloScripts.utils                 import *

set_verbose(10)

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

def sync_boards(source, dest, label_name):
	log(f".[*] Synching : \"{source.name}\" --> \"{dest.name}\"")
	pass

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