#!/usr/bin/env python3
import os
from datetime import datetime
from typing import Iterable

from trello import Card, Label
from TrelloScripts.utils import get_item, iterate_cards, log, requires_lables


def main() -> None:
	iterate_cards(
		log_name=os.path.splitext(os.path.basename(__file__))[0],
		apply_to_card=[print_card, remove_date_labels, add_date_label, reorder_dates],
		boards_filter=lambda b: b.name == "Friends",
	)


LABELS = {
	"week": "Last week",
	"2_weeks": "More than a week",
	"month": "More than 2 weeks",
	"2_months": "More than a month",
	"6_months": "More than 2 months",
	"year": "More than 6 months",
	"too_much": "too much",
}


def print_card(card: Card) -> None:
	log(f"....[*] Updating : {card.name}")


@requires_lables
def remove_date_labels(card: Card, board_labels: list[Label]) -> None:
	for label_name in LABELS.values():
		label = get_item(board_labels, label_name)
		if label in card.labels:
			card.remove_label(label)


@requires_lables
def add_date_label(card: Card, board_labels: list[Label]) -> None:
	try:
		last_seen_date = max(_get_all_dates(card))
	except ValueError:  # max() arg is an empty sequence
		return

	delta = (datetime.now() - last_seen_date).days
	log(f"........[*] Last met {delta:3d} days ago")

	if delta <= 7:
		label_name = LABELS["week"]
	elif delta <= 14:
		label_name = LABELS["2_weeks"]
	elif delta <= 30:
		label_name = LABELS["month"]
	elif delta <= 30 * 2:
		label_name = LABELS["2_months"]
	elif delta <= 30 * 6:
		label_name = LABELS["6_months"]
	elif delta <= 365:
		label_name = LABELS["year"]
	else:
		label_name = LABELS["too_much"]

	log(f"......[*] Adding label : {label_name}")
	card.add_label(get_item(board_labels, label_name))


def reorder_dates(card: Card) -> None:
	if not card.description:
		return

	card.set_description(
		"\n".join(
			map(
				str.strip,
				sorted(
					card.description.splitlines(),
					key=_line_to_datetime,
					reverse=True,
				),
			),
		)
	)


#
# Utils
#
def _line_to_datetime(line: str) -> datetime:
	return datetime.strptime(line[:10], "%Y/%m/%d")


def _get_all_dates(card: Card) -> Iterable[datetime]:
	# the description is multi-lined,
	# each line is a date: yyyy/mm/dd
	# 				   or: yyyy/mm/dd (host)
	return map(_line_to_datetime, card.description.splitlines())


if __name__ == "__main__":
	main()
