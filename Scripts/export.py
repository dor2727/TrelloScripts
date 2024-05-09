#!/usr/bin/env python3

import os
import json
import datetime
from functools import lru_cache

from TrelloScripts.utils.consts import *
from TrelloScripts.utils.log    import log, initialize_logfile
from TrelloScripts.utils.utils  import *

UNKNOWN_ORGANIZATION_FOLDER = "Other_Organization"

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

@lru_cache(maxsize=None)
def get_organization(client, organization_id: str) -> str:
	try:
		# this line may fail due to ConnectionError
		json_data = client.fetch_json(f"/organizations/{organization_id}")
		# this line may fail due to KeyError
		return json_data["displayName"]
	except:
		return UNKNOWN_ORGANIZATION_FOLDER

def export_board(client, folder_name, board):
	log(f"..[*] Exporting {board.name} - {board.id}")


	# getting the board full data as json
	json_data = client.fetch_json(
		"/boards/" + board.id,
		query_params=EXPORT_PARAMETERS
	)

	# getting the organization
	if json_data["idOrganization"]:
		organization_name = get_organization(client, json_data["idOrganization"])
	else:
		if json_data["closed"]:
			organization_name = "closed"
		else:
			organization_name = UNKNOWN_ORGANIZATION_FOLDER

	board_folder = os.path.join(
		folder_name,
		organization_name,
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
	log(f"....[*] wrote {c:7} bytes \t;\t {organization_name=}")
	file.close()

def initialize_export_folder():
	if not os.path.exists(os.path.join(MAIN_FOLDER, "Exports")):
		os.mkdir(os.path.join(MAIN_FOLDER, "Exports"))

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


@initialize_logfile("export.log")
def main():
	client = get_client()
	all_boards = get_all_boards()

	folder_name = initialize_export_folder()

	log("[*] Exporting boards")
	for board in all_boards:
		export_board(client, folder_name, board)

	compress_export(folder_name)

	log("[*] Done")

if __name__ == '__main__':
	main()
