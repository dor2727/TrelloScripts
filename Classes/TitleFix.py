
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from TrelloScripts.log import log
from TrelloScripts.utils import get_item


def get_domain(url):
	return urlparse(url).netloc


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
}


def get_bs(url):
	req = requests.get(url, headers=headers)
	if not req.ok:
		log(f".....[!] Failed getting URL: {url}")
		return None

	bs = BeautifulSoup(req.content, features="lxml")
	return bs

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
			url = attachment["url"]
			domain = get_domain(url)

			if domain == "www.reddit.com":
				return self._get_name_reddit(url)
			elif domain in ("www.youtube.com", "youtu.be"):
				return self._get_name_youtube(url)
			else:
				log(f".....[w] Unrecognized domain. Skipping.")

		return None


	def _get_name_reddit(self, url):
		bs = get_bs(url)

		# in case the request failed.
		if bs is None:
			return None

		# from my manual test, bs.find_all("h1") brings two identical results.
		post_name = bs.find("h1").text

		return post_name

	def _get_name_youtube(self, url):
		bs = get_bs(url)

		# in case the request failed.
		if bs is None:
			return None

		# it should return "<video name> - YouTube"
		web_page_title = bs.find("title").text

		return web_page_title

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
