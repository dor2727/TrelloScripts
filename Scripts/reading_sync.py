#!/usr/bin/env python3
import sys

from TrelloScripts.utils.consts import *
from TrelloScripts.utils.log    import log, initialize_logfile
from TrelloScripts.utils.utils  import *

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
	log(f"..[*] Synching cards : \"{source_board.name}\" --> \"{dest_board.name}\"")

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
	dest_lists_pos = [i.pos for i in dest_lists]

	some_high_number = max((i.pos for i in dest_lists), default=100_000)

	for index, l_dest in enumerate(dest_lists):
		l_source = get_item(source_lists, l_dest.name)
		if l_dest.pos > 200_000:
			log(f"......[*] Weird pos : {l_dest.pos}")

		suffix = ''
		if l_source is None:
			suffix = " (no source list found)"
			# check if there's no collisions
			if dest_lists_pos.count(l_dest.pos) > 1:
				new_pos = some_high_number + index*1000
			else:
				new_pos = l_dest.pos
		else:
			new_pos = l_source.pos

		if new_pos != l_dest.pos:
			log(f"..........[*] Moving {l_dest.name} from {l_dest.pos} to {new_pos}{suffix}")
			l_dest.move(new_pos)

def reset_lists_pos(board):
	log(f"...[*] Reseting list positions : \"{board.name}\"")

	for index, l in enumerate(sorted(board.all_lists(), key=lambda i: i.pos)):
		new_pos = (index+1) * 1000
		if new_pos != l.pos:
			log(f".........[*] Moving {l.name} from {l.pos} to {new_pos}")
			l.move(new_pos)

def sync(board_main, board_done, board_backlog, board_inspiration=None, board_wont_do=None):
	# sync main -> done
	# 	label: "Done"
	# sync main -> backlog
	# 	label: "ToBacklog"
	# sync backlog -> main
	# 	label: "ToReading"
	log(f"[*] Synching \"{board_main.name}\"")

	if (board_main is not None):
		reset_lists_pos(board_main)

	if (board_main is not None) and (board_done is not None):
		sync_boards     (board_main, board_done, "Done")
		sync_lists_order(board_main, board_done)

	if (board_main is not None) and (board_backlog is not None):
		sync_boards     (board_main   , board_backlog, "ToBacklog")
		sync_lists_order(board_main   , board_backlog)
		sync_boards     (board_backlog, board_main   , "ToReading")

	if (board_main is not None) and (board_inspiration is not None):
		sync_boards     (board_main   , board_inspiration, "TookInspiration")
		sync_lists_order(board_main   , board_inspiration)
	if (board_backlog is not None) and (board_inspiration is not None):
		sync_boards     (board_backlog, board_inspiration, "TookInspiration")

	if (board_main is not None) and (board_wont_do is not None):
		sync_boards     (board_main   , board_wont_do, "Wont do")
		sync_lists_order(board_main   , board_wont_do)
	if (board_backlog is not None) and (board_wont_do is not None):
		sync_boards     (board_backlog, board_wont_do, "Wont do")

def get_board_triplet(board_name, boards, prefix=""):
	# if a board doesn't exist - get_item returns None
	board_reading     = get_item(boards, f"{prefix}{board_name}")
	board_done        = get_item(boards, f"{prefix}{board_name} - Done")
	board_backlog     = get_item(boards, f"{prefix}{board_name} - Backlog")
	board_inspiration = get_item(boards, f"{prefix}{board_name} - TookInspiration")
	board_wont_do     = get_item(boards, f"{prefix}{board_name} - Wont do")

	return board_reading, board_done, board_backlog, board_inspiration, board_wont_do

def sync_reading_boards(all_boards):
	log("[*] Getting reading boards")

	# take only the reading boards
	reading_boards = [b for b in all_boards if "Reading" in b.name]
	# extract the names of the boards
	reading_board_names = set(map(
		lambda b: b.name.split(" - ")[1],
		reading_boards
	))
	# iterate each name, and sync it.
	for name in reading_board_names:
		sync(*get_board_triplet(name, reading_boards, prefix="Reading - "))

def sync_all_boards(all_boards):
	sync_reading_boards(all_boards)

	for board_name in [
		"Games",
		"Programming Projects",
		"Cooking",
		"Shopping",
	]:
		log(f"[*] Getting \"{board_name}\" boards")
		sync(*get_board_triplet(board_name, all_boards))


@initialize_logfile("reading_sync.log")
def main():
	all_boards = get_all_boards()

	if len(sys.argv) == 1:
		sync_all_boards(all_boards)
	else:
		board_name = sys.argv[1]
		log(f"[*] Getting \"{board_name}\" boards")
		sync(*get_board_triplet(board_name, all_boards))


	log("[*] Done")


if __name__ == '__main__':
	main()
