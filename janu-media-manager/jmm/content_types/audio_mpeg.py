import os
import urllib2
from datetime import datetime
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError

def get_media_dict(media_url):
	file_name = '/tmp/jmm%d.mp3' % datetime.now().microsecond
	mp3_file = open(file_name, 'w+')
	media = urllib2.urlopen(media_url)
	media_content = media.readline()
	media_content += media.readline()
	media_content += media.readline()
	mp3_file.write(media_content)
	mp3_file.close()
	dict_ = None
	try:
		mp3_tags = EasyID3(file_name)
		dict_ = {k: v[0] for k, v in mp3_tags.items()}
		if not dict_.has_key('artist'):
			raise ID3NoHeaderError()
		if not dict_.has_key('genre'):
			raise ID3NoHeaderError()
		if dict_.has_key('title'):
			dict_['name'] = dict_['title']
			dict_.pop('title')
		else:
			raise ID3NoHeaderError()
		genres = dict_['genre'].split(',')
		dict_['genre'] = []
		for genre in genres:
			dict_['genre'].append(genre.strip())
		if dict_.has_key('album'):
			dict_['collection'] = dict_['album']
			dict_.pop('album')
		if dict_.has_key('date'):
			dict_['date'] = datetime(int(dict_['date']), 1, 1)
		if dict_.has_key('tracknumber'):
			dict_['collection_position'] = dict_['tracknumber']
			dict_.pop('tracknumber')
	except ID3NoHeaderError:
		dict_ = None
	try:
		os.remove(file_name)
	except OSError:
		pass
	if dict_:
		dict_['url'] = media_url
	return dict_