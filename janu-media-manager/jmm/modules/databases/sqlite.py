from common import JMMDataBase, JMMDBError
import sqlite3 as sqlite
from jmm.messages import *

class JMMSQLite(JMMDataBase):
	def __init__(self, url, user=None, password=None):
		JMMDataBase.__init__(self, url, user, password)
		self._connect()
		self._con.close()

	def _connect(self):
		try:
			self._con = sqlite.connect(self._url)
		except sqlite.Error:
			raise JMMDBError(DB_CONNECTION_ERROR % self._url)

	def executeSQL(self, sql, ret_type=None):
		self._connect()
		cur = self._con.cursor()
		ret = False

		try:
			cur.execute(sql)
		except sqlite.Error:
			self._con.rollback()
			self._con.close()
			raise JMMDBError(DB_SQL_SYNTAX_ERROR % sql)

		try:
			if ret_type == 'one':
				ret = cur.fetchone()
			elif ret_type == 'all':
				ret = cur.fetchall()
			elif ret_type == 'many':
				ret = cur.fetchmany()
			elif ret_type == 'last_id':
				ret = cur.lastrowid
			elif ret_type == None:
				ret = True
			else:
				raise JMMDBError(UNSUPPORTED_RET_TYPE_ERROR % ret_type)
		except sqlite.Error:
			self._con.rollback()
			self._con.close()
			raise JMMDBError(DB_RET_TYPE_ERROR % (ret_type, sql))

		self._con.close()
		return ret

def new(url, user=None, password=None):
	return JMMSQLite(url, user, password)