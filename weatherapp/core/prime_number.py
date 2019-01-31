class PrimeNumber:
    """ An iterator that generates primes to a given number.
    """

    def __init__(self, num=2, stop=101):
        self.num = num
        self.stop = stop

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n <= self.stop:
            result = self.n + self.num
            self.n += 1
            return result
        else:
            raise StopIteration


for n in PrimeNumber(stop=101):
    for i in range(2, n):
        if n % i == 0:
            break
    else:
        print(n)
