from celery.task import Task
from celery.registry import tasks
from models import Song
import os
import time




class ScanMediaTask(Task):

    def run(self, path, raise_errors=False):
        state = {
            "scanned": 0,
            "tagged": 0
        }
        self.raise_errors = raise_errors
        os.path.walk(path, self.scan_path, state)

    def scan_path(self, state, dir, files):
        """
        Scan the given list of files in the given directory
        for new media and updated metadata.
        """

        print dir
        # Go through each of the files...
        for file_name in files:
            # Figure out where on the filesystem it is
            file_path = os.path.join(dir, file_name)
            # Update our scanned file count before anything bad happens
            state["scanned"] += 1
            # From this point on, any number of errors can occur
            try:
                song = Song(file_path=file_path)
                # Only save the Song if the update went OK
                if song.update_from_file():
                    song.save()
            except Exception, e:
                if self.raise_errors:
                    raise
                else:
                    print "Error %s while processing file %s" % (e, file_path)

tasks.register(ScanMediaTask)
