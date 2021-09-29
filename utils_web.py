import urllib
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from TrelloScripts.log import log

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
}


#
# An exported utility function
#
def is_url(url):
	if '\n' in url:
		return False
	scheme = urllib.parse.urlparse(url).scheme
	return scheme in ["https", "http"]



def get_domain(url):
	return urlparse(url).netloc

def get_bs(url):
	req = requests.get(url, headers=headers)
	if not req.ok:
		log(f".....[!] Failed getting URL: {url}")
		return None

	bs = BeautifulSoup(req.content, features="lxml")
	return bs

#
# The exported function
#
def read_link(url):
	domain = get_domain(url)

	if domain == "www.reddit.com":
		return read_link_reddit(url)
	elif domain in ("www.youtube.com", "youtu.be"): # m.youtube.com
		return read_link_youtube(url)
	else:
		return read_link_other(url)

def read_link_reddit():
	bs = get_bs(url)

	# in case the request failed.
	if bs is None:
		return None

	# from my manual test, bs.find_all("h1") brings two identical results.
	post_name = bs.find("h1").text

	return post_name

def read_link_youtube(url):
	bs = get_bs(url)

	# in case the request failed.
	if bs is None:
		return None

	# it should return "<video name> - YouTube"
	web_page_title = bs.find("title").text

	return web_page_title

def read_link_other(url):
	bs = get_bs(url)

	# in case the request failed.
	if bs is None:
		return None

	title = bs.find('title').text
	log(f".....[*] Setting title: {title}")
	return title
