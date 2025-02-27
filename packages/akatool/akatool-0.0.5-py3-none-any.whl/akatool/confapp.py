from csv import reader as __reader__
from sys import argv as _a
import akatool
def loader(f):
    with open(f) as f:
        for res in __reader__(f):
            yield res
core = lambda conf : ([incognito(i) for i in loader(conf)], __import__('subpr').lib.subpr('python -m akatool'))
main = lambda : core(_a[1])
if __name__ == "__main__": main()