import os
import datetime
from TrelloScripts.consts import *


VERBOSE = 1000
def set_verbose(verbose):
	global VERBOSE
	VERBOSE = verbose


LOGFILE = os.path.join(MAIN_FOLDER, "Logs/tests.log")
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


def log(s):
	if s.count('.') <= VERBOSE:
		print(s)
		f = open(LOGFILE, 'a')
		f.write('\n' + s)
		f.close()

def log_initialize():
	log("-------------")
	log(datetime.datetime.now().strftime("%Y/%m/%d %H:%M"))
