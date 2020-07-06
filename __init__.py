from webob import Request,Response
from .template import render
from .web import Route,App
idx = Route()
world = Route('/world')
App.regesiter(world,idx)
def ip(request:Request):
    if not request.remote_addr.startswith('192.'):
        return None
    else:
        return request
@world.route(r'/{world:str}')
def worldhandler(request):
    print(request.var)

    return "hello human"
@idx.route(r'')
def indexhandler(Request):
    user =[
        'bob',
        'james',
        'kevin'
    ]
    d = {'user' : user}
    render('index.html',d)