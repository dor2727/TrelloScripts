#!/usr/bin/env python3
from dataclasses import dataclass
from functools import cached_property

from trello import Board, Card, Label, List
from TrelloScripts.utils import _init, get_item, is_labeled, log

SUFFIX_BACKLOG = "Backlog"
SUFFIX_DONE = "Done"
SUFFIX_TOOK_INSPIRATION = "TookInspiration"

LABEL_TO_BACKLOG = "ToBacklog"
LABEL_TO_DONE = "Done"
LABEL_TO_TOOK_INSPIRATION = "TookInspiration"
LABEL_TO_MAIN_BOARD = "ToReading"
LABEL_COLOR = {
	LABEL_TO_DONE: "green",
	LABEL_TO_BACKLOG: "lime",
	LABEL_TO_MAIN_BOARD: "lime",
	LABEL_TO_TOOK_INSPIRATION: "green",
	"Wont do": "black",
}


def main() -> None:
	client, all_boards = _init("reading_sync", boards_filter=None)

	board_groups = [_get_board_groups(b, all_boards) for b in all_boards]

	for board_group in filter(bool, board_groups):
		sync_boards(board_group)
		sync_lists(board_group)
		log("\n")

	log("[*] Done")


#
# Grouping of source and destination boards
#
@dataclass
class BoardGroup:
	main: Board
	backlog: Board | None
	done: Board | None
	took_inspiration: Board | None

	def __bool__(self) -> bool:
		return any(board is not None for board in [self.backlog, self.done, self.took_inspiration])

	def __repr__(self) -> str:
		get_attr_repr = lambda attr: f"{attr}: {getattr(getattr(self, attr), "name", "None")}"
		attrs = ["main", "backlog", "done", "took_inspiration"]
		all_attrs_repr = ", ".join(map(get_attr_repr, attrs))
		return f"BoardGroup({all_attrs_repr})"

	def iter_non_main_boards(self) -> list[Board]:
		return [board for board in [self.backlog, self.done, self.took_inspiration] if board is not None]

	def iter_non_main_boards_data(self) -> "list[BoardData]":
		result = []
		if self.backlog is not None:
			result.append(BoardData(self.backlog, *_get_label_and_name(self.main, LABEL_TO_BACKLOG)))
		if self.done is not None:
			result.append(BoardData(self.done, *_get_label_and_name(self.main, LABEL_TO_DONE)))
		if self.took_inspiration is not None:
			result.append(BoardData(self.took_inspiration, *_get_label_and_name(self.main, LABEL_TO_TOOK_INSPIRATION)))
		return result


def _get_board_groups(b: Board, all_boards: list[Board]) -> BoardGroup:
	return BoardGroup(
		main=b,
		backlog=get_item(all_boards, f"{b.name} - {SUFFIX_BACKLOG}"),
		done=get_item(all_boards, f"{b.name} - {SUFFIX_DONE}"),
		took_inspiration=get_item(all_boards, f"{b.name} - {SUFFIX_TOOK_INSPIRATION}"),
	)


@dataclass
class BoardData:
	board: Board
	label_name: str
	label: Label

	@cached_property
	def lists(self) -> list[List]:
		return self.board.all_lists()


def sync_boards(boards: BoardGroup) -> None:
	# sync from main
	move_all_cards(boards.main, boards.iter_non_main_boards_data())

	# sync to main_board
	for board in boards.iter_non_main_boards():
		move_all_cards(board, [BoardData(boards.main, *_get_label_and_name(board, LABEL_TO_MAIN_BOARD))])


def move_all_cards(source_board: Board, destination_data: list[BoardData]) -> None:
	log(f'..[*] Synching cards : "{source_board.name}"')
	num_cards_moved = sum(_move_card(card, destination_data) for card in source_board.all_cards())
	if num_cards_moved:
		log(f"...[*] moved {num_cards_moved} cards")


def _move_card(card: Card, destination_data: list[BoardData]) -> bool:
	for data in destination_data:
		if is_labeled(card, data.label_name):
			log(f".....[*] found card - {card.name} - {data.label_name}")

			log(".........[*] Removing label")
			card.remove_label(data.label)

			log(".........[*] Getting destination list")
			list_name = card.get_list().name

			destination_list = get_item(data.lists, list_name)
			if destination_list is None:
				log(".............[*] Creating destination list")
				destination_list = data.board.add_list(list_name, "bottom")
				# reset data.lists cache
				del data.lists

			if destination_list.closed:
				log(".........[*] List is archived - un-archiving")
				destination_list.open()

			if card.closed:
				log(".........[*] Card is archived - un-archiving")
				card.open()

			log(f".........[*] Changing board (to {data.board.name} : {destination_list.name})")
			card.change_board(data.board.id, destination_list.id)

			log(".........[*] Done")

			return True
	return False


def _get_label_and_name(board: Board, label_name: str) -> tuple[str, Label]:
	label = get_item(board.get_labels(), label_name)

	if label is None:
		log(f"....[*] Creating label ({label_name})")
		label = board.add_label(label_name, LABEL_COLOR[label_name])

	return label_name, label


def sync_lists(boards: BoardGroup) -> None:
	_reset_lists_positions(boards.main)

	for board in boards.iter_non_main_boards():
		_sync_lists_order(boards.main, board)


def _sync_lists_order(source_board: Board, dest_board: Board) -> None:
	log(f'...[*] Synching lists : "{source_board.name}" --> "{dest_board.name}"')
	source_lists = source_board.all_lists()
	dest_lists = dest_board.all_lists()
	dest_lists_positions = [i.pos for i in dest_lists]

	some_high_number = max(dest_lists_positions, default=100_000)

	for index, destination_list in enumerate(dest_lists):
		source_list = get_item(source_lists, destination_list.name)
		if source_list is None:
			suffix = " (no source list found)"
			# check if there's no collisions
			if dest_lists_positions.count(destination_list.pos) > 1:
				new_pos = some_high_number + index * 1000
			else:
				new_pos = destination_list.pos
		else:
			suffix = ""
			new_pos = source_list.pos

		if new_pos != destination_list.pos:
			log(f"..........[*] Moving {destination_list.name} from {destination_list.pos} to {new_pos}{suffix}")
			destination_list.move(new_pos)


def _reset_lists_positions(board: Board) -> None:
	log(f'...[*] Reseting list positions : "{board.name}"')

	for index, lst in enumerate(sorted(board.all_lists(), key=lambda i: i.pos)):
		new_pos = (index + 1) * 1000
		if new_pos != lst.pos:
			log(f".........[*] Moving {lst.name} from {lst.pos} to {new_pos}")
			lst.move(new_pos)


if __name__ == "__main__":
	main()
