""" An iterator that generates a sequence of numbers from 0 to
a given number increasing each number by a given value.
"""


class AddNumber:
    """ Simple iterator
    """

    def __init__(self, num=1, stop=100):
        self.num = num
        self.stop = stop

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n <= self.stop:
            result = self.n
            self.n += self.num
            return result
        else:
            raise StopIteration

for n in AddNumber():
    print(n)
