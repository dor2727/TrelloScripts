#!/usr/bin/env python3
import sys

from trello import Board, Card
from TrelloScripts.utils import BoardsFilter, get_cover_url, iterate_cards, log


def main() -> None:
	# set_verbose(9)  # verbose=10 shows "skipping archived card"

	iterate_cards(
		log_name="card_fix",
		apply_to_card=[set_card_cover],
		boards_filter=_get_boards_filter(),
	)


def _get_boards_filter() -> BoardsFilter:
	boards_filter: BoardsFilter
	if len(sys.argv) == 1:
		boards_filter = ["cooking", "youtube", "games", "courses", "dr k", "books", "podcasts"]
	else:

		def boards_filter(b: Board) -> bool:
			return any(b.name in requested_board for requested_board in sys.argv[1:])

	return boards_filter


def _print_card(card: Card) -> None:
	log(f'....[*] found card in board "{card.board.name}" : in list "{card.get_list().name}" : "{card.name}"')


def set_card_cover(card: Card) -> None:
	if not _is_cover_set(card):
		if cover_url := _get_card_cover_url(card):
			log(f'....[*] Setting cover : {card.name} : "{cover_url}"')
			card.attach(url=cover_url, setCover=True)
		else:
			log("..........[*] No cover url found. Skipping.")


def _is_cover_set(card: Card) -> bool:
	return any(att["previews"] for att in card.attachments)


def _get_card_cover_url(card: Card) -> str | None:
	for attachment in card.attachments:
		if "url" in attachment and (cover_url := get_cover_url(attachment["url"])):
			return cover_url

	return None


if __name__ == "__main__":
	main()
