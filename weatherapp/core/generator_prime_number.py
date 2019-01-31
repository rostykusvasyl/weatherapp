""" Generator prime number
"""

def integers(stop):
    i = 0
    while i <= stop:
        yield i
        i += 1


for n in iter(integers(stop=101)):
    if n >= 2:
        for k in range(2, n):
            if n % k == 0:
                break
        else:
            print(n)
