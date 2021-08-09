import datetime
from TrelloScripts.consts import *


VERBOSE = 1000
def set_verbose(verbose):
	global VERBOSE
	VERBOSE = verbose


def log(s):
	if s.count('.') <= VERBOSE:
		print(s)
		f = open(LOGFILE, 'a')
		f.write('\n' + s)
		f.close()

def log_initialize():
	log("-------------")
	log(datetime.datetime.now().strftime("%Y/%m/%d %H:%M"))
