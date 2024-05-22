import re
import urllib
from typing import Any, Callable, TypeAlias, TypeVar
from urllib.parse import unquote, urlparse

import requests
from bs4 import BeautifulSoup

from .log import log

Url: TypeAlias = str
Title: TypeAlias = str

HEADERS = {
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
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


def read_link(url: Url) -> Title | None:
	domain = get_domain(url)

	if domain == "www.reddit.com":
		return read_link_reddit(url)
	elif domain in ("www.youtube.com", "youtu.be"):  # m.youtube.com
		return read_link_youtube(url)
	else:
		if url.lower().endswith(".pdf"):
			return read_link_pdf(url)
		else:
			return read_link_other(url)


def get_cover_url(url: Url) -> Url | None:
	domain = get_domain(url)

	if domain == "www.reddit.com":
		return get_cover_url_reddit(url)
	elif domain in ("www.youtube.com", "m.youtube.com"):
		return get_cover_url_youtube_full(url)
	elif domain == "youtu.be":
		return get_cover_url_youtube_short(url)


#
# read-link utils
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


def url_to_bs(
	func: Callable[
		[
			BeautifulSoup,
		],
		T,
	],
) -> Callable[[Url], T]:
	def inner(url: Url, *args: Any, **kwargs: Any) -> Any:
		bs = get_bs(url)

		# in case the request failed.
		if bs is None:
			return None

		return func(bs, *args, **kwargs)

	return inner


#
# Specific read-link functions
#
@url_to_bs
def read_link_reddit(bs: BeautifulSoup) -> Title:
	# from my manual test, bs.find_all("h1") brings two identical results.
	post_name = bs.find("h1").text

	return post_name


@url_to_bs
def read_link_youtube(bs: BeautifulSoup) -> Title:
	# it should return "<video name> - YouTube"
	web_page_title = bs.find("title").text

	return web_page_title


def read_link_pdf(url: Url) -> Title:
	return unquote(url).split("/")[-1]


@url_to_bs
def read_link_other(bs: BeautifulSoup) -> Title:
	title = bs.find("title").text
	log(f".....[*] Setting title: {title}")
	return title


#
# Specific get-cover-url functions
#
@url_to_bs
def get_cover_url_reddit(bs: BeautifulSoup) -> Url | None:
	try:
		div_1 = bs.find(attrs={"data-test-id": "post-content"})
		div_1_children = list(div_1.children)

		div_2 = div_1_children[3]

		div_3 = next(div_2.children)

		a = next(div_3.children)
		assert a.name == "a"

		return a.attrs["href"]
	except Exception:
		return None


YOUTUBE_THUMBNAIL_TEMPLATE = "http://img.youtube.com/vi/%s/0.jpg"


def get_cover_url_from_youtube_video_id(video_id: str) -> Url:
	return YOUTUBE_THUMBNAIL_TEMPLATE % video_id


YOUTUBE_PATTERN_FULL = re.compile("(?<=v=).{11}")


def get_cover_url_youtube_full(url: Url) -> Url | None:
	try:
		video_id = YOUTUBE_PATTERN_FULL.findall(url)[0]
		return get_cover_url_from_youtube_video_id(video_id)
	except Exception:
		return None


def get_cover_url_youtube_short(url: Url) -> Url | None:
	try:
		assert url.startswith("https://youtu.be/")
		assert len(url) == 28
		video_id = url[17:]
		return get_cover_url_from_youtube_video_id(video_id)
	except Exception:
		return None
