import datetime
import os
import re

from .consts import MAIN_FOLDER

VERBOSE = 1000


def set_verbose(verbose):
	global VERBOSE
	VERBOSE = verbose


LOGFILE = os.path.join(MAIN_FOLDER, "Logs", "tests.log")


def set_logfile(log_name: str):
	global LOGFILE
	LOGFILE = os.path.join(MAIN_FOLDER, "Logs", f"{log_name}.log")


_GET_INITIAL_DOTS = re.compile("^\\.*")


def log(s):
	num_dots = len(_GET_INITIAL_DOTS.match(s).group())
	if num_dots <= VERBOSE:
		print(s)
		with open(LOGFILE, "a") as f:
			f.write("\n" + s)


def log_initialize():
	if not os.path.exists(os.path.dirname(LOGFILE)):
		os.mkdir(os.path.dirname(LOGFILE))
	log("-------------")
	log(datetime.datetime.now().strftime("%Y/%m/%d %H:%M"))
