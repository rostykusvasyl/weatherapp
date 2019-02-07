import unittest

from weatherapp.core.providermanager import ProviderManager


class DummyProvider:
    pass


class ProviderManagerTestCase(unittest.TestCase):

    """ Unit test case for ProviderManager manager.
    """

    def setUp(self):
        self.provider_manager = ProviderManager()

    def test_add(self):
        """ Test add method for provider manager.
        """

        self.provider_manager.add('provider', DummyProvider)

        self.assertTrue('provider' in self.provider_manager._commands)
        self.assertEqual(self.provider_manager.get('provider'), DummyProvider)

    def test_get(self):
        """ Test application get method."""

        self.provider_manager.add('provider', DummyProvider)

        self.assertEqual(self.provider_manager.get('provider'), DummyProvider)
        self.assertIsNone(self.provider_manager.get('bar'))

    def test_contains(self):
        """ Test if '__contains__' method is working.
        """

        self.provider_manager.add('provider', DummyProvider)

        self.assertTrue('provider' in self.provider_manager)
        self.assertFalse('bar' in self.provider_manager)


if __name__ == '__main__':
    unittest.main()
