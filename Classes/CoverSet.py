from ..utils.log import log
from ..utils.utils import get_item, read_link
from ..utils.utils_web import get_cover_url

class CardUpdater(object):
	def __init__(self, card):
		self.card = card

	def get_cover_url(self):
		for attachment in self.card.attachments:
			if "url" in attachment:
				if cover_url := get_cover_url(attachment["url"]):
					return cover_url

		log(f".....[*] No cover url found. Skipping.")
		return None

	def set_card_cover(self):
		if cover_url := self.get_cover_url():
			log(f"..[*] Setting cover : {self.card.name} : \"{cover_url}\"")
			self.card.attach(url=cover_url, setCover=True)

	def is_cover_set(self):
		return any(att["previews"] for att in self.card.attachments)

	def update_card(self):
		if not self.is_cover_set():
			self.set_card_cover()
