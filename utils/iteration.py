from typing import Callable

from trello import Board, Card, TrelloClient
from TrelloScripts.utils.log import log, log_initialize, set_logfile
from TrelloScripts.utils.utils_trello import get_all_boards, get_client

Args = tuple

BoardsFilter = Callable[[Board], bool] | list[str] | None


def iterate_boards(
	log_name: str,
	apply_to_board: Callable[[TrelloClient, Board, Args], bool],
	boards_filter: BoardsFilter = None,
	pre_iteration: Callable[[], Args] | None = None,
	post_iteration: Callable[[Args], None] | None = None,
) -> None:
	client, boards = _init(log_name, boards_filter)

	# pre-iteration
	if pre_iteration is not None:
		args = pre_iteration()
		if not isinstance(args, tuple):
			args = (args,)
	else:
		args = ()

	log("[*] Iterating boards")
	for board in boards:
		apply_to_board(client, board, *args)

	# post-iteration
	if post_iteration is not None:
		post_iteration(*args)

	log("[*] Done")


def iterate_cards(
	log_name: str,
	apply_to_card: list[Callable],
	boards_filter: BoardsFilter = None,
	skip_archived: bool = True,
) -> None:
	_, boards = _init(log_name, boards_filter)

	log("[*] Iterating cards")
	for board in boards:
		log(f"..[*] Iterating {board.name}")

		labels = board.get_labels()

		for card in board.all_cards():
			if skip_archived and is_card_archived(card):
				log(f"..........[*] Skipping archived card : {card.name}")
				continue

			for func in apply_to_card:
				if getattr(func, "requires_labels", False):
					func(card, labels)
				else:
					func(card)

	log("[*] Done")


def requires_lables(func: Callable) -> Callable:
	func.requires_labels = True  # type: ignore[attr-defined]
	return func


#
# Utils
#
def _init(log_name: str, boards_filter: BoardsFilter = None) -> tuple[TrelloClient, list[Board]]:
	# init logging
	set_logfile(log_name)
	log_initialize()

	# init client
	client = get_client()
	# init boards
	all_boards = get_all_boards()
	boards = filter_boards(all_boards, boards_filter)
	return client, boards


def filter_boards(all_boards: list[Board], boards_filter: BoardsFilter) -> list[Board]:
	if boards_filter is None:
		return all_boards
	elif isinstance(boards_filter, list):
		return get_boards_by_name(all_boards, boards_filter)
	elif callable(boards_filter):
		return list(filter(boards_filter, all_boards))
	else:
		raise ValueError("Invalid boards_filter given")


def get_boards_by_name(all_boards: list[Board], names: list[str]) -> list[Board]:
	return sum(([b for b in all_boards if name.lower() in b.name.lower()] for name in names), [])


def is_card_archived(card: Card) -> bool:
	return card.closed or card.get_list().closed
