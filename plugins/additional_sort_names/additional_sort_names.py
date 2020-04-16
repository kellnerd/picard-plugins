PLUGIN_NAME = 'Additional Sort Names'
PLUGIN_AUTHOR = 'David Kellner'
PLUGIN_VERSION = '1.0'
PLUGIN_API_VERSIONS = ['2.1', '2.3']
PLUGIN_LICENSE = 'GPL-2.0-or-later'
PLUGIN_LICENSE_URL = 'https://www.gnu.org/licenses/gpl-2.0.html'
PLUGIN_DESCRIPTION = '''
Provides the artist sort names for writers and lyricists.
Values are available as additional variables <code>_writersort</code> and
<code>_lyricistsort</code> for usage in a script.
'''


from picard import log
from picard.metadata import register_track_metadata_processor


def provide_sort_names(album, metadata, track, release):
    recording = track['recording']
    if not 'relations' in recording:
        log.error('Please enable track relationships in the metadata options.')
        return
    writer_sort = []
    lyricist_sort = []
    for recording_rel in recording['relations']:
        if recording_rel['type'] == 'performance':
            work = recording_rel['work']
            if not 'relations' in work:
                continue
            for work_rel in work['relations']:
                rel_type = work_rel['type']
                if not rel_type in ['writer', 'lyricist']:
                    continue
                artist = work_rel['artist']
                if rel_type == 'writer':
                    writer_sort.append(artist['sort-name'])
                elif rel_type == 'lyricist':
                    lyricist_sort.append(artist['sort-name'])
    metadata['~writersort'] = writer_sort
    metadata['~lyricistsort'] = lyricist_sort


register_track_metadata_processor(provide_sort_names)
