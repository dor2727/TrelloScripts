
import datetime

from TrelloScripts.log import log
from TrelloScripts.utils import get_item


LABELS = [
	"Last week",
	"More than a week",
	"More than 2 weeks",
	"More than a month",
	"More than 2 months",
	"More than 6 months",
	"too much",
]

LABEL_WEEK     = "Last week"
LABEL_2_WEEKS  = "More than a week"
LABEL_MONTH    = "More than 2 weeks"
LABEL_2_MONTHS = "More than a month"
LABEL_6_MONTHS = "More than 2 months"
LABEL_YEAR     = "More than 6 months"
LABEL_TOO_MUCH = "too much"



class CardUpdater(object):
	def __init__(self, card, friends_board):
		self.card  = card
		self.board = friends_board
		
		self._set_labels()

		# define now only once
		self.now = datetime.datetime.now()

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


	def get_all_dates(self):
		# the description is multi-lined,
		# each line is a date: yyyy/mm/dd
		return [
			datetime.datetime.strptime(i, "%Y/%m/%d")
			for i in self.card.description.splitlines()
		]

	def remove_date_labels(self):
		log("......[*] Removing date labels")
		for label in self.date_labels:
			self.card.remove_label(label)

	def add_date_label(self, all_dates):
		date = max(all_dates)
		delta = (self.now - date).days
		log(f"......[*] Last met {delta:3d} days ago")

		if delta <= 7:
			log(f"....[*] Adding label : {LABEL_WEEK}")
			self.card.add_label(self.label_week)
		elif delta <= 14:
			log(f"....[*] Adding label : {LABEL_2_WEEKS}")
			self.card.add_label(self.label_2_weeks)
		elif delta <= 30:
			log(f"....[*] Adding label : {LABEL_MONTH}")
			self.card.add_label(self.label_month)
		elif delta <= 30*2:
			log(f"....[*] Adding label : {LABEL_2_MONTHS}")
			self.card.add_label(self.label_2_months)
		elif delta <= 30*6:
			log(f"....[*] Adding label : {LABEL_6_MONTHS}")
			self.card.add_label(self.label_6_months)
		elif delta <= 365:
			log(f"....[*] Adding label : {LABEL_YEAR}")
			self.card.add_label(self.label_year)
		else:
			log(f"....[*] Adding label : {LABEL_TOO_MUCH}")
			self.card.add_label(self.label_too_much)

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
			self.add_date_label(all_dates)

			# put the newest date on top
			self.reorder_dates(all_dates)
