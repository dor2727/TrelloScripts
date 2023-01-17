#!/usr/bin/env python3

from TrelloScripts.consts                import *
from TrelloScripts.log                   import log, log_initialize, set_logfile
from TrelloScripts.utils                 import *
from TrelloScripts.Classes.TitleFix      import CardUpdater as TitleCardUpdater
from TrelloScripts.Classes.TitleStrip    import CardUpdater as TitleStripCardUpdater
from TrelloScripts.Classes.AttachmentFix import CardUpdater as AttachmentCardUpdater
from TrelloScripts.Classes.CoverSet      import CardUpdater as CoverSetCardUpdater

set_verbose(10)


def main():
	set_logfile("card_fix.log")
	log_initialize()

	all_boards = get_all_boards()
	boards = [b for b in all_boards if "Reading"    in b.name] \
		   + [b for b in all_boards if "Games"      in b.name] \
		   + [b for b in all_boards if "Blog"       in b.name] \
		   + [b for b in all_boards if "Collection" in b.name] \
		   + [b for b in all_boards if "Cooking"    in b.name]
	boards_cover = [get_item(all_boards, "Cooking")]

	log("[*] Fixing Description/Title to Attachment : Iterating cards")
	for board in boards:
		log(f"..[*] Iterating {board.name}")
		for card in board.all_cards():
			c = AttachmentCardUpdater(card)
			c.update_card()

	log("[*] Fixing Title : Iterating cards")
	for board in boards:
		log(f"..[*] Iterating {board.name}")
		for card in board.all_cards():
			c = TitleCardUpdater(card)
			c.update_card()

	log("[*] Fixing Title Strip : Iterating cards")
	for board in boards:
		log(f"..[*] Iterating {board.name}")
		all_labels = board.get_labels()
		for card in board.all_cards():
			c = TitleStripCardUpdater(card, all_labels)
			c.update_card()

	log("[*] Adding covers : Iterating cards")
	for board in boards_cover:
		log(f"..[*] Iterating {board.name}")
		for card in board.all_cards():
			c = CoverSetCardUpdater(card)
			c.update_card()

	log("[*] Done")


if __name__ == '__main__':
	main()