#!/usr/bin/env python3

from TrelloScripts.consts                import *
from TrelloScripts.log                   import log, initialize_logfile
from TrelloScripts.utils                 import *
from TrelloScripts.Classes.TitleFix      import CardUpdater as TitleCardUpdater
from TrelloScripts.Classes.TitleStrip    import CardUpdater as TitleStripCardUpdater
from TrelloScripts.Classes.AttachmentFix import CardUpdater as AttachmentCardUpdater
from TrelloScripts.Classes.CoverSet      import CardUpdater as CoverSetCardUpdater

set_verbose(10)


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

@initialize_logfile("card_fix.log")
def main():
	all_boards = get_all_boards()
	boards = [b for b in all_boards if "Reading"    in b.name] \
		   + [b for b in all_boards if "Games"      in b.name] \
		   + [b for b in all_boards if "Blog"       in b.name] \
		   + [b for b in all_boards if "Collection" in b.name] \
		   + [b for b in all_boards if "Cooking"    in b.name]
	boards_cover = [get_item(all_boards, "Cooking")]

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