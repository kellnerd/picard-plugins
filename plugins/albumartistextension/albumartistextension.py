PLUGIN_NAME = 'AlbumArtist Extension'
PLUGIN_AUTHOR = 'Bob Swift (rdswift)'
PLUGIN_DESCRIPTION = '''
This plugin provides standardized, credited and sorted artist information
for the album artist.  This is useful when your tagging or renaming scripts
require both the standardized artist name and the credited artist name, or
more detailed information about the album artists.
<br /><br />
The information is provided in the following variables:
<ul>
<li>_aaeStdAlbumArtists = The standardized version of album artist(s)
<li>_aaeCredAlbumArtists = The credited version of album artist(s)
<li>_aaeSortAlbumArtists = The sorted version of album artist(s)
<li>_aaeAlbumArtistCount = The number of artists comprising the album artist.
<li>_aaeStdAlbumArtist_n = The standardized version of the album artists,
    where n is the number of the artist in the list starting at 0.  If there 
    are two artists in the AlbumArtist tag, then they will be available in 
    the _aaeStdAlbumArtist_0 and _aaeStdAlbumArtist_1 variables. 
<li>_aaeCredAlbumArtist_n = The credited version of the album artists,
    where n is the number of the artist in the list starting at 0.  If there
    are two artists in the AlbumArtist tag, then they will be available in
    the _aaeCredAlbumArtist_0 and _aaeCredAlbumArtist_1 variables.
<li>_aaeSortAlbumArtist_n = The sorted version of the album artists, where
    n is the number of the artist in the list starting at 0.  If there are
    two artists in the AlbumArtist tag, then they will be available in the
    _aaeSortAlbumArtist_0 and _aaeSortAlbumArtist_1 variables.
<li>_aaeJoinPhrase_n = The phrases used to join the album artists, where n
    is the number of the phrase in the list starting at 0.  NOTE: This
    variable will not be provided if there is only one artist in the
    AlbumArtist tag.  The user should check that _aaeAlbumArtistCount is
    greater than one before using this variable.
</ul>
PLEASE NOTE: Tagger scripts are required to make use of these hidden
variables.
'''

PLUGIN_VERSION = "0.3"
PLUGIN_API_VERSIONS = ["1.4"]
PLUGIN_LICENSE = "GPL-2.0 or later"
PLUGIN_LICENSE_URL = "https://www.gnu.org/licenses/gpl-2.0.html"

from picard import log
from picard.metadata import register_album_metadata_processor

class AlbumArtistStdName:

    @staticmethod
    def add_artist_std_name(album, album_metadata, releaseXmlNode):
        albumid = releaseXmlNode.id
        # Test for valid XML node for the release
        if 'artist_credit' in releaseXmlNode.children:
            # Initialize variables to default values
            credArtist = ""
            stdArtist = ""
            sortArtist = ""
            aCount = 0
            jPhrase = []
            # The 'name_credit' child should always be there.
            # This check is to avoid a runtime error if it doesn't exist for some reason.
            if 'name_credit' in releaseXmlNode.artist_credit[0].children:
                for ncredit in releaseXmlNode.artist_credit[0].name_credit:
                    # Initialize temporary variables for each loop.
                    tempStdName = ""
                    tempCredName = ""
                    tempSortName = ""
                    tempPhrase = ""
                    # Check if there is a 'joinphrase' specified.
                    if 'joinphrase' in ncredit.attribs:
                        tempPhrase = ncredit.joinphrase
                        jPhrase.append(tempPhrase)
                    # Check if there is a 'name' specified.  This will be the
                    # credited name.
                    if 'name' in ncredit.children:
                        tempCredName = ncredit.name[0].text
                    # The 'artist' child should always be there.
                    # This check is to avoid a runtime error if it doesn't
                    # exist for some reason.
                    if 'artist' in ncredit.children:
                        # The 'name' child should always be there.
                        # This check is to avoid a runtime error if it
                        # doesn't exist for some reason.
                        if 'name' in ncredit.artist[0].children:
                            tempStdName = ncredit.artist[0].name[0].text
                            stdArtist += tempStdName + tempPhrase
                            album_metadata["~aaeStdAlbumArtist_%i" % aCount] = tempStdName
                            tCredName = tempCredName if len(tempCredName) > 0 else tempStdName
                            credArtist += tCredName + tempPhrase
                            album_metadata["~aaeCredAlbumArtist_%i" % aCount] = tCredName
                        else:
                            log.error("%s: %r: Missing artist 'name' in XML contents: %s",
                                    PLUGIN_NAME, albumid, releaseXmlNode)
                        # The 'sort_name' child should always be there.
                        # This check is to avoid a runtime error if it
                        # doesn't exist for some reason.
                        if 'sort_name' in ncredit.artist[0].children:
                            tempSortName = ncredit.artist[0].sort_name[0].text
                            sortArtist += tempSortName + tempPhrase
                            album_metadata["~aaeSortAlbumArtist_%i" % aCount] = tempSortName
                        else:
                            log.error("%s: %r: Missing artist 'sort_name' in XML contents: %s",
                                    PLUGIN_NAME, albumid, releaseXmlNode)
                    else:
                        log.error("%s: %r: Missing 'artist' in XML contents: %s",
                                PLUGIN_NAME, albumid, releaseXmlNode)
                    aCount += 1
                else:
                    log.error("%s: %r: Missing 'name_credit' in XML contents: %s",
                            PLUGIN_NAME, albumid, releaseXmlNode)
            if len(stdArtist) > 0:
                album_metadata["~aaeStdAlbumArtists"] = stdArtist
            if len(credArtist) > 0:
                album_metadata["~aaeCredAlbumArtists"] = credArtist
            if len(sortArtist) > 0:
                album_metadata["~aaeSortAlbumArtists"] = sortArtist
            if aCount > 0:
                album_metadata["~aaeAlbumArtistCount"] = aCount
            # Reset counter
            aCount = 0
            for tPhrase in jPhrase:
                album_metadata["~aaeJoinPhrase_%i" % aCount] = tPhrase
                aCount += 1
        else:
            log.error("%s: %r: Error reading XML contents: %s",
                      PLUGIN_NAME, albumid, releaseXmlNode)
        return None

register_album_metadata_processor(AlbumArtistStdName().add_artist_std_name)
