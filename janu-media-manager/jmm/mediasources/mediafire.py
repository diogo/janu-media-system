from models import db
from httplib import HTTPSConnection
from threading import Thread
from sqlalchemy.orm import relationship
import json
import hashlib
import urllib2

def get_module_class():
    return mediafire

class mediafire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Text)
    password = db.Column(db.Text)
    appid = db.Column(db.Text)
    apikey = db.Column(db.Text)
    media_source_id = db.Column(db.Integer, db.ForeignKey('media_source.id'), nullable=False, unique=True)
    media_source = relationship('MediaSource', uselist=False, backref='media_source')

    def __init__(self, data=None, user=None, password=None,
                 appid=None, apikey=None, media_source_id=None):
        if data:
            super(mediafire, self).__init__(user=data['user'], password=data['password'],
                                            appid=data['appid'], apikey=data['apikey'],
                                            media_source_id=data['media_source_id'])
        else:
            super(mediafire, self).__init__()
        self._token = None
        self._threads = []
        self._medias = []

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

    def _get_medias(self, folder_key=None):
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
            self._medias.append({'content_type': file_['mimetype'], 'url': file_['quickkey']})
                
        for folder in folders:
            thread = Thread(target=self._get_medias, args=(folder['folderkey'],))
            self._threads.append(thread)
            thread.start()

    def get_media_url(self, url):
        self._get_token()
        return self._get_api_data('file', 'get_links', link_type='direct_download',
                                  quick_key=url)['response']['links'][0]['direct_download']

    def get_all_medias(self):
        self._get_token()
        self._get_medias()
        for thread in self._threads:
            thread.join()
        return self._medias
