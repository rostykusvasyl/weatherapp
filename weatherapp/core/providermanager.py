""" Module container for providers.
"""


import logging
import pkg_resources
from weatherapp.core import config
from weatherapp.core import commandmanager


class ProviderManager(commandmanager.CommandManager):
    """ Discovers registered providers and loads them.
    """

    logger = logging.getLogger(__name__)

    def _load_commands(self):
        """ Loads all existing providers.
        """

        # for provider in [accuprovider.AccuProvider, rp5provider.Rp5Provider,
        #                  sinoptikprovider.SinoptikProvider]:
        #     self.add(provider.name, provider)
        entry_points = pkg_resources.iter_entry_points(
            config.PROVIDER_EP_NAMESPACE)
        for entry_point in entry_points:
            self.logger.debug('found provider %r', entry_point.name)
            self._commands[entry_point.name] = entry_point.load()
