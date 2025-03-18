import urllib
from typing import Any, Callable, TypeAlias, TypeVar
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from .log import log

Url: TypeAlias = str
Title: TypeAlias = str

HEADERS = {
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0",
}


#
# An exported utility function
#
_ALLOWED_SCHEMES = ["https", "http"]


#
# The exported function
#
def is_url(url: Url) -> bool:
	if "\n" in url:
		return False
	scheme = urllib.parse.urlparse(url).scheme
	return scheme in _ALLOWED_SCHEMES


#
# Reading-link utils
#


def get_domain(url: Url) -> str:
	return urlparse(url).netloc


def get_bs(url: Url) -> BeautifulSoup:
	try:
		req = requests.get(url, headers=HEADERS)
		if not req.ok:
			log(f".....[!] Failed getting URL: {url}")
			return None
	except requests.RequestException as exc:
		log(f".....[!] Failed getting URL: {url} ; {exc=}")
		return None

	bs = BeautifulSoup(req.content, features="lxml")
	return bs


T = TypeVar("T")


def url_to_bs(func: Callable[[BeautifulSoup], T]) -> Callable[[Url], T]:
	def inner(url: Url, *args: Any, **kwargs: Any) -> Any:
		bs = get_bs(url)

		# in case the request failed.
		if bs is None:
			return None

		return func(bs, *args, **kwargs)

	return inner
