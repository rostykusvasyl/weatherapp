import prettytable
from weatherapp.core.abstract import Formatter


class TableFormatter(Formatter):
    """ Table formatter for app output.
    """

    name = 'table'

    def emit(self, column_names, data):
        """ Format and print data from the iterable source.

        :param column_names: names of the columns
        :type column_names: list
        :param data: iterable data source, one tuple per object
                     with values in order of column names
        :type data: list or tuple

        """

        pt = prettytable.PrettyTable()

        for column, values in zip(column_names, (data.keys(), data.values())):
            if any(values):
                pt.add_column(column, list(values))

        pt.align = 'l'
        pt.padding_width = 1
        print(pt.get_string())
