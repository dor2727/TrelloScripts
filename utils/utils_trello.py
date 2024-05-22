import os
from typing import TypeVar

from trello import Board, Card, TrelloClient

from .consts import MAIN_FOLDER
from .log import log

#
# File utils
#


def try_read(file_path: str) -> str | None:
	try:
		with open(file_path) as f:
			return f.read().strip()
	except Exception:
		return None


def read(filename: str) -> str | None:
	if (result := try_read(filename)) is not None:
		return result

	path_in_directory = os.path.join(os.path.dirname(__file__), filename)
	if (result := try_read(path_in_directory)) is not None:
		return result

	path_in_secrets = os.path.join(MAIN_FOLDER, "secrets", filename)
	return try_read(path_in_secrets)


#
# Client utils
#
CLIENT = None


def get_client() -> TrelloClient:
	global CLIENT

	if CLIENT is None:
		CLIENT = TrelloClient(
			api_key=read("key"),
			api_secret=read("secret"),
			token=read("token"),
		)

	return CLIENT


def get_all_boards() -> list[Board]:
	client = get_client()
	log("[*] Getting boards")
	all_boards = client.list_boards()
	return all_boards


#
# Card utils
#

T = TypeVar("T")


def get_item(all_list: list[T], item_name: str, case_sensitive: bool = True) -> T | None:
	if case_sensitive:
		filter_function = lambda obj: obj.name == item_name
	else:
		item_name_lower = item_name.lower()
		filter_function = lambda obj: obj.name.lower() == item_name_lower

	try:
		return next(filter(filter_function, all_list))
	except StopIteration:
		return None


def is_labeled(card: Card, label_name: str | None = None) -> bool:
	# if label_name is a string, check if the card has that label
	if label_name:
		return any(label.name == label_name for label in card.labels)
	# Otherwise, simply check if there are any labels
	else:
		return bool(card.labels)


def get_first_attachment(card: Card) -> dict | None:
	for attachment in card.attachments:
		# youtube cover
		if attachment["name"] == "0.jpg":
			continue

		return attachment

	return None
