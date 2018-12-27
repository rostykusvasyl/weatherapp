''' Module container for providers.
'''

from providers import AccuProvider, Rp5Provider, SinoptikProvider


class ProviderManager(object):
    ''' Discovers registered providers and loads them.
    '''

    def __init__(self):
        self._providers = {}
        self._load_providers()

    def _load_providers(self):
        ''' Loads all existing providers.
        '''

        for provider in [AccuProvider, Rp5Provider, SinoptikProvider]:
            self.add(provider.name, provider)

    def add(self, name, provider):
        ''' Add new provider by name.
        '''

        self._providers[name] = provider

    def get(self, name):
        ''' Get provider by name.
        '''
        return self._providers.get(name, None)

    def __len__(self):
        return len(self._providers)

    def __contains__(self, name):
        return name in self._providers

    def __getitem__(self, name):
        return self._providers[name]
