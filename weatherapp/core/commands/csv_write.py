import csv
# from prettytable import from_csv
from weatherapp.core.abstract import Command


class CsvWrite(Command):
    """ Writing weather data in .csv format.
    """

    name = 'csv_write'

    def __init__(self, app):
        super().__init__(app)
        self.options = self.app.options

    def run(self, argv):
        """ Run command.
        """

        data = []
        for provider in self.app.providermanager._commands.values():
            location = {'location': provider(self).location}
            weather_info = provider(self).run(argv)
            location.update(weather_info)
            data.append(location)

            with open('data_weather.csv', 'wt') as frecord:
                writer = \
                    csv.DictWriter(frecord, fieldnames=list(data[0].keys()))
                writer.writeheader()
                writer.writerows(data)

        self.app.stdout.write('writing completed')
