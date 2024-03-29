import os
import re
import datetime

from .consts import *


VERBOSE = 1000
def set_verbose(verbose):
	global VERBOSE
	VERBOSE = verbose


LOGFILE = os.path.join(MAIN_FOLDER, "Logs", "tests.log")
def set_logfile(file_name=None, absolute_path=None):
	global LOGFILE

	if absolute_path is not None:
		if '..' in absolute_path:
			raise ValueError("\"..\" is not allowed in a file_name")

		LOGFILE = absolute_path
		return

	if file_name:
		if '..' in file_name:
			raise ValueError("\"..\" is not allowed in a file_name")

		LOGFILE = os.path.join(MAIN_FOLDER, "Logs", file_name)
		return

	raise ValueError("No file name specified")


_GET_INITIAL_DOTS = re.compile("^\\.*")
def log(s):
	num_dots = len(_GET_INITIAL_DOTS.match(s).group())
	if num_dots <= VERBOSE:
		print(s)
		with open(LOGFILE, 'a') as f:
			f.write('\n' + s)

def log_initialize():
	if not os.path.exists(os.path.dirname(LOGFILE)):
		os.mkdir(os.path.dirname(LOGFILE))
	log("-------------")
	log(datetime.datetime.now().strftime("%Y/%m/%d %H:%M"))

def initialize_logfile(*log_args, **log_kwargs):
	def dec(func):
		def inner(*args, **kwargs):
			set_logfile(*log_args, **log_kwargs)
			log_initialize()

			return func(*args, **kwargs)
		return inner
	return dec
