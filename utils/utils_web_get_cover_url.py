import re

from bs4 import BeautifulSoup

from .utils_web import Url, get_domain, url_to_bs


#
# The exported function
#
def get_cover_url(url: Url) -> Url | None:
	domain = get_domain(url)

	if domain == "www.reddit.com":
		return get_cover_url_reddit(url)
	elif domain in ("www.youtube.com", "m.youtube.com", "youtu.be"):  # noqa: SIM102
		if video_id := extract_youtube_video_id(url):
			return get_cover_url_from_youtube_video_id(video_id)


#
# Specific get-cover-url functions
#

#
# Reddit
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


#
# Youtube
#

YOUTUBE_THUMBNAIL_TEMPLATE = "http://img.youtube.com/vi/%s/0.jpg"


def get_cover_url_from_youtube_video_id(video_id: str) -> Url:
	return YOUTUBE_THUMBNAIL_TEMPLATE % video_id


YOUTUBE_VIDEO_ID_REGEX_STR = [
	# short youtube url (youtube.be)
	# example url: https://youtu.be/tCoEYFbDVoI?si=UEPMjicmUB1S5NzL
	"https://youtu\\.be/(.{11})\\?",
	# youtube shorts, from PC
	# example url: https://www.youtube.com/watch?v=9qqbco6I4JQ
	"https://www\\.youtube\\.com/watch\\?v=(.{11})",
	# youtube shorts, from mobile
	# example url: https://m.youtube.com/shorts/9qqbco6I4JQ
	"https://m\\.youtube\\.com/shorts/(.{11})",
]
YOUTUBE_VIDEO_ID_REGEX = [re.compile(s) for s in YOUTUBE_VIDEO_ID_REGEX_STR]

# tested on dummy url: "a.com/?a=5&v=abc123abc12&c=5"
YOUTUBE_VIDEO_ID_GENERIC_REGEX = re.compile("\\bv=(.{11})")


def extract_youtube_video_id(url: Url) -> str | None:
	for pattern in YOUTUBE_VIDEO_ID_REGEX:
		if match := re.match(pattern, url):
			return match.group(1)

	if match := re.search(YOUTUBE_VIDEO_ID_GENERIC_REGEX, url):
		return match.group(1)

	return None
