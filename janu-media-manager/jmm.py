# encoding: utf-8

from os import path
from messages import *
from flask.ext import restful
from models import *

class JMMSettingError(Exception):
	pass

class JanuMediaManager(object):
	def __init__(self, settings_filepath=None):
		self._settings = {}
		self._modules = {}
		self.reload_settings(settings_filepath)
		self._set_database()

	def _load_settings_file(self, filepath):
		if filepath is None:
			filepath = "%s/settings" % path.realpath(path.dirname(__file__))
		settings_file = open(filepath, 'r')
		settings = {}
		for setting in settings_file.readlines():
			setting = setting.strip()
			if setting.startswith('#'):
				continue
			elif setting == '':
				continue
			var, values = setting.split('=')
			var = var.strip()
			values = values.split(',')
			values = [x.strip() for x in values]
			if values[0] == '':
				raise JMMSettingError(SETTING_EMPTY_ERROR % var)
			settings[var] = values
		settings_file.close()

		# retorna True se as configurações do banco mudaram
		ret = False
		for nsk, nsv in settings.items():
			for sk, sv in self._settings.items():
				if sk.startswith('db_') and sk == nsk and sv != nsv:
					ret = True

		self._settings = settings
		return ret

	def _load_modules(self):
		modules = {}
		for module in self._settings.keys():
			if not module.startswith('db_'):
				modules[module] = {}
				for submodule in self._settings[module]:
					try:
						modules[module][submodule] = __import__('jmm.modules.%s.%s'\
							% (module, submodule), fromlist=['jmm', 'modules', module])
					except ImportError:
						raise JMMSettingError(MODULE_NOT_SUPPORTED_ERROR\
							% '%s.%s' % (module,submodule))
		self._modules = modules

	def _set_database(self):
		db_type = self._settings['db_type'][0]
		db_url = self._settings['db_url'][0]
		self._db = self._modules['databases'][db_type].new(db_url)

	def reload_settings(self, settings_filepath=None):
		if self._load_settings_file(settings_filepath):
			self._set_database()
		self._load_modules()

	def _init_restful(self):
		pass