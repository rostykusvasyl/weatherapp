import prettytable
from weatherapp.core.abstract import Formatter
from weatherapp.core import app


class TableFormatter(Formatter):
    """ Table formatter for app output.
    """

    name = 'table'

    def __init__(self):
        self.app = app.App()

    def emit(self, column_names, data):
        """ Format and print data from the iterable source.

        :param column_names: names of the columns
        :type column_names: list
        :param data: iterable data source, one tuple per object
                     with values in order of column names
        :type data: list or tuple

        """

        options = self.app.arg_parser.parse_args()
        pt = prettytable.PrettyTable()

        for column, values in zip(column_names, (data.keys(), data.values())):
            if any(values):
                pt.add_column(column, list(values))

        if options.align:
            pt.align = options.align

        if options.padding_width:
            pt.padding_width = options.padding_width

        if options.vertical_char:
            pt.vertical_char = options.vertical_char

        if options.horizontal_char:
            pt.horizontal_char = options.horizontal_char

        if options.set_style == 'MSWORD_FRIENDLY':
            pt.set_style(prettytable.MSWORD_FRIENDLY)
            print(pt.get_string())
        elif options.set_style == 'PLAIN_COLUMNS':
            pt.set_style(prettytable.PLAIN_COLUMNS)
            print(pt.get_string())
        elif options.set_style == 'RANDOM':
            pt.set_style(prettytable.RANDOM)
            print(pt.get_string())
        else:
            print(pt.get_string())
