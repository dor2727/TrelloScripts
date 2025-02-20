#!/usr/bin/env python3
import os

from trello import Card
from TrelloScripts.utils import get_boards_filter, get_cover_url, iterate_cards, log, set_verbose


def main() -> None:
	set_verbose(8)  # 4 shows card, 6 shows new cover, 8 shows "skipping no cover cards", 10 shows "skipping archived card"

	iterate_cards(
		log_name=os.path.splitext(os.path.basename(__file__))[0],
		apply_to_card=[set_card_cover],
		boards_filter=get_boards_filter(default=["cooking", "youtube", "courses", "dr k", "books", "podcasts", "chen"]),
	)


def _print_card(card: Card) -> None:
	log(f'....[*] found card in board "{card.board.name}" : in list "{card.get_list().name}" : "{card.name}"')


def set_card_cover(card: Card) -> None:
	if not _is_cover_set(card):
		if cover_url := _get_card_cover_url(card):
			log(f'......[*] Setting cover : {card.name} : "{cover_url}"')
			try:
				card.attach(url=cover_url, setCover=True)
			except Exception:
				log("........[X] Failed setting cover. Maybe the video is unavailable?")
		else:
			if card.attachments:
				log("........[*] No cover url found. Skipping.")


def _is_cover_set(card: Card) -> bool:
	return any(att["previews"] for att in card.attachments)


def _get_card_cover_url(card: Card) -> str | None:
	for attachment in card.attachments:
		if "url" in attachment and (cover_url := get_cover_url(attachment["url"])):
			return cover_url

	return None


if __name__ == "__main__":
	main()
