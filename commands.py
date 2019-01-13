""" App commamds
"""

from pathlib import Path
from abstract import Command
import config


class Configurate(Command):
    """ Help to configurate weather providers.
    """

    name = "configurate"

    def get_parser(self):
        """ Initialize argument parser for command.
        """

        parser = super(Configurate, self).get_parser()
        parser.add_argument("provider", help="Provider name")
        return parser

    def run(self, argv):
        """ Run command
        """

        parsed_args = self.get_parser().parse_args(argv)
        provider_name = parsed_args.provider
        provider_factory = self.app.providermanager.get(provider_name)
        provider_factory(self.app).configurate()


class Providers(Command):
    """ Displays all existing providers.
    """

    name = "providers"

    def run(self, argv):
        """ Run command
        """

        for name in self.app.providermanager._commands:
            print(name)


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
