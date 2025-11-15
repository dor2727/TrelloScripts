#!/usr/bin/env python3
import os
import sys
from datetime import datetime
from pprint import pformat
from typing import Callable, Iterable

from trello import Card
from TrelloScripts.utils import iterate_cards, log, set_verbose

LATEST = datetime.min
LATEST_N: list[datetime] = []


def main(n: int = 1) -> None:
	set_verbose(4)

	iterate_cards(
		log_name=os.path.splitext(os.path.basename(__file__))[0],
		# apply_to_card=[get_latest_date],
		apply_to_card=[get_latest_n_dates(n)],
		boards_filter=lambda b: b.name == "Friends",
	)

	print("-" * 50)
	print(f"Latest date: {LATEST}")
	print(f"Latest dates:\n{pformat(LATEST_N)}")


def get_latest_date(card: Card) -> None:
	if not card.description:
		return

	global LATEST
	latest = max(_get_all_dates(card))
	if latest > LATEST:
		LATEST = latest
		log(f"[*] Latest date: {LATEST} (in card: {card.name})")


def get_latest_n_dates(n: int) -> Callable:
	def inner(card: Card) -> None:
		if not card.description:
			return

		global LATEST_N
		this_card_latest = max(_get_all_dates(card))
		if this_card_latest > min(LATEST_N, default=datetime.min):
			log(f"[*] New latest date: {this_card_latest} (in card: {card.name})")
		LATEST_N = sorted(set([this_card_latest] + LATEST_N), reverse=True)[:n]

	return inner


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
	if len(sys.argv) > 1:
		n = int(sys.argv[1])
	else:
		n = 1
	main(n)
