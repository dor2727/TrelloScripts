
import requests

from TrelloScripts.log import log
from TrelloScripts.utils import get_item



class CardUpdater(object):
	def __init__(self, card):
		self.card  = card

	def get_name(self):
		for att in self.card.attachments:
			if "url" in att:
				att["url"]
				raise NotImplemented
				# TODO:
				# if url is reddit: get post title
				# if url is youtube: get video title

		return None

	def set_card_name(self):
		new_name = self.get_name()
		if new_name:
			self.card.set_name(new_name)
		else:
			log(f"....[*] Unable to find new title. aborting. card : {self.card.name}"))

	def update_card(self):
		if self.card.name == "null":
			log(f"..[*] Fixing title : {self.card.name}")

			self.set_card_name()
