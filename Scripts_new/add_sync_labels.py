#!/usr/bin/env python3

import sys

from TrelloScripts.utils import log, iterate_boards

from trello import Board, TrelloClient

LABEL_COLOR = {
	"Done": "green",
	"ToBacklog": "lime",
	"ToMain": "green",
	"TookInspiration": "green",
	"Wont do": "black",
}

def main():
	if len(sys.argv) < 2:
		print(f"Usage: {sys.argv[0]} board_name [board_name ...]")
		sys.exit(1)

	boards = sys.argv[1:]

	iterate_boards(
		log_name="export",
		boards_filter=lambda b: b.name in boards,
		apply_to_board=add_labels_to_board,
	)

def apply_to_board(client: TrelloClient, board: Board):
	current_board_labels = board.get_labels()
	current_board_labels_names = [l.name for l in current_board_labels]

	for label_name, label_color in LABEL_COLOR.items():
		if label_name in current_board_labels_names:
			pass
		else:
			board.add_label(label_name, label_color)

if __name__ == '__main__':
	main()
