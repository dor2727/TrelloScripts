#!/usr/bin/env python3

from TrelloScripts.utils.consts import *
from TrelloScripts.utils.log import initialize_logfile, log
from TrelloScripts.utils.utils import *

set_verbose(8)


def get_boards_by_name(all_boards, *names):
	return sum(([b for b in all_boards if name in b.name] for name in names), [])


from urllib.parse import urlparse


def get_domain(s: str) -> str:
	if not s:  # emtpy string
		return s
	return urlparse(s).netloc


@initialize_logfile("card_fix.log")
def main():
	all_boards = get_all_boards()
	boards = get_boards_by_name(all_boards, "Reading", "Games", "Blog Projects", "Collection", "Cooking", "Breath", "Yoga")

	log("[*] Adding labels per url : Iterating cards")
	for board in boards:
		all_board_attachements = reduce(set.union, {get_domain(attachment.get("url", "")) for card in board.all_cards() for attachment in card.attachments})

	log("[*] Done")


if __name__ == "__main__":
	main()
