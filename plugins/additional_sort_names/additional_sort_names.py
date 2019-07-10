PLUGIN_NAME = "Sort Names"
PLUGIN_AUTHOR = "David Kellner"
PLUGIN_DESCRIPTION = """Provides the artist sort names for writers and lyricists. Values are available as <code>_writersort</code> and <code>_lyricistsort</code>, e.g. for usage in a script like this one:
<pre>
$copymerge(composer,writer)
$copymerge(composersort,_writersort)
$unset(writer)
</pre>"""
PLUGIN_VERSION = "0.1"
PLUGIN_API_VERSIONS = ["2.0"]

from picard.metadata import register_track_metadata_processor


def provide_sortnames(album, metadata, track, release):
    writersort = []
    lyricistsort = []
    for trackrel in track["recording"]["relations"]:
        if trackrel["type"] == "performance":
            for workrel in trackrel["work"]["relations"]:
                if workrel["type"] == "writer":
                    writersort.append(workrel["artist"]["sort-name"])
                elif workrel["type"] == "lyricist":
                    lyricistsort.append(workrel["artist"]["sort-name"])
    metadata["~writersort"] = writersort
    metadata["~lyricistsort"] = lyricistsort


register_track_metadata_processor(provide_sortnames)
