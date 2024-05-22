import datetime
import os
import re

from .consts import MAIN_FOLDER

VERBOSE: int = 1000


def set_verbose(verbose: int) -> None:
	global VERBOSE
	VERBOSE = verbose


LOGFILE = os.path.join(MAIN_FOLDER, "Logs", "tests.log")


def set_logfile(log_name: str) -> None:
	global LOGFILE
	LOGFILE = os.path.join(MAIN_FOLDER, "Logs", f"{log_name}.log")


_GET_INITIAL_DOTS = re.compile("^\\.*")


def log(s: str) -> None:
	num_dots = len(_GET_INITIAL_DOTS.match(s).group())  # type: ignore[union-attr]
	if num_dots <= VERBOSE:
		print(s)
		with open(LOGFILE, "a") as f:
			f.write("\n" + s)


def log_initialize() -> None:
	if not os.path.exists(os.path.dirname(LOGFILE)):
		os.mkdir(os.path.dirname(LOGFILE))
	log("-------------")
	log(datetime.datetime.now().strftime("%Y/%m/%d %H:%M"))
