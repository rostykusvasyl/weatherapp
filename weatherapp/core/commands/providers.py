from weatherapp.core.abstract import Command


class Providers(Command):
    """ Displays all existing providers.
    """

    name = "providers"

    def run(self, argv):
        """ Run command
        """

        for name in self.app.providermanager._commands:
            print(name)