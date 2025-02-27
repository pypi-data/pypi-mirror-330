from .util import popattr, UnparseNoSuchPathException
from collections import namedtuple
from itertools import islice
import heapq

def resolvedscopeornone(s, path):
    for name in path:
        r = s.resolvableornone(name)
        if r is None:
            return
        s = r.resolve(s)
        if not hasattr(s, 'resolvableornone'):
            return
    return s

class Address(namedtuple('BaseAddress', 'scope key')): pass

class Hit(namedtuple('BaseHit', 'depths address resolvable')):

    def naiveresolve(self):
        return self.resolvable.resolve(self.address.scope) # XXX: Wise?

    def iterornone(self, word):
        contextscope = self.naiveresolve()
        if hasattr(contextscope, 'resolvableornone'):
            return Iterator(self.depths, contextscope, word)

    def shortcut(self, zerocount):
        return all(not d for d in islice(self.depths, len(self.depths) - zerocount, None))

class Iterable:

    def __iter__(self):
        return self.popiterator()

class Iterator(Iterable):

    def __init__(self, depths, contextscope, word):
        def g():
            for depth, scopes in enumerate(contextscope.scopedepths()):
                for scope in scopes:
                    resolvable = scope.resolvableornone(word)
                    if resolvable is not None:
                        yield Hit(depths + [depth], Address(scope, word), resolvable)
        self.iterator = g()

    def next(self):
        return next(self.iterator)

    def popiterator(self):
        return popattr(self, 'iterator')

class Merge(Iterable):

    def __init__(self):
        self.iterables = []

    def add(self, iterable):
        self.iterables.append(iterable)

    def popiterator(self):
        return heapq.merge(*popattr(self, 'iterables'))

def _lt(*depthspair):
    for d1, d2 in zip(*map(reversed, depthspair)):
        if d1 < d2:
            return True
        if d1 > d2:
            break

class Sump:

    besthit = None

    def add(self, iterable):
        pass

    def offer(self, hit):
        if self.besthit is None or _lt(hit.depths, self.besthit.depths):
            self.besthit = hit

    def __iter__(self):
        if self.besthit is not None:
            yield self.besthit

class Query:

    def __init__(self, path):
        assert path
        self.path = path

    def search(self, scope):
        root = Iterator([], scope, self.path[0])
        size = len(self.path)
        if 1 == size:
            for hit in root:
                return hit
        else:
            merges = [root]
            for _ in range(size - 2):
                merges.append(Merge())
            sump = Sump()
            merges.append(sump)
            for cursor, merge in enumerate(merges):
                xs = range(cursor + 1, size)
                for hit in sump:
                    if hit.shortcut(len(xs)):
                        return hit
                for hit in merge:
                    for x in xs:
                        i = hit.iterornone(self.path[x])
                        if i is None:
                            break
                        try:
                            hit = i.next()
                        except StopIteration:
                            break
                        merges[x].add(i)
                    else:
                        if hit.shortcut(len(xs)):
                            return hit
                        sump.offer(hit)
        raise UnparseNoSuchPathException(self.path)
