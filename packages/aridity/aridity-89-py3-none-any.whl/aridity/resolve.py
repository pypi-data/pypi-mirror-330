from .search import Query
from .util import CycleException, NoSuchPathException, TreeNoSuchPathException
from itertools import chain

def _slices(path):
    yield path
    limit = len(path) + 1
    for k in range(1, limit):
        for i in range(limit - k):
            yield path[:i] + path[i + k:]

class BaseResolveContext:

    @property
    def label(self):
        return self.leafscope().label

    @property
    def parents(self):
        return self.leafscope().parents

    @property
    def resolvables(self):
        return self.leafscope().resolvables

    def createchild(self, **kwargs):
        return self.leafscope().createchild(**kwargs)

    def getresolvecontext(self):
        return self

    def resolvableornone(self, key):
        return self.leafscope().resolvableornone(key)

    def resolved(self, *path, **kwargs):
        return self.resolvedimpl(path, kwargs) if path else self.leafscope()

    def staticscope(self):
        return self.leafscope().staticscope()

class AnchorResolveContext(BaseResolveContext):

    def __init__(self, anchorscope):
        self.anchorscope = anchorscope

    def leafscope(self):
        return self.anchorscope

    def resolvedimpl(self, path, kwargs):
        hit = Query(path).search(self.anchorscope)
        return hit.resolvable.resolve(ResolveContext(self.anchorscope, path, [hit.address]), **kwargs)

class ResolveContext(BaseResolveContext):

    @classmethod
    def _of(cls, *args):
        return cls(*args)

    def __init__(self, anchorscope, exprpath, addresses):
        self.anchorscope = anchorscope
        self.scopepath = exprpath[:-1]
        self.exprpath = exprpath
        self.addresses = addresses

    def leafscope(self):
        return Query(self.scopepath).search(self.anchorscope).naiveresolve() if self.scopepath else self.anchorscope # XXX: Is naiveresolve correct here?

    def resolvedimpl(self, path, kwargs):
        errors = []
        for prefix in _slices(self.scopepath):
            try:
                hit = Query(list(chain(prefix, path))).search(self.anchorscope)
                if hit.address in self.addresses: # XXX: Could it be valid to resolve the same address recursively with 2 different contexts?
                    raise CycleException(path)
            except NoSuchPathException as e:
                errors.append(e)
                continue
            try:
                return hit.resolvable.resolve(self._of(self.anchorscope, list(chain(self.scopepath, path)), self.addresses + [hit.address]), **kwargs)
            except NoSuchPathException as e:
                errors.append(e)
                break # XXX: Or continue?
        raise TreeNoSuchPathException(self.exprpath, errors)
