#!/usr/bin/env python3

from TrelloScripts.consts import *
from TrelloScripts.log    import log, log_initialize, set_logfile
from TrelloScripts.utils  import *

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

	# log("...[*] Iterating cards")
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

	if counter:
		log(f"...[*] moved {counter} cards")

def sync_lists_order(source_board, dest_board):
	log(f"...[*] Synching lists : \"{source_board.name}\" --> \"{dest_board.name}\"")
	source_lists = source_board.all_lists()
	dest_lists = dest_board.all_lists()

	some_high_number = max((i.pos for i in dest_lists), default=100)

	for index, l_dest in enumerate(dest_lists):
		l_source = get_item(source_lists, l_dest.name)

		suffix = ''
		if l_source is None:
			suffix = " (no source list found)"
			new_pos = some_high_number*10 + index
		else:
			new_pos = l_source.pos

		if new_pos != l_dest.pos:
			log(f"..........[*] Moving {l_dest.name} from {l_dest.pos} to {new_pos}{suffix}")
			l_dest.move(new_pos)

def sync(board_reading, board_done, board_backlog):
	# sync reading -> done
def sync(board_main, board_done, board_backlog):
	# sync main -> done
	# 	label: "Done"
	# sync main -> backlog
	# 	label: "ToBacklog"
	# sync backlog -> main
	# 	label: "ToReading"

	if (board_reading is not None) and (board_done is not None):
		sync_boards(board_reading, board_done, "Done")
	if (board_main is not None) and (board_done is not None):
		sync_boards(board_main, board_done, "Done")

	if (board_reading is not None) and (board_backlog is not None):
		sync_boards(board_reading, board_backlog, "ToBacklog")
		sync_boards(board_backlog, board_reading, "ToReading")
	if (board_main is not None) and (board_backlog is not None):
		sync_boards(board_main, board_backlog, "ToBacklog")
		sync_boards(board_backlog, board_main, "ToReading")

def get_board_triplet(board_name, boards, prefix=""):
	# if a board doesn't exist - get_item returns None
	board_reading = get_item(boards, f"{prefix}{board_name}")
	board_done    = get_item(boards, f"{prefix}{board_name} - Done")
	board_backlog = get_item(boards, f"{prefix}{board_name} - Backlog")

	return board_reading, board_done, board_backlog

def main():
	set_logfile("reading_sync.log")

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
		sync(*get_board_triplet(name, reading_boards, prefix="Reading - "))

	log("[*] Getting Programming boards")
	sync(*get_board_triplet("Programming Projects", all_boards))

	log("[*] Getting Cooking boards")
	sync(*get_board_triplet("Cooking", all_boards))

	log("[*] Done")


if __name__ == '__main__':
	main()