#!/usr/bin/env python

import re

class dummy(object):
    pass

class Router():
    def __init__(self, hooks, states):
        self.hooks=hooks
        self.states=states
        self.routes={}

    def dispatch(self, ctx, **wargs):
        #print '-->', ctx, wargs
        for _jid, _hook, _status in [(ctx.jid, ctx.hook, ctx.state),
                                     (None, ctx.hook,  ctx.state),
                                     (ctx.jid, None, ctx.state),
                                     (ctx.jid, ctx.hook, None),
                                     (None, None, ctx.state),
                                     (None, ctx.hook, None),
                                     (ctx.jid, None, None),
                                     (None, None,None)]:
            for pattern, fn in self.routes.get((_jid, _hook, _status),[]):
                if not pattern:
                    return fn(ctx, **wargs)
                m=pattern.search(ctx.message or '')
                if m:
                    ctx.matches=m.groups()
                    for k,v in m.groupdict().items():
                        ctx.__dict__[k]=v
                    return fn(ctx, **wargs)

    def __call__(self, pattern=None, hooks=[None], states=[None], jids=[None]):
        # registers the function with the route
        def decor(func):
            #def wrapper(*args,**wargs):
            #    tmp=func(*args,**wargs)
            #    #print '<--', tmp
            #    return tmp
            # register route
            for hook in hooks:
                for state in states:
                    for jid in jids:
                        if not (jid, hook, state) in self.routes:
                            self.routes[(jid, hook, state)]=[]
                        #self.routes[(jid, hook, state)].append((re.compile(pattern), wrapper))
                        self.routes[(jid, hook, state)].append((re.compile(pattern) if pattern else None, func))
            #return wrapper
            return func
        return decor

def test():
    hooks=['hook-otr-start', 'hook-post-message-in', 'hook-otr-smp']
    states=['fetchsmp', 'start']
    router=Router(hooks,states)

    @router(pattern="asdf")
    def asdf(route):
        return 'asdf'

    @router(pattern="qwer")
    def qwer(route):
        return 'qwer'

    @router(pattern="qwer", hooks=['hook-otr-start', 'hook-post-message-in'], states=['fetchsmp'])
    def zxcv(route):
        return 'zxcv', route.msg

    @router(pattern="zxcv(?P<no>..)-(?P<nx>..)", hooks=['hook-otr-start', 'hook-post-message-in'], states=['fetchsmp'])
    def zaq(route):
        return 'zaq', route.nx

    @router(pattern="asdf(?P<no>..)-(?P<nx>..)", hooks=['hook-otr-start', 'hook-post-message-in'], states=['fetchsmp'])
    def csw(route):
        return 'csw', route.nx

    import pprint
    pprint.pprint(router.routes)

    assert router.dispatch(msg='xxxasdfxxx') == 'asdf'
    assert router.dispatch(msg='xxxasdf') == 'asdf'
    assert router.dispatch(msg='xxxasd') == None
    assert router.dispatch(msg='asdfxxx') == 'asdf'
    assert router.dispatch(msg='aqwerxx') == 'qwer'
    assert router.dispatch(hook='juheee') == None
    assert router.dispatch(msg='aqwerxx', hook='hook-otr-start', status='fetchsmp') == ('zxcv', 'aqwerxx')
    assert router.dispatch(msg='aqwerxx', hook='hook-otr-start', status='fetch') == 'qwer'
    assert router.dispatch(msg='aqwerxx', hook='hook-post-message-in', status='fetch') == 'qwer'
    assert router.dispatch(msg='aqwerxx', hook='hook-post-message-in', status='fetchsmp') == ('zxcv', 'aqwerxx')
    assert router.dispatch(msg='azxcvxx-yy', hook='hook-post-message-in', status='fetchsmp') == ('zaq', 'yy')
    assert router.dispatch(msg='azxcvxxyy', hook='hook-post-message-in', status='fetchsmp') == None
    assert router.dispatch(msg='aasdfxx-yy', hook='hook-post-message-in', status='fetchsmp') == ('csw', 'yy')
    assert router.dispatch(msg='aasdfxx-yy', hook='hook-post-message-in', status='fetchsmp') == ('csw', 'yy')
    assert router.dispatch(msg='aasdfxxyy', hook='hook-post-message-in', status='fetchsmp') == 'asdf'

if __name__ == "__main__":
    test()
