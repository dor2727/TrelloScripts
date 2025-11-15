# manual add total time
# run from /home/me/Dropbox/Projects/TrelloScripts

import re

from trello import Board, Card, List

import Scripts.manual.youtube_playlist_to_card_checklist as YP
import utils

a, b, c = utils._init("manual")

_BOARD = "mine"
_LIST = "8"
_CARD = "grian"


def _set(all_boards: list[Board], board_name: str, list_name: str, card_name: str) -> None:
	board: Board = YP._create_find_in(board_name)(all_boards)
	lst: List = YP._create_find_in(list_name)(board.all_lists())
	card: Card = YP._create_find_in(card_name)(lst.list_cards())

	total_minutes = 0
	for checklist in card.checklists:
		for item in checklist.items:
			if res := re.search("\\((\\d+)min\\)", item["name"]):
				total_minutes += int(res.groups()[0])

	rounded_hours = round(total_minutes / 60 * 2) / 2
	if rounded_hours == int(rounded_hours):
		hours_str = f"{int(rounded_hours)}h"
	else:
		hours_str = f"{rounded_hours:.1f}h"

	print(f"Setting: {card.name} ({hours_str})")
	card.set_name(f"{card.name} ({hours_str})")


_set(c, "mine", "8", "tango")
