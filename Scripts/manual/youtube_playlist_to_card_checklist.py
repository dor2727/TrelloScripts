#!/usr/bin/env python3

import os
import re
import sys
from typing import Callable, Literal

from trello import Board, Card, List
from TrelloScripts.utils import (
	_init,
	log,
	set_verbose,
)

sys.path.append(os.path.expanduser("~/Dropbox/Projects/Scripts/scraping_to_trello_checklist"))
from youtube_playlist_to_trello_checklist import main as get_items_from_playlist


def main(
	pick_board: Callable[[list[Board]], Board],
	pick_list: Callable[[list[List]], List] | None,
	pick_card: Callable[[list[Card]], Card] | Literal[True],
	playlist_url: str | None,
	format_video_print: Callable[[str, int, str, str], str],
	checklist_name: str = "Checklist",
	item_state: list[bool] | None = None,
	item_slice: range | None = None,
	add_duration_to_card_name: bool = False,
	exclude_cards: list[str] | None = None,
) -> None:
	set_verbose(100)

	_, _, all_boards = _init("youtube_playlist_to_card_checklist")
	board = pick_board(all_boards)
	log(f'....[*] found board "{board.name}"')

	if pick_list is None:
		all_cards = board.all_cards()
	else:
		lst = pick_list(board.all_lists())
		all_cards = lst.list_cards()
		log(f'....[*] found list "{lst.name}"')

	if pick_card is True and pick_list is not None:
		cards = all_cards
		if exclude_cards is not None:
			# fmt:off
			cards = [
				card
				for card in cards
				if not any(
					excluded in card.name.lower()
					for excluded in exclude_cards
				)
			]
			# fmt:on
	else:
		cards = [pick_card(all_cards)]  # type:ignore

	for card in cards:
		log(f'....[*] found card "{card.name}" : in list "{card.get_list().name}"')
		_handle_card(card, playlist_url, format_video_print, checklist_name, item_state, item_slice, add_duration_to_card_name)


def _handle_card(
	card: Card,
	playlist_url: str | None,
	format_video_print: Callable[[str, int, str, str], str],
	checklist_name: str = "Checklist",
	item_state: list[bool] | None = None,
	item_slice: range | None = None,
	add_duration_to_card_name: bool = False,
) -> None:
	if playlist_url is None:
		try:
			playlist_url = card.attachments[0]["url"]
		except (IndexError, KeyError):
			log("No playlist URL provided and no attachments found in card.")
			return

	items = get_items_from_playlist(playlist_url, format_video_print)
	log(f"....[*] found {len(items)} items")

	if item_state is None:
		pass  # all good
	elif item_state is True:
		item_state = [True] * len(items)
	elif isinstance(item_state, range):
		item_state = [i in item_state for i in range(len(items))]
	elif isinstance(item_state, list):
		item_state = list(item_state) + [False] * (len(items) - len(item_state))

	if isinstance(item_slice, range):
		items = items[item_slice.start : item_slice.stop]
		if item_state is not None:
			item_state = item_state[item_slice.start : item_slice.stop]

	checklist = card.add_checklist(checklist_name, items, item_state)
	log(f"..[*] added {len(checklist.items)} items")

	if add_duration_to_card_name:
		if re.search("\\(\\d+(\\.5)h\\)", card.name):
			log("Card name already contains duration, skipping")
		else:
			minutes = [re.search("\\((\\d+)min\\)", item) for item in items]
			total_minutes = sum([int(m.group(1)) for m in minutes])  # type:ignore
			rounded_hours = round(total_minutes / 60 * 2) / 2
			if rounded_hours == int(rounded_hours):
				hours_str = f"{int(rounded_hours)}h"
			else:
				hours_str = f"{rounded_hours:.1f}h"
			card.set_name(f"{card.name} ({hours_str})")


def _create_find_in(s: str) -> Callable[[list], object]:
	def find_in(l: list) -> object:  # noqa: E741
		return next(filter(lambda x: s in x.name.lower(), l))

	return find_in


generic_format_video_print = lambda v_id, v_seconds, v_title, v_url: f"{int(v_id):02d}: ({v_seconds // 60}min): {v_url}"

