from ..utils.log import log
from ..utils.utils import get_item, read_link

Url = Label = str
SITES: dict[Url, Label] = {
	"quantamagazine.org": "quanta",
	"bakadesuyo.com": "Barking up the wrong tree",
	# youtube
	# wikipedia
	# arxiv
}

class CardUpdater(object):
	def __init__(self, card, all_labels):
		self.card = card
		self.all_labels = all_labels

"""
TODO:
- detect utl from card.attachments
- if url is detected
	- if label doesn't exist - create it
	- if label isn't attached to the card - attach it


board.add_label?
Signature: all_boards[0].add_label(name, color)
Docstring:
Add a label to this board

:name: name of the label
:color: the color, either green, yellow, orange
        red, purple, blue, sky, lime, pink, or black
:return: the label
:rtype: Label
File:      ~/.local/lib/python3.11/site-packages/trello/board.py
Type:      method

"""