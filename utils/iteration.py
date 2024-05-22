from typing import Callable

from TrelloScripts.utils.log import set_logfile, log_initialize, log
from TrelloScripts.utils.utils import get_client, get_all_boards

from trello import Board, TrelloClient

Args = tuple

def iterate_boards(
	log_name: str,
	apply_to_board: Callable[[TrelloClient, Board, Args], bool],
	boards_filter: filter | list[str] | None=None,
	pre_iteration: Callable[[None], [Args]] | None=None,
	post_iteration: Callable[[Args], None] | None=None,
):
	boards = init(log_name, boards_filter)

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
	apply_to_card: list[callable],
	boards_filter: filter | list[str] | None=None,
):
	boards = init(log_name, boards_filter)
	breakpoint()

	log("[*] Iterating cards")
	for board in boards:
		labels = board.get_labels()

		for card in board.all_cards():
			for func in apply_to_card:
				if getattr(func, "requires_labels", False):
					func(card, labels)
				else:
					func(card)

	log("[*] Done")

#
# Utils
#
def init(log_name: str, boards_filter: filter | list[str] | None=None) -> list[Board]:
	# init logging
	set_logfile(log_name)
	log_initialize()

	# init client
	client = get_client()
	# init boards
	all_boards = get_all_boards()
	boards = filter_boards(all_boards, boards_filter)
	return boards


def filter_boards(all_boards: list[Board], boards_filter: filter | list[str] | None) -> list[Board]:
	if boards_filter is None:
		return all_boards
	elif isinstance(boards_filter, list):
		return get_boards_by_name(all_boards, boards_filter)
	elif callable(boards_filter):
		return list(filter(boards_filter, all_boards))
	else:
		raise ValueError("Invalid boards_filter given")

def get_boards_by_name(all_boards: list[Board], names: list[str]) -> list[Board]:
	return sum(
		(
			[b for b in all_boards if name in b.name]
			for name in names
		),
		[]
	)
