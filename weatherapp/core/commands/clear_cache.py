from pathlib import Path

from weatherapp.core.abstract import Command
from weatherapp.core import config


class ClearCache(Command):
    """ Remove cache directory.
    """

    name = "clear_cache"

    def run(self, argv):
        """ Run command
        """

        cache_dir = Path.home() / config.CACHE_DIR
        if cache_dir.exists():
            for current_file in cache_dir.iterdir():
                # To delete a folder you must first delete all the files inside
                current_file.unlink()
            cache_dir.rmdir()
        self.app.stdout.write('deletion complete')
