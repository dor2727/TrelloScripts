#!/usr/bin/env python3

import datetime
import json
import os

from trello import Board, TrelloClient
from TrelloScripts.utils import MAIN_FOLDER, iterate_boards, log


def main() -> None:
	iterate_boards(
		log_name=os.path.splitext(os.path.basename(__file__))[0],
		apply_to_board=export_board,
		boards_filter=None,  # get all boards
		pre_iteration=initialize_export_folder,
		post_iteration=compress_export,
		filter_out_old_boards=False,
	)


def export_board(client: TrelloClient, board: Board, root_folder_name: str) -> None:
	log(f"..[*] Exporting {board.name} - {board.id}")

	board_data = get_board_data(client, board)

	organization_name = get_organization_name(client, board_data)

	organization_folder_name = get_folder(root_folder_name, organization_name)
	file_name = get_file_name(board)

	data_length = dump_board_data_to_file(os.path.join(organization_folder_name, file_name), board_data)

	log(f"....[*] wrote {data_length:7} bytes \t;\t {organization_name=}")


def initialize_export_folder() -> str:
	if not os.path.exists(os.path.join(MAIN_FOLDER, "Exports")):
		os.mkdir(os.path.join(MAIN_FOLDER, "Exports"))

	log("[*] creating export folder")
	folder_name = os.path.join(
		MAIN_FOLDER,
		"Exports",
		datetime.datetime.now().strftime("%Y.%m.%d_%H.%M"),
	)
	os.mkdir(folder_name)
	return folder_name


def compress_export(folder_name: str) -> int:
	return os.system(f"tar -I 'gzip -9' --remove-files -cf {folder_name}.tar.gz {folder_name}")


#
# Export Board Utils
#
EXPORT_PARAMETERS = {
	"fields": "all",
	"actions": "all",
	"action_fields": "all",
	"actions_limit": 1000,
	"cards": "all",
	"card_fields": "all",
	"card_attachments": "true",
	"labels": "all",
	"lists": "all",
	"list_fields": "all",
	"members": "all",
	"member_fields": "all",
	"checklists": "all",
	"checklist_fields": "all",
	"organization": "true",
}


def get_board_data(client: TrelloClient, board: Board) -> dict:
	return client.fetch_json(
		"/boards/" + board.id,
		query_params=EXPORT_PARAMETERS,
	)


def get_organization_name(client: TrelloClient, board_data: dict) -> str:
	if board_data["closed"]:
		organization_name = "closed"
	else:
		organization_name = board_data.get("organization", {}).get("name", "Unknown_organization")
	return organization_name


# file location:
# 	export / <date> / <organization name> / <board id>_<board name>.json
def get_folder(root_folder_name: str, organization_name: str) -> str:
	folder = os.path.join(
		root_folder_name,
		organization_name,
	)

	if not os.path.isdir(folder):
		os.mkdir(folder)

	return folder


def get_file_name(board: Board) -> str:
	# board.name may include '/', which is replaced by '_'
	return f"{board.id}_{board.name.replace('/', '_')}.json"


def dump_board_data_to_file(full_file_path: str, board_data: dict) -> int:
	with open(full_file_path, "w") as file:
		return file.write(json.dumps(board_data, indent=2, separators=(",", ": ")))


if __name__ == "__main__":
	main()
