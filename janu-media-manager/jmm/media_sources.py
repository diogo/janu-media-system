from httplib import HTTPSConnection
import json
import hashlib

class MediaFire(object):
    def __init__(self, user_email, password, app_id, api_key):
        signature = hashlib.sha1(user_email + password + app_id + api_key).hexdigest()
        self._token = self._get_api_data('/api/user/get_session_token.php?email=%s&password=%s&application_id=%s&signature=%s&response_format=json'
                                         % (user_email, password, app_id, signature)
                                         )['response']['session_token']

    def _get_api_data(self, uri):
        conn = HTTPSConnection('www.mediafire.com')
        conn.request('GET', uri)
        response = conn.getresponse()
        if response.status == 200:
            return json.loads(response.read())
        else:
            return False

    def renew_token(self):
            self._token = self._get_api_data('/api/user/renew_session_token.php?session_token=%s&response_format=json'
                               % self._token)['response']['session_token']

    def get_root_content(self):
        self._get_folder_content()

    def _get_folder_content(self, folderkey=None):
        print folderkey
        if folderkey:
            print 'oi'
            files = self._get_api_data('/api/folder/get_content.php?session_token=%s&folderkey=%s&content_type=files&response_format=json'
                                         % (self._token, folderkey))['response']['folder_content']['files']
            folders = self._get_api_data('/api/folder/get_content.php?session_token=%s&folderkey=%s&response_format=json'
                                         % (self._token, folderkey))['response']['folder_content']['folders']
        else:
            print 'porra'
            files = self._get_api_data('/api/folder/get_content.php?session_token=%s&content_type=files&response_format=json'
                                         % self._token)['response']['folder_content']['files']
            folders = self._get_api_data('/api/folder/get_content.php?session_token=%s&response_format=json'
                                     % self._token)['response']['folder_content']['folders']
        print folders
        for _file in files:
            print _file['filename']
        for folder in folders:
            print folder['name']
            print folder['folderkey']
            self._get_folder_content(folder['folderkey'])

