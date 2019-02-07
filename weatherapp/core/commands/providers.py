from weatherapp.core.abstract import Command


class Providers(Command):
    """ Displays all existing providers.
    """

    name = "providers"

    def run(self, argv):
        """ Run command
        """

        for name, provider in self.app.providermanager:
            self.app.stdout.write('{} \n'.format(name))
