'Interactive REPL.'
from .repl import CommandReader
from .scope import Scope
from .util import NoSuchPathException
from traceback import print_exc
import sys

assert NoSuchPathException

def main():
    scope = Scope()
    for command in CommandReader(sys.stdin):
        try:
            scope.execute(command)
        except:
            print_exc(0)

if '__main__' == __name__:
    main()
