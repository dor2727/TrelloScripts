from TrelloScripts.log import log
from TrelloScripts.utils import get_item, read_link


class CardUpdater(object):
	def __init__(self, card):
		self.card  = card

	def get_name(self):
		if len(self.card.attachments) == 0:
			log(f".....[*] No attachments. Skipping.")
			return None

		if len(self.card.attachments) > 1:
			log(f".....[w] More than 1 attachment! Using the first one.")


		attachment = self.card.attachments[0]
		if "url" in attachment:
			return read_link(attachment["url"])

		return None


	def set_card_name(self):
		new_name = self.get_name()
		if new_name:
			self.card.set_name(new_name)
		else:
			log(f"....[*] Unable to find new title. aborting. card : {self.card.name}")

	def update_card(self):
		if self.card.name == "null":
			log(f"..[*] Fixing title : {self.card.name}")

			self.set_card_name()
