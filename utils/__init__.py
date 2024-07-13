from .consts import MAIN_FOLDER
from .iteration import iterate_boards, iterate_cards, requires_lables, BoardsFilter, _init
from .log import log, set_logfile, log_initialize, set_verbose
from .utils_trello import get_item, get_first_attachment, get_client, get_all_boards, is_labeled
from .utils_web import is_url
from .utils_web_read_link import read_link
from .utils_web_get_cover_url import get_cover_url

# ruff: noqa

# monkey patch
# https://github.com/sarumont/py-trello/issues/373
import trello
import json


def patched_fetch_json(self, uri_path, http_method="GET", headers=None, query_params=None, post_args=None, files=None):  # type: ignore
	"""Fetch some JSON from Trello"""

	# explicit values here to avoid mutable default values
	if headers is None:
		headers = {}
	if query_params is None:
		query_params = {}
	if post_args is None:
		post_args = {}

	# if files specified, we don't want any data
	data = None
	if files is None and post_args != {}:
		data = json.dumps(post_args)

	# set content type and accept headers to handle JSON
	if http_method in ("POST", "PUT", "DELETE") and not files:
		headers["Content-Type"] = "application/json; charset=utf-8"

	headers["Accept"] = "application/json"

	# construct the full URL without query parameters
	if uri_path[0] == "/":
		uri_path = uri_path[1:]
	url = "https://api.trello.com/1/%s" % uri_path

	if self.oauth is None:
		query_params["key"] = self.api_key
		query_params["token"] = self.api_secret

	# perform the HTTP requests, if possible uses OAuth authentication
	response = self.http_service.request(http_method, url, params=query_params, headers=headers, data=data, auth=self.oauth, files=files, proxies=self.proxies)

	if response.status_code == 401:
		raise trello.Unauthorized("%s at %s" % (response.text, url), response)
	if response.status_code != 200:
		raise trello.ResourceUnavailable("%s at %s" % (response.text, url), response)

	return response.json()


trello.TrelloClient.fetch_json = patched_fetch_json
