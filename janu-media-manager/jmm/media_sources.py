from httplib import HTTPSConnection
from threading import Thread
from settings import FORMATS
import json
import hashlib

class MediaFire(object):
    def __init__(self, email, password, app_id, api_key):
        self._signature = hashlib.sha1(email + password + app_id + api_key).hexdigest()
        self._email = email
        self._password = password
        self._app_id = app_id
        self._token = None
        self._get_token()

    def _get_api_data(self, type_, method, **kwargs):
        conn = HTTPSConnection('www.mediafire.com')
        uri = '/api/%s/%s.php?response_format=json' % (type_, method)
        if self._token:
            uri = uri + '&session_token=%s' % self._token
        if len(kwargs):
            for key, value in kwargs.items():
                uri = uri + '&%s=%s' % (key, value)
        conn.request('GET', uri)
        response = conn.getresponse()
        if response.status == 200:
            return json.loads(response.read())
        else:
            return None

    def _get_token(self):
        self._token = self._get_api_data('user', 'get_session_token',
                                         email=self._email, password=self._password,
                                         application_id=self._app_id,
                                         signature=self._signature)['response']['session_token']

    def _renew_token(self):
        new_token = self._get_api_data('user', 'renew_session_token')['response']['session_token']
        if new_token:
            self._token = new_token
        else:
            self._get_token()

    def _populate_db_recursive(self, folder_key=None):
        if folder_key:
            files = self._get_api_data('folder', 'get_content', folder_key=folder_key,
                                       content_type='files')['response']['folder_content']['files']
            folders = self._get_api_data('folder', 'get_content',
                                         folder_key=folder_key)['response']['folder_content']['folders']
        else:
            files = self._get_api_data('folder', 'get_content',
                                       content_type='files')['response']['folder_content']['files']
            folders = self._get_api_data('folder', 'get_content')['response']['folder_content']['folders']

        for file_ in files:
            if FORMATS.has_key(file_['mimetype']):
                url = self._get_api_data('file', 'get_links', link_type='direct_download',
                                          quick_key=file_['quickkey'])['response']['links'][0]['direct_download']
                #tags = FORMATS[file_['mimetype']](direct_link)
                print url
        for folder in folders:
            self._populate_db_recursive(folder['folderkey'])

    def populate_db(self):
        self._populate_db_recursive()

