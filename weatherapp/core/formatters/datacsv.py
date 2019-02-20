import csv
from prettytable import from_csv
from weatherapp.core.abstract import Formatter


class CsvFormatter(Formatter):
    """ Format and print data from table data in a comma separated values
        file (.csv).
    """

    name = 'csvtable'

    def emit(self, column_names, data):
        """ Format and print data from the iterable source.

        :param column_names: names of the columns
        :type column_names: list
        :param data: iterable data source, one tuple per object
                     with values in order of column names
        :type data: list or tuple

        """

        datacsv = []

        location = {column_names[0]: column_names[1]}
        location.update(data)
        datacsv.append(location)

        with open('data_weather.csv', 'wt') as frecord:
            writer = \
                csv.DictWriter(frecord, fieldnames=list(datacsv[0].keys()))
            writer.writeheader()
            writer.writerows(datacsv)
        with open("data_weather.csv", "r") as fp:
            x = from_csv(fp)
            x.align = "c"
            x.padding_width = 0
        print(x)
