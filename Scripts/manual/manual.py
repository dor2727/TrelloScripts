#!/usr/bin/env python3

from trello import Card, Label
from TrelloScripts.utils import (
	get_item,
	iterate_cards,
	log,
	requires_lables,
	set_verbose,
)


def main() -> None:
	set_verbose(100)

	iterate_cards(
		log_name="manual",
		apply_to_card=[add_pair_label],
		boards_filter=["Books - Need Research"],
	)


def _print_card(card: Card) -> None:
	log(f'....[*] found card in board "{card.board.name}" : in list "{card.get_list().name}" : "{card.name}"')


@requires_lables
def add_pair_label(card: Card, board_labels: list[Label]) -> None:
	label_structure = get_item(board_labels, "From Structure", case_sensitive=True)
	label_backlog = get_item(board_labels, "ToBacklog", case_sensitive=True)

	if (label_structure is not None) and (label_structure in card.labels) and (label_backlog not in card.labels):
		_print_card(card)
		card.add_label(label_backlog)


if __name__ == "__main__":
	main()
