from ..utils.log import log
from ..utils.utils import get_item

_YOUTUBE = " - YouTube"
_TASTE_OF_HOME = " Recipe: How to Make It"
_10_DAKOT = " | מתכונים ב10 דקות"
_KENJI = " | Kenji's Cooking Show"


class CardUpdater:
	def __init__(self, card, all_labels):
		self.card = card
		self.all_labels = all_labels

	def _strip_by_suffix(self, s, suffix, label_name=None):
		if s.endswith(suffix) and len(s) > len(suffix):
			# maybe add label
			if label_name is not None:
				label = get_item(self.all_labels, label_name, case_sensitive=False)
				if label is not None and label not in self.card.labels:
					self.card.add_label(label)

			return s[: -len(suffix)]

		return s

	def strip_youtube(self, s):
		return self._strip_by_suffix(s, _YOUTUBE, "YouTube")

	def strip_taste_of_home(self, s):
		return self._strip_by_suffix(s, _TASTE_OF_HOME, "Taste of home")

	def strip_10_dakot(self, s):
		return self._strip_by_suffix(s, _10_DAKOT, "10dakot")

	def strip_kenji(self, s):
		return self._strip_by_suffix(s, _KENJI, "Kenji's Cooking Show")

	def update_card(self):
		name = self.card.name

		for strip_func in (
			self.strip_youtube,
			self.strip_taste_of_home,
			self.strip_10_dakot,
			self.strip_kenji,
		):
			name = strip_func(name)

		if name != self.card.name:
			log(f"....[*] Fixing title : {self.card.name} -> {name}")
			self.card.set_name(name)
