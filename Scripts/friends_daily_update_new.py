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


LABELS = [
	"last week",
	"last 14 days",
	"last month",
	"last 2 months",
	"last 6 months",
	"last year",
	"too much",
]

LABEL_WEEK     = "last week"
LABEL_2_WEEKS  = "last 14 days"
LABEL_MONTH    = "last month"
LABEL_2_MONTHS = "last 2 months"
LABEL_6_MONTHS = "last 6 months"
LABEL_YEAR     = "last year"
LABEL_TOO_MUCH = "too much"



class CardUpdater(object):
	def __init__(self, card, friends_board):
		self.card  = card
		self.board = friends_board
		
		self._set_labels()

	def _set_labels(self):
		# get the labels
		log("......[*] Getting labels")
		self._all_labels = self.board.get_labels()

		# the labels are
		# week, 14, month, 2 month, 6 month, year, too much
		self.label_week     = get_item(self._all_labels, LABEL_WEEK)
		self.label_2_weeks  = get_item(self._all_labels, LABEL_2_WEEKS)
		self.label_month    = get_item(self._all_labels, LABEL_MONTH)
		self.label_2_months = get_item(self._all_labels, LABEL_2_MONTHS)
		self.label_6_months = get_item(self._all_labels, LABEL_6_MONTHS)
		self.label_year     = get_item(self._all_labels, LABEL_YEAR)
		self.label_too_much = get_item(self._all_labels, LABEL_TOO_MUCH)

		self.date_labels = [
			self.label_week,
			self.label_2_weeks,
			self.label_month,
			self.label_2_months,
			self.label_6_months,
			self.label_year,
			self.label_too_much,
		]


	def remove_date_labels(self):
		log("......[*] Removing labels")
		for label in self.date_labels:
			self.card.remove_label(label)

	def add_date_label(self, delta):
		if delta <= 7:
			log(f"....[*] Adding label : last week"    )
			self.card.add_label(self.label_week)
		elif delta <= 14:
			log(f"....[*] Adding label : last 14 days" )
			self.card.add_label(self.label_2_weeks)
		elif delta <= 30:
			log(f"....[*] Adding label : last month"   )
			self.card.add_label(self.label_month)
		elif delta <= 30*2:
			log(f"....[*] Adding label : last 2 months")
			self.card.add_label(self.label_2_months)
		elif delta <= 30*6:
			log(f"....[*] Adding label : last 6 months")
			self.card.add_label(self.label_6_months)
		elif delta <= 365:
			log(f"....[*] Adding label : last year"    )
			self.card.add_label(self.label_year)
		else:
			log(f"....[*] Adding label : too much"     )
			self.card.add_label(self.label_too_much)

	def get_all_dates(self):
		# the description is multi-lined,
		# each line is a date: yyyy/mm/dd
		return [
			datetime.datetime.strptime(i, "%Y/%m/%d")
			for i in self.card.description.splitlines()
		]

	def reorder_dates(self, all_dates=None):
		all_dates = all_dates or self.get_all_dates()
		self.card.set_description(
			'\n'.join( [
				i.strftime("%Y/%m/%d")
				for i in sorted(all_dates, reverse=True)
			] )
		)

	def update_card(self):
		log(f"..[*] Updating : {self.card.name}")
		
		all_dates = self.get_all_dates()

		if all_dates:
			# first, remove all labels
			self.remove_date_labels()

			# then, calculate which label to add
			date = max(all_dates)
			delta = (NOW - date).days
			log(f"......[*] Last met {delta:3d} days ago")

			self.add_date_label(delta)

			# put the newest date on top
			self.reorder_dates(all_dates)


def main():
	log_initialize()

	client = get_client()


	log("[*] Getting friends board")
	all_boards = client.list_boards()
	friends_board = get_item(all_boards, "Friends - After degree")


	log("[*] Iterating cards")
	for card in friends_board.all_cards():
		c = CardUpdater(card, friends_board)
		c.update_card()
	log("[*] Done")


if __name__ == '__main__':
	main()