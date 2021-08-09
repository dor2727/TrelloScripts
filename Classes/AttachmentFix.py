
import urllib

from TrelloScripts.log import log
from TrelloScripts.utils import get_item




def is_url(url):
	if '\n' in url:
		return False
	scheme = urllib.parse.urlparse(url).scheme
	return scheme in ["https", "http"]


class CardUpdater(object):
	def __init__(self, card):
		self.card  = card

	def _fix_card(self):
		log(f"..[*] found {self.card.board.name} : {self.card.name}")

		log(f"....[*] setting attachment to card: {self.card.description}")
		card.attach(url=self.card.description)
		card.set_description('')


	def update_card(self):
		if self.card.description:
			if is_url(self.card.description):
				self._fix_card()
