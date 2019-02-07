import unittest

from weatherapp.core.commandmanager import CommandManager


class DummyCommand:
    name = 'dummycommand'
    pass


class DummyClearCache:
    name = 'dummyclear'
    pass

class CommandManagerTestCase(unittest.TestCase):

    """ Unit test case for command manager.
    """
    def setUp(self):
        self.command_manager = CommandManager()

    def test_add(self):
        """ Test add method for command manager.
        """

        self.command_manager.add('dummy', DummyCommand)

        self.assertTrue('dummy' in self.command_manager._commands)
        self.assertEqual(self.command_manager.get('dummy'), DummyCommand)

    def test_get(self):
        """ Test application get method."""

        self.command_manager.add('dummy', DummyCommand)

        self.assertEqual(self.command_manager.get('dummy'), DummyCommand)
        self.assertIsNone(self.command_manager.get('bar'))

    def test_contains(self):
        """ Test if '__contains__' method is working.
        """

        self.command_manager.add('dummy', DummyCommand)

        self.assertTrue('dummy' in self.command_manager)
        self.assertFalse('bar' in self.command_manager)

    def test_iter(self):
        """ Test application for __iter__ method.
        """

        self.assertTrue(iter(self.command_manager._commands))

    def test_load_commands(self):
        """ Test application for _load_commands method.
        """
        for command in [DummyCommand, DummyClearCache]:
            self.command_manager.add(command.name, command)

        self.assertTrue(self.command_manager._commands['dummycommand'])
        self.assertTrue(self.command_manager._commands['dummyclear'])


if __name__ == '__main__':
    unittest.main()
