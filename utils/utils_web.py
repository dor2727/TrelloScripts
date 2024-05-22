import re
import urllib
from urllib.parse import unquote, urlparse

import requests
from bs4 import BeautifulSoup

from .log import log

headers = {
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
}


#
# An exported utility function
#
_allowed_schemes = ["https", "http"]


def is_url(url):
	if "\n" in url:
		return False
	scheme = urllib.parse.urlparse(url).scheme
	return scheme in _allowed_schemes


def get_domain(url):
	return urlparse(url).netloc


def get_bs(url):
	try:
		req = requests.get(url, headers=headers)
		if not req.ok:
			log(f".....[!] Failed getting URL: {url}")
			return None
	except requests.RequestException as exc:
		log(f".....[!] Failed getting URL: {url} ; {exc=}")
		return None

	bs = BeautifulSoup(req.content, features="lxml")
	return bs


def url_to_bs(func):
	def inner(url, *args, **kwargs):
		bs = get_bs(url)

		# in case the request failed.
		if bs is None:
			return None

		return func(bs, *args, **kwargs)

	return inner


#
# The exported function
#
def read_link(url):
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


@url_to_bs
def read_link_reddit(bs):
	# from my manual test, bs.find_all("h1") brings two identical results.
	post_name = bs.find("h1").text

	return post_name


@url_to_bs
def read_link_youtube(bs):
	# it should return "<video name> - YouTube"
	web_page_title = bs.find("title").text

	return web_page_title


def read_link_pdf(url):
	return unquote(url).split("/")[-1]


@url_to_bs
def read_link_other(bs):
	title = bs.find("title").text
	log(f".....[*] Setting title: {title}")
	return title


def get_cover_url(url):
	domain = get_domain(url)

	if domain == "www.reddit.com":
		return get_cover_url_reddit(url)
	elif domain in ("www.youtube.com", "m.youtube.com"):
		return get_cover_url_youtube_full(url)
	elif domain == "youtu.be":
		return get_cover_url_youtube_short(url)


@url_to_bs
def get_cover_url_reddit(bs):
	try:
		div_1 = bs.find(attrs={"data-test-id": "post-content"})
		div_1_children = list(div_1.children)

		div_2 = div_1_children[3]

		div_3 = next(div_2.children)

		a = next(div_3.children)
		assert a.name == "a"

		return a.attrs["href"]
	except:
		return


YOUTUBE_THUMBNAIL_TEMPLATE = "http://img.youtube.com/vi/%s/0.jpg"


def get_cover_url_from_youtube_video_id(video_id):
	return YOUTUBE_THUMBNAIL_TEMPLATE % video_id


YOUTUBE_PATTERN_FULL = re.compile("(?<=v=).{11}")


def get_cover_url_youtube_full(url):
	try:
		video_id = YOUTUBE_PATTERN_FULL.findall(url)[0]
		return get_cover_url_from_youtube_video_id(video_id)
	except:
		return


def get_cover_url_youtube_short(url):
	try:
		assert url.startswith("https://youtu.be/")
		assert len(url) == 28
		video_id = url[17:]
		return get_cover_url_from_youtube_video_id(video_id)
	except:
		return