if __name__ == "__main__":
	### Etho
	## Etho HC-7
	# main(
	# 	# pick_board=lambda boards: next(filter(lambda b: "youtube - minecraft" in b.name.lower(), boards)),
	# 	pick_board=_create_find_in("youtube - minecraft"),
	# 	pick_list=None,
	# 	pick_card=_create_find_in("ethoslab - season 7"),
	# 	playlist_url="https://www.youtube.com/playlist?list=PLaAVDbMg_XAoTkSw42KSc-pl7rG9Hr95v",
	# 	format_video_print=generic_format_video_print,
	# 	checklist_name="Checklist",
	# )
	## Etho HC-5
	# main(
	# 	pick_board=_create_find_in("youtube - minecraft"),
	# 	pick_list=None,
	# 	pick_card=_create_find_in("ethoslab - season 5"),
	# 	playlist_url=None,
	# 	format_video_print=generic_format_video_print,
	# 	checklist_name="Checklist",
	# 	item_state=True,
	# )
	## Etho HC-4
	# main(
	# 	pick_board=_create_find_in("youtube - minecraft"),
	# 	pick_list=None,
	# 	pick_card=_create_find_in("ethoslab - season 4"),
	# 	playlist_url=None,
	# 	format_video_print=generic_format_video_print,
	# 	checklist_name="Checklist",
	# 	item_state=True,
	# )
	## Etho HC-3
	# main(
	# 	pick_board=_create_find_in("youtube - minecraft"),
	# 	pick_list=None,
	# 	pick_card=_create_find_in("ethoslab - season 3"),
	# 	playlist_url=None,
	# 	format_video_print=generic_format_video_print,
	# 	checklist_name="Checklist",
	# 	item_state=True,
	# )
	# Etho old
	# for card_name in ["mindcrack season 1", "mindcrack season 2", "modded minecraft 1", "modded minecraft 2"]:
	# 	main(
	# 		pick_board=_create_find_in("youtube - minecraft"),
	# 		pick_list=_create_find_in("old etho"),
	# 		pick_card=_create_find_in(card_name),
	# 		playlist_url=None,
	# 		format_video_print=generic_format_video_print,
	# 		checklist_name="Checklist",
	# 		item_state=range(10) if card_name == "mindcrack season 1" else None,
	# 	)

	### HC-10
	## Etho HC-10
	# main(
	# 	pick_board=_create_find_in("youtube - minecraft"),
	# 	pick_list=_create_find_in("10"),
	# 	pick_card=_create_find_in("ethoslab"),
	# 	playlist_url=None,
	# 	format_video_print=lambda v_id, v_seconds, v_title, v_url: f"S10E{int(v_id):02d}: ({v_seconds // 60}min): {v_url}",
	# 	checklist_name="Checklist",
	# 	item_state=True,
	# )
	# Joel HC-10
	# main(
	# 	pick_board=_create_find_in("youtube - minecraft"),
	# 	pick_list=_create_find_in("10"),
	# 	pick_card=_create_find_in("joel smallishbeans"),
	# 	playlist_url=None,
	# 	format_video_print=lambda v_id, v_seconds, v_title, v_url: f"S10E{int(v_id):02d}: ({v_seconds // 60}min): {v_url}",
	# 	checklist_name="Checklist",
	# 	item_state=True,
	# )
	## Pearl HC-10
	# main(
	# 	pick_board=_create_find_in("youtube - minecraft"),
	# 	pick_list=_create_find_in("10"),
	# 	pick_card=_create_find_in("pearlescentmoon"),
	# 	playlist_url=None,
	# 	format_video_print=lambda v_id, v_seconds, v_title, v_url: f"S10E{int(v_id):02d}: ({v_seconds // 60}min): {v_url}",
	# 	checklist_name="Checklist",
	# 	item_state=None,
	# )

	### HC-9
	# for card_name in ["ethoslab", "pearlescentmoon", "geminitay"]:
	# 	main(
	# 		pick_board=_create_find_in("youtube - minecraft"),
	# 		pick_list=_create_find_in("9"),
	# 		pick_card=_create_find_in(card_name),
	# 		playlist_url=None,
	# 		format_video_print=lambda v_id, v_seconds, v_title, v_url: f"S09E{int(v_id):02d}: ({v_seconds // 60}min): {v_url}",
	# 		checklist_name="Checklist",
	# 		item_state=None,
	# 	)

	### HC-8
	# for card_name in ["ethoslab", "tango", "grain"]:
	# format_season_8 = lambda v_id, v_seconds, v_title, v_url: f"S08E{int(v_id):02d}: ({v_seconds // 60}min): {v_url}"
	# for card_name in ["grian"]:
	# 	main(
	# 		pick_board=_create_find_in("youtube - minecraft"),
	# 		pick_list=_create_find_in("8"),
	# 		pick_card=_create_find_in(card_name),
	# 		playlist_url=None,
	# 		format_video_print=format_season_8,
	# 		checklist_name="Checklist",
	# 		item_state=None,
	# 	)
	# main(
	# 	pick_board=_create_find_in("youtube - minecraft"),
	# 	pick_list=_create_find_in("8"),
	# 	pick_card=_create_find_in("pearl"),
	# 	playlist_url=None,
	# 	format_video_print=format_season_8,
	# 	checklist_name="Checklist",
	# 	item_state=range(13),
	# )
	# main(
	# 	pick_board=_create_find_in("youtube - minecraft"),
	# 	pick_list=_create_find_in("8"),
	# 	pick_card=_create_find_in("gemini"),
	# 	playlist_url=None,
	# 	format_video_print=format_season_8,
	# 	checklist_name="Checklist",
	# 	item_state=range(11),
	# )

	## Life series - wild life
	# main(
	# 	pick_board=_create_find_in("youtube - minecraft"),
	# 	pick_list=_create_find_in("wild life"),
	# 	pick_card=True,
	# 	playlist_url=None,
	# 	format_video_print=generic_format_video_print,
	# 	checklist_name="Checklist",
	# 	item_state=None,
	# )
	## Life series
	# added a patch to ignore "etho" cards"
	# for list_name in ["secret life", "limited life", "double life", "last life", "3rd life"]:
	# 	main(
	# 		pick_board=_create_find_in("youtube - minecraft"),
	# 		pick_list=_create_find_in(list_name),
	# 		pick_card=True,
	# 		playlist_url=None,
	# 		format_video_print=generic_format_video_print,
	# 		checklist_name="Checklist",
	# 		item_state=None,
	# 	)
	## Etho
	# main(
	# 	pick_board=_create_find_in("youtube - minecraft"),
	# 	pick_list=_create_find_in("secret life"),
	# 	pick_card=_create_find_in("etho"),
	# 	playlist_url=None,
	# 	format_video_print=generic_format_video_print,
	# 	checklist_name="Checklist",
	# 	item_state=None,
	# 	item_slice=range(29-1, 36),  # 29 to 36, inclusive, converted to zero-based
	# )
	# main(
	# 	pick_board=_create_find_in("youtube - minecraft"),
	# 	pick_list=_create_find_in("limited life"),
	# 	pick_card=_create_find_in("etho"),
	# 	playlist_url=None,
	# 	format_video_print=generic_format_video_print,
	# 	checklist_name="Checklist",
	# 	item_state=None,
	# 	item_slice=range(22-1, 28),  # 22 to 28, inclusive, converted to zero-based
	# )
	# main(
	# 	pick_board=_create_find_in("youtube - minecraft"),
	# 	pick_list=_create_find_in("double life"),
	# 	pick_card=_create_find_in("etho"),
	# 	playlist_url=None,
	# 	format_video_print=generic_format_video_print,
	# 	checklist_name="Checklist",
	# 	item_state=None,
	# 	item_slice=range(16-1, 21),  # 16 to 21, inclusive, converted to zero-based
	# )
	# main(
	# 	pick_board=_create_find_in("youtube - minecraft"),
	# 	pick_list=_create_find_in("last life"),
	# 	pick_card=_create_find_in("etho"),
	# 	playlist_url=None,
	# 	format_video_print=generic_format_video_print,
	# 	checklist_name="Checklist",
	# 	item_state=None,
	# 	item_slice=range(8-1, 18),  # 8 to 18, inclusive, converted to zero-based
	# )
	# main(
	# 	pick_board=_create_find_in("youtube - minecraft"),
	# 	pick_list=_create_find_in("3rd life"),
	# 	pick_card=_create_find_in("etho"),
	# 	playlist_url=None,
	# 	format_video_print=generic_format_video_print,
	# 	checklist_name="Checklist",
	# 	item_state=None,
	# 	item_slice=range(1-1, 7),  # 1 to 7, inclusive, converted to zero-based
	# )

	## empires
	# for list_name in ["empires 1", "empires 2"]:
	# 	main(
	# 		pick_board=_create_find_in("youtube - minecraft"),
	# 		pick_list=_create_find_in(list_name),
	# 		pick_card=_create_find_in("lizzie"),
	# 		playlist_url=None,
	# 		format_video_print=generic_format_video_print,
	# 		checklist_name="Checklist",
	# 		item_state=True,
	# 	)
	# 	main(
	# 		pick_board=_create_find_in("youtube - minecraft"),
	# 		pick_list=_create_find_in(list_name),
	# 		pick_card=_create_find_in("joel"),
	# 		playlist_url=None,
	# 		format_video_print=generic_format_video_print,
	# 		checklist_name="Checklist",
	# 		item_state=None,
	# 	)

	## More etho
	main(
		pick_board=_create_find_in("youtube - minecraft"),
		pick_list=_create_find_in("old etho"),
		pick_card=True,
		playlist_url=None,
		format_video_print=generic_format_video_print,
		checklist_name="Checklist",
		item_state=None,
		add_duration_to_card_name=True,
		exclude_cards=["mindcrack", "modded minecraft 1", "modded minecraft 2"],
	)
