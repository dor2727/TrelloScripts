#!/usr/bin/env python3

from TrelloScripts.utils.consts import *
from TrelloScripts.utils.log    import log, initialize_logfile
from TrelloScripts.utils.utils  import *
from TrelloScripts.Classes		import FriendCardUpdater

set_verbose(4)




@initialize_logfile("friends_updater.log")
def main():
	all_boards = get_all_boards()
	friends_board = get_item(all_boards, "Friends")

	log("[*] Iterating cards")
	for card in friends_board.all_cards():
		c = FriendCardUpdater(card, friends_board)
		c.update_card()

	log("[*] Done")


if __name__ == '__main__':
	main()
