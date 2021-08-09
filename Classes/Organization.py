
# this is only a plan

from TrelloScripts.consts import ORGANIZATIONS


class Organization(object):
	"""docstring for Organization"""
	def __init__(self, common_name=None, trello_name=None):
		self.name = self._get_name(common_name=None, trello_name=None)


	def _get_name(self, common_name=None, trello_name=None):
		raise NotImplemented

	def get_boards():
		raise NotImplemented


# client = get_client()
# organizations = client.list_organizations()
# organizations[4].all_boards()
