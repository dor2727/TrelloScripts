#!/usr/bin/env python3

import os
import sys

# this file is in Trello/Scripts/file.py
sys.path = [os.path.dirname(os.path.dirname(__file__))] + sys.path
print(sys.path)
from trello_utils import *

set_verbose(4)

# define now only once
NOW = datetime.datetime.now()


class CardUpdater(object):
	def __init__(self, friends_board):
		self.board = friends_board
		
		self._set_labels()

	def _set_labels(self):
		# get the labels
		log("......[*] Getting labels")
		self.date_labels = self.board.get_labels()

		# the labels are
		# week, 14, month, 2 month, 6 month, year, too much
		self.label_week     = get_item(self.date_labels, "last week")
		self.label_2_weeks  = get_item(self.date_labels, "last 14 days")
		self.label_month    = get_item(self.date_labels, "last month")
		self.label_2_months = get_item(self.date_labels, "last 2 months")
		self.label_6_months = get_item(self.date_labels, "last 6 months")
		self.label_year     = get_item(self.date_labels, "last year")
		self.label_too_much = get_item(self.date_labels, "too much")


	def remove_date_labels(self, card):
		log("......[*] Removing labels")
		for label in self.date_labels:
			card.remove_label(label)

	def add_date_label(self, card, delta):
		if delta <= 7:
			log(f"....[*] Adding label : last week"    )
			card.add_label(self.label_week)
		elif delta <= 14:
			log(f"....[*] Adding label : last 14 days" )
			card.add_label(self.label_2_weeks)
		elif delta <= 30:
			log(f"....[*] Adding label : last month"   )
			card.add_label(self.label_month)
		elif delta <= 30*2:
			log(f"....[*] Adding label : last 2 months")
			card.add_label(self.label_2_months)
		elif delta <= 30*6:
			log(f"....[*] Adding label : last 6 months")
			card.add_label(self.label_6_months)
		elif delta <= 365:
			log(f"....[*] Adding label : last year"    )
			card.add_label(self.label_year)
		else:
			log(f"....[*] Adding label : too much"     )
			card.add_label(self.label_too_much)

	def update_card(self, card):
		log(f"..[*] Updating : {card.name}")
		# the description is multi-lined,
		# each line is a date: yyyy/mm/dd
		all_dates = [
			datetime.datetime.strptime(i, "%Y/%m/%d")
			for i in card.description.splitlines()
		]

		# first, remove all labels
		self.remove_date_labels(card)

		# then, calculate which label to add
		if all_dates:
			date = max(all_dates)
			delta = (NOW - date).days
			log(f"......[*] Last met {delta:3d} days ago")

			self.add_date_label(card, delta)

	def update_all_cards(self):
		log("[*] Iterating cards")
		for card in self.board.all_cards():
			self.update_card(card)
		log("[*] Done")


def main():
	log_initialize()

	client = get_client()

	log("[*] Getting friends board")
	all_boards = client.list_boards()
	friends_board = get_item(all_boards, "Friends - After degree")


	c = CardUpdater(friends_board)
	c.update_all_cards()

if __name__ == '__main__':
	main()