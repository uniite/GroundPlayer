from django.db import models
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
import os
import time


# Maps Song fields to metadata fields from mutagen
# in the format {song_field_name: mutagen_field_name}
SONG_METADATA_MAPPING = {
    "title": "title",
    "artist": "artist",
    "album": "album",
    "genre": "genre",
    "album_artist": "album artist",
    "track_number": "tracknumber",
    "year": "date",
}

class Song(models.Model):
    title = models.CharField(max_length=50)
    artist = models.CharField(max_length=50)
    album = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    album_artist = models.CharField(max_length=50)
    track_number = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    bitrate = models.IntegerField(blank=True, null=True)
    format = models.CharField(max_length=20)
    play_count = models.IntegerField(blank=True, null=True)
    last_played = models.IntegerField(blank=True, null=True)
    last_updated = models.IntegerField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    file_last_modified = models.IntegerField(blank=True, null=True)
    file_path = models.TextField()
    file_path_hash = models.CharField(max_length=40)
    
    def update_from_file(self):
        # Figure out which metadata parser we need to use, and do format-specific parsing
        if self.file_path.endswith(".mp3"):
            self.format = "MP3"
            metadata = MP3(self.file_path, ID3=EasyID3)
            self.bitrate = metadata.info.bitrate / 1000
        elif self.file_path.endswith(".flac"):
            self.format = "FLAC"
            metadata = FLAC(self.file_path)
            info = metadata.info
            self.bitrate = info.bits_per_sample * info.sample_rate * info.channels / 1000
        # If the file format is unrecognized, ignore it
        else:
            return False
        # Get whatever metadata we can from the file
        for self_key, meta_key in SONG_METADATA_MAPPING.iteritems():
            # Skip over any problematic fields
            try:
                # The year field is an annoying special case;
                # metadata["date"] can be in the format "20110" or "2011-00-00"
                if self_key == "year":
                    setattr(self, self_key, int(metadata[meta_key][0][:4]))
                # Track number is another of these cases;
                # metadata["tracknumber"] can be "1" or "1/4"
                elif self_key == "track_number":
                    setattr(self, self_key, int(metadata[meta_key][0].split("/", 2)[0]))
                elif meta_key in metadata:
                    setattr(self, self_key, metadata[meta_key][0])
            except Exception, e:
                print e
        # Update our timestamps
        self.last_updated = time.time()
        self.file_last_modified = os.path.getmtime(self.file_path)
        return True
