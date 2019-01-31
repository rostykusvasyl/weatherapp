def integers(num=5):
    """Infinite sequence of integers.
    : num - step(integer number)
    """
    i = 0
    while True:
        yield i
        i += num


def take(stop, seq):
    """Returns first n values from the given sequence."""
    seq = iter(seq)
    try:
        while True:
            res = next(seq)
            if res <= stop:
                print(res)
            else:
                break
    except StopIteration:
        pass


take(10000, integers())
