from .model import Stream
from .search import resolvedscopeornone
import os, sys, unicodedata

def acceptdirectivename(word):
    return word and unicodedata.category(word[0])[0] in 'PS'

def prime(d):
    def pd(prefix, suffix, scope):
        if not prefix.directives:
            return d(prefix, suffix, scope)
    return pd

def colon(prefix, suffix, scope):
    'Ignore rest of logical line.'
    return prefix

@prime
def _redirect(prefix, suffix, scope):
    scope['stdout',] = Stream(suffix.tophrase().resolve(scope).openable(scope).open(True))

@prime
def _write(prefix, suffix, scope):
    scope.resolved('stdout').flush(suffix.tophrase().resolve(scope).textvalue)

@prime
def source(prefix, suffix, scope):
    'Include path or resource at prefix.'
    # XXX: Use full algo to get phrasescope?
    phrasescope = scope
    for word in prefix.topath(scope):
        s = resolvedscopeornone(phrasescope, [word])
        if s is None:
            break
        phrasescope = s
    suffix.tophrase().resolve(phrasescope).openable(phrasescope).source(scope, prefix)

@prime
def _cd(prefix, suffix, scope):
    scope['cwd',] = suffix.tophrase().resolve(scope).openable(scope)

@prime
def _test(prefix, suffix, scope):
    sys.stderr.write(str(suffix.tophrase().resolve(scope)))
    sys.stderr.write(os.linesep)

@prime
def equals(prefix, suffix, scope):
    'Assign expression to path.'
    scope[prefix.topath(scope)] = suffix.tophrase()

@prime
def colonequals(prefix, suffix, scope):
    'Evaluate expression and assign result to path.'
    path = prefix.topath(scope)
    scope[path] = suffix.tophrase().resolve(scope.getorcreatesubscope(path[:-1]))

@prime
def plusequals(prefix, suffix, scope):
    'Assign expression to prefix plus an opaque key, i.e. add to list.'
    from .functions import OpaqueKey
    phrase = suffix.tophrase()
    scope[prefix.topath(scope) + (OpaqueKey(),)] = phrase

@prime
def _cat(prefix, suffix, scope):
    scope = scope.getorcreatesubscope(prefix.topath(scope))
    scope.resolved('stdout').flush(suffix.tophrase().resolve(scope).openable(scope).processtemplate(scope).textvalue)

def coredirectives():
    yield ':', colon
    yield '!redirect', _redirect
    yield '!write', _write
    yield '.', source
    yield '!cd', _cd
    yield '!test', _test
    yield '=', equals
    yield ':=', colonequals
    yield '+=', plusequals
    yield '<', _cat
