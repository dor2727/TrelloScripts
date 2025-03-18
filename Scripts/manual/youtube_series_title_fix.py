#!/usr/bin/env python3

# mypy: disable-error-code="return-value"

import os
import re
from functools import lru_cache

from trello import Card
from TrelloScripts.utils import (
	iterate_cards,
	log,
	set_verbose,
)

TOTAL_DURATION = 0.0


def main() -> None:
	set_verbose(6)

	iterate_cards(
		log_name=os.path.splitext(os.path.basename(__file__))[0],
		apply_to_card=[update_title, count_total_hours],
		boards_filter="YouTube",
	)

	log(f"...[*] Total duration: {TOTAL_DURATION} hours")


def _print_card(card: Card) -> None:
	log(f'....[*] found card in board "{card.board.name}" : in list "{card.get_list().name}" : "{card.name}"')


def update_title(card: Card) -> None:
	duration_hours = _get_duration(card)
	if duration_hours is None:
		return

	if "(" in card.name:
		log("......[w] Card had already been delt with. Skipping.")
		return

	if duration_hours == int(duration_hours):
		duration_hours_str = str(int(duration_hours))
	else:
		duration_hours_str = f"{duration_hours:.1f}"

	new_title = f"{card.name} ({duration_hours_str}h)"
	log(f"......[*] Updating title from '{card.name}' to '{new_title}' ; {duration_hours=}")
	card.set_name(new_title)


def count_total_hours(card: Card) -> None:
	global TOTAL_DURATION
	duration_hours = _get_duration(card)
	TOTAL_DURATION += duration_hours or 0


@lru_cache(maxsize=1)
def _get_duration(card: Card) -> float | None:
	if card.name.startswith("---"):
		return

	_print_card(card)

	card_list = card.get_list().name
	if not card_list.startswith("Series - "):
		log("........[w] Card is in a list we're not dealing with.")
		return

	if not card.description:
		log("......[w] Card has no description. Skipping.")
		return

	for line in card.description.splitlines():
		if line.startswith("Total length : "):
			duration_hours: float = _parse_duration_to_hours(line)
			break
	else:
		log("......[w] Unable to find duration in description. Skipping.")
		return

	return duration_hours


def _parse_duration_to_hours(duration_str: str) -> float:
	time_units = {"day": 24, "hour": 1, "minute": 1 / 60, "second": 1 / 3600}
	total_hours = 0.0

	matches = re.findall(r"(\d+)\s+(day|hour|minute|second)", duration_str)
	for value, unit in matches:
		total_hours += int(value) * time_units[unit]

	return round(total_hours * 2) / 2  # Round to the nearest 0.5


if __name__ == "__main__":
	main()
