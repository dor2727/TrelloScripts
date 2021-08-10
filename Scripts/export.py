#!/usr/bin/env python3

import os
import json
import datetime

from TrelloScripts.consts                import *
from TrelloScripts.log                   import log, log_initialize, set_logfile
from TrelloScripts.utils                 import *


EXPORT_PARAMETERS = {
	"fields"           : "all",
	"actions"          : "all",
	"action_fields"    : "all",
	"actions_limit"    : 1000 ,
	"cards"            : "all",
	"card_fields"      : "all",
	"card_attachments" : "true" ,
	"labels"           : "all",
	"lists"            : "all",
	"list_fields"      : "all",
	"members"          : "all",
	"member_fields"    : "all",
	"checklists"       : "all",
	"checklist_fields" : "all",
	"organization"     : "false",
}

def export_board(client, folder_name, board):
	log(f"..[*] Exporting {board.name} - {board.id}")


	# getting the board full data as json
	json_data = client.fetch_json(
		"/boards/" + board.id,
		query_params=EXPORT_PARAMETERS
	)

	# getting the organization
	if json_data["idOrganization"]:
		organization = client.get_organization( json_data["idOrganization"] )

		board_folder = os.path.join(
			folder_name,
			organization.name,
		)
	else:
		board_folder = os.path.join(
			folder_name,
			"Personal Boards",
		)

	if not os.path.isdir(board_folder):
		os.mkdir(board_folder)

	# file location:
	# 	export / <date> / <organization name> / <board id>_<board name>.json
	# board.name may include '/', which is replaced by '_'
	board_file_name = f"{board.id}_{board.name.replace('/', '_')}.json"

	file = open(
		os.path.join(
			board_folder,
			board_file_name
		),
		'w'
	)

	c = file.write(json.dumps(json_data, indent = 2, separators=(',', ': ')))
	print(f"....[*] wrote {c:7} bytes")
	file.close()

def initialize_export_folder():
	log("[*] creating folder")
	folder_name = os.path.join(
		MAIN_FOLDER,
		"Exports",
		datetime.datetime.now().strftime('%Y.%m.%d_%H.%M')
	)
	os.mkdir(folder_name)
	return folder_name

def compress_export(folder_name):
	return os.system(f"tar -I 'gzip -9' --remove-files -cf {folder_name}.tar.gz {folder_name}")


def main():
	set_logfile("export.log")

	log_initialize()

	client = get_client()

	folder_name = initialize_export_folder()


	log("[*] Getting boards")
	all_boards = client.list_boards()


	log("[*] Exporting boards")
	for board in all_boards:
		export_board(client, folder_name, board)


	compress_export(folder_name)

if __name__ == '__main__':
	main()
