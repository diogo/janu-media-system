import urllib2
from datetime import datetime
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
from models import Artist, Genre, Playlist, MediaGenres, MediaArtists, Media



def get_media_dict(media_url):
	file_name = '/tmp/jmm%d.mp3' % datetime.now().microsecond
	mp3_file = open(file_name, 'w+')
	mp3_file.write(urllib2.urlopen(media_url).readline())
	mp3_file.close()
	try:
		dict_ = {k: v[0] for k, v in EasyID3(file_name).items()}
		if not dict_.has_key('artist'):
			return None
		if not dict_.has_key('genre'):
			return None
		if dict_.has_key('title'):
			dict_['name'] = dict_['title']
			dict_.pop('title')
		else:
			return None
		if dict_.has_key('album'):
			dict_['collection'] = dict_['album']
			dict_.pop('album')
		if dict_.has_key('date'):
			dict_['date'] = datetime(int(dict_['date']), 1, 1)
		if dict_.has_key('tracknumber'):
			dict_['collection_position'] = dict_['tracknumber']
			dict_.pop('tracknumber')
		return dict_
	except ID3NoHeaderError:
		return None
