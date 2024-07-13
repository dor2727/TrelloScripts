from typing import TypeAlias
from urllib.parse import unquote

from bs4 import BeautifulSoup

from .log import log
from .utils_web import get_domain, url_to_bs

Url: TypeAlias = str
Title: TypeAlias = str

HEADERS = {
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
}


#
# The exported function
#
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
