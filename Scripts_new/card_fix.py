#!/usr/bin/env python3
import sys

from TrelloScripts.utils import log, iterate_cards, get_first_attachment, read_link

from trello import Card, Label


def main():
	if len(sys.argv) == 1:
		boards_filter = None  # all boards
	else:
		boards_filter = lambda b: any(b.name in requested_board for requested_board in sys.argv[1:])
		print(f"Usage: {sys.argv[0]} board_name [board_name ...]")
		sys.exit(1)

	boards = sys.argv[1:]

	iterate_cards(
		log_name="card_fix",
		apply_to_card=[move_description_url_to_attachment, move_title_url_to_attachment, fix_null_title, strip_title],
		boards_filter=boards_filter,
	)


def _print_card(card):
	log(f"....[*] found card in board \"{card.board.name}\" : in list \"{card.get_list().name}\" : \"{card.name}\"")

def move_description_url_to_attachment(card: Card):
	if card.description and is_url(card.description):
		_print_card(card)
		log(f"......[*] setting attachment to card: {card.description}")
		card.attach(url=card.description)
		card.set_description('')

def move_title_url_to_attachment(card: Card):
	if is_url(card.name):
		_print_card(card)
		log(f"......[*] setting attachment to card: {card.name}")
		card.attach(url=card.name)
		card.set_name("null")

def fix_null_title(card: Card):
	if card.name == "null":
		_print_card(card)

		if len(card.attachments) == 0:
			log(f"......[*] No attachments. Skipping.")
			return

		if len(card.attachments) > 1:
			log(f"......[w] More than 1 attachment! Using the first one.")

		attachment = get_first_attachment(self.card)
		if "url" in attachment:
			new_title = read_link(attachment["url"])
			card.set_name(new_title)
		else:
			log(f".....[*] Unable to find new title. aborting. card : {self.card.name}")

STRIPS = {
	" - YouTube": "YouTube",
	" Recipe: How to Make It": "Taste of home",
	" | מתכונים ב10 דקות": "10dakot",
	" | Kenji's Cooking Show": "Kenji's Cooking Show",
}
def strip_title(card: Card, board_labels: list[Label]):
	name = card.name

	for suffix, label_name in STRIPS.items():
		if name.endswith(suffix):
			# add the label to the card
			label = get_item(board_labels, label_name, case_sensitive=False)
			if label is not None and label not in card.labels:
				card.add_label(label)

			# strip the card name
			name = name[:-len(suffix)]

	if name != card.name:
		log(f"....[*] Fixing title : {card.name} -> {name}")
		card.set_name(name)
strip_title.requires_labels = True


if __name__ == '__main__':
	main()
