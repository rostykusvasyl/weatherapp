""" Module container for providers.
"""

from providers import AccuProvider, Rp5Provider, SinoptikProvider

import commandmanager


class ProviderManager(commandmanager.CommandManager):
    """ Discovers registered providers and loads them.
    """

    def _load_commands(self):
        """ Loads all existing providers.
        """

        for provider in [AccuProvider, Rp5Provider, SinoptikProvider]:
            self.add(provider.name, provider)
