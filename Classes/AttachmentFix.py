from ..utils.log import log
from ..utils.utils import get_item, is_url


class CardUpdater(object):
	def __init__(self, card):
		self.card  = card

	def _fix_card_description(self):
		log(f"....[*] found card in board \"{self.card.board.name}\" : in list \"{self.card.get_list().name}\" : \"{self.card.name}\"")

		log(f"......[*] setting attachment to card: {self.card.description}")
		self.card.attach(url=self.card.description)
		self.card.set_description('')


	def _fix_card_name(self):
		log(f"....[*] found card in board \"{self.card.board.name}\" : in list \"{self.card.get_list().name}\" : \"{self.card.name}\"")

		log(f"......[*] setting attachment to card: {self.card.name}")
		self.card.attach(url=self.card.name)
		self.card.set_name("null")


	def update_card(self):
		# move description to attachment
		if self.card.description:
			if is_url(self.card.description):
				self._fix_card_description()

		# move title to attachment
		if is_url(self.card.name):
			self._fix_card_name()
