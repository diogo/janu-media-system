
class JMMDBError(Exception):
	pass

class JMMDataBase(object):
	def __init__(self, url, user=None, password=None):
		self._url = url
		self._user = user
		self._password = password

	def executeSQL(self, sql, ret_type=None):
		pass