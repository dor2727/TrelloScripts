#!/usr/bin/env python3

from TrelloScripts.consts                import *
from TrelloScripts.log                   import log, log_initialize
from TrelloScripts.utils                 import *
from TrelloScripts.Classes.FriendUpdater import CardUpdater

set_verbose(4)



def main():
	log_initialize()

	client = get_client()


	log("[*] Getting friends board")
	all_boards = client.list_boards()
	friends_board = get_item(all_boards, "Friends")


	log("[*] Iterating cards")
	for card in friends_board.all_cards():
		c = CardUpdater(card, friends_board)
		c.update_card()
	log("[*] Done")


if __name__ == '__main__':
	main()