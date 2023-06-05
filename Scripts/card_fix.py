#!/usr/bin/env python3

from TrelloScripts.utils.consts          import *
from TrelloScripts.utils.log             import log, initialize_logfile
from TrelloScripts.utils.utils           import *
from TrelloScripts.Classes import	TitleCardUpdater     , \
									TitleStripCardUpdater, \
									AttachmentCardUpdater, \
									CoverSetCardUpdater

set_verbose(8)


def iterate_boards(cls, boards, requires_all_labels = False):
	for board in boards:
		log(f"..[*] Iterating {board.name}")

		if requires_all_labels:
			all_labels = board.get_labels()
			args = (all_labels,)
		else:
			args = ()

		for card in board.all_cards():
			c = cls(card, *args)
			c.update_card()

def get_boards_by_name(all_boards, *names):
	return sum(
		(
			[b for b in all_boards if name in b.name]
			for name in names
		),
		[]
	)

@initialize_logfile("card_fix.log")
def main():
	all_boards = get_all_boards()
	boards = get_boards_by_name(all_boards, "Reading", "Games", "Blog Projects", "Collection", "Cooking", "Breath", "Yoga")
	boards_cover = get_boards_by_name(all_boards, "Cooking")

	log("[*] Fixing Description/Title to Attachment : Iterating cards")
	iterate_boards(AttachmentCardUpdater, boards)

	log("[*] Fixing Title : Iterating cards")
	iterate_boards(TitleCardUpdater, boards)

	log("[*] Fixing Title Strip : Iterating cards")
	iterate_boards(TitleStripCardUpdater, boards, True)

	log("[*] Adding covers : Iterating cards")
	iterate_boards(CoverSetCardUpdater, boards_cover)

	log("[*] Done")


if __name__ == '__main__':
	main()