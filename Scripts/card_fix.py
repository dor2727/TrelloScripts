#!/usr/bin/env python3

from TrelloScripts.consts                import *
from TrelloScripts.log                   import log, log_initialize, set_logfile
from TrelloScripts.utils                 import *
from TrelloScripts.Classes.TitleFix      import CardUpdater as TitleCardUpdater
from TrelloScripts.Classes.AttachmentFix import CardUpdater as AttachmentCardUpdater

set_verbose(10)


def main():
	set_logfile("card_fix.log")

	log_initialize()

	client = get_client()


	log("[*] Getting reading boards")
	all_boards = client.list_boards()
	boards = [b for b in all_boards if "Reading"    in b.name] \
		   + [b for b in all_boards if "Blog"       in b.name] \
		   + [b for b in all_boards if "Collection" in b.name] \
		   + [b for b in all_boards if "Cooking"    in b.name]


	log("[*] Fixing Description/Title to Attachment : Iterating cards")
	for board in boards:
		for card in board.all_cards():
			c = AttachmentCardUpdater(card)
			c.update_card()

	log("[*] Fixing Title : Iterating cards")
	for board in boards:
		for card in board.all_cards():
			c = TitleCardUpdater(card)
			c.update_card()

	log("[*] Done")


if __name__ == '__main__':
	main()