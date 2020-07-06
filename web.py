import re
from webob import Request,Response
from webob.dec import wsgify
from webob.exc import HTTPNotFound
class AttrDict:
    def __init__(self,d:dict):
        self.__dict__.update(d if isinstance(d,dict) else {})
    def __setattr__(self,key,value):
        raise NotImplementedError
    def __repr__(self):
        return '<AttrDict:{}>'.format(self.__dict__)
    def __len__(self):
        return len(self.__dict__)
class Route:

    PATTNERTABLE = {
        'str': r'[^/]+',
        'word': r'\w+',
        'int': r'[+-]?\d+',
        'float': r'[+-]?\d+\.\d+',
        'any': r'.+'
    }
    TYPECAST = {
        'str': str,
        'word': str,
        'int': int,
        'float': float,
        'any': str
    }
    _regex = re.compile(r'/{([^{}:]+):?([^{}:]*)}')

    def __init__(self, prefix: str = ''):
        self._prefix = prefix.rstrip('/\\')
        self._routetable = []
        self.pre_interceptor = []
        self.post_interceptor = []
    def preinterceptor(self,fn):
        self.pre_interceptor.append(fn)
        return fn
    def postinterceptor(self,fn):
        self.post_interceptor.append(fn)
        return fn
    def _parse(self,src):
        start = 0
        repl = ''
        type = {}
        matcher = self._regex.finditer(src)
        for _, match in enumerate(matcher):
            name = match.group(1)
            t = match.group(2)
            type[name] = self.TYPECAST.get(t, str)
            repl += src[start:match.start()]
            tmp = '/(?P<{}>{})'.format(
                name,
                self.PATTNERTABLE.get(t, self.PATTNERTABLE['str'])
            )
            repl += tmp
            start = match.end()
        else:
            repl += src[start:]
        return repl, type
    def route(self,path,*method):
        def wrapper(handler):
            pattern,trans = self._parse(path)
            self._routetable.append((tuple(map(lambda x:x.upper(),method)),re.compile(pattern),trans,handler))
            return handler
        return wrapper
    def match(self,request):
        if not request.path.startswith(self._prefix): #前缀匹配
            print(request.path)
            return None
        #前置拦截route请求
        for fn in self.pre_interceptor:
            request = fn(request)
            if not request:
                return None

        for method,pattern,trans,handler in self._routetable:
            if not method or request.method in method:
                matcher = pattern.match(request.path.replace(self._prefix,'',1))
                if matcher:
                    newdict = {}
                    for k,v in matcher.groupdict().items():
                        newdict[k] = trans[k](v)
                    request.var = AttrDict(newdict)
                    response =  handler(request)
                for fn in self.post_interceptor:
                    request = fn(request)
                    if not request:
                        return None
                    else:
                        return response
class App:
    _Routable = [] #存储一级对象
    #全局拦截器
    PRE_INTERCEPTOR = []
    POST_INTERCEPTOR = []
    @classmethod
    def regesiter(cls,*routes:Route):
        for route in routes:
            cls._Routable.append(route)
    @classmethod
    def preinterceptoreg(cls,fn):
        cls.PRE_INTERCEPTOR.append(fn)
        return fn
    @classmethod
    def postinterceptoreg(cls,fn):
        cls.POST_INTERCEPTOR.append(fn)
        return fn
    @wsgify
    def __call__(self,request:Request):
        for fn in self.PRE_INTERCEPTOR:
            request = fn(request)
        for route in self._Routable:
            response = route.match(request)
            for fn in self.POST_INTERCEPTOR:
                response = fn(request)
            if response:
                return response
        raise HTTPNotFound





