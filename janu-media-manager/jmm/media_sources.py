from models import db, Format, 
from httplib import HTTPSConnection
from settings import FORMATS
import json
import hashlib

def get_module(mediasource, data):
    module_name = mediasource.module.name
    data['media_source_id'] = mediasource.id
    return eval('%s(data)' % module_name)

class mediafire(object):
    def __init__(self, data):
        self._token = None
        self.user = user
        self.password = password
        self.appid = appid
        self.apikey = apikey

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
        signature = hashlib.sha1(self.user + self.password +
                                 self.appid + self.apikey).hexdigest()
        self._token = self._get_api_data('user', 'get_session_token',
                                         email=self.user, password=self.password,
                                         application_id=self.appid,
                                         signature=signature)['response']['session_token']
            
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
            format = db.session.query(Format.id).filter(Format.name == file_['mimetype']).first()
            if format:
                url = self._get_api_data('file', 'get_links', link_type='direct_download',
                                          quick_key=file_['quickkey'])['response']['links'][0]['direct_download']
                
                print url
        for folder in folders:
            self._populate_db_recursive(folder['folderkey'])

    def populate_db(self):
        self._renew_token()
        self._populate_db_recursive()

