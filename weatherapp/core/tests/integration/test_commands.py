import unittest
import io

from weatherapp.core.app import App


class CommandsTestCase(unittest.TestCase):

    """ Test case for commands tests.
    """

    def setUp(self):
        self.stdout = io.StringIO()

    def test_providers(self):
        """ Test providers command.
        """
        App(stdout=self.stdout).run(['providers'])
        self.stdout.seek(0)
        self.assertEqual(self.stdout.read(), 'accu \nrp5 \nsinoptik \n')

    def test_clearcache(self):
        """ Test clear_cache command.
        """
        App(stdout=self.stdout).run(['clear_cache'])
        self.stdout.seek(0)
        self.assertEqual(self.stdout.read(), 'Deletion completed! \n')

    def test_csvwrite(self):
        """ Test csv_write command.
        """
        App(stdout=self.stdout).run(['csv_write'])
        self.stdout.seek(0)
        self.assertEqual(self.stdout.read(), 'Writing completed!\n')
