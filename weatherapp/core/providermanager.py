""" Module container for providers.
"""
import logging
from weatherapp.core.providers import accuprovider, rp5provider,\
    sinoptikprovider
from weatherapp.core import commandmanager


class ProviderManager(commandmanager.CommandManager):
    """ Discovers registered providers and loads them.
    """

    logger = logging.getLogger(__name__)

    def _load_commands(self):
        """ Loads all existing providers.
        """

        for provider in [accuprovider.AccuProvider, rp5provider.Rp5Provider,
                         sinoptikprovider.SinoptikProvider]:
            self.add(provider.name, provider)
