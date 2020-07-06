import re
PATTNERTABLE = {
    'str' : r'[^/]+',
    'word' : r'\w+',
    'int' : r'[+-]?\d+',
    'float' : r'[+-]?\d+\.\d+',
    'any' : r'.+'
}
TYPECAST = {
    'str' : str,
    'word' : str,
    'int' : int,
    'float' : float,
    'any' : str
}
s = [
    '/student/{name:str}/xxx/{id:int}',
    '/student/xxx/{id:int}/yyy',
    '/student/xxx/5134324',
    '/student/{name:}/xxx/{id}',
    '/student/{name:}/xxx/{id:aaa}'
]
regex = re.compile(r'/{([^{}:]+):?([^{}:]*)}')

def parse(src):
    start = 0
    repl = ''
    type = {}
    matcher = regex.finditer(src)
    for _,match in enumerate(matcher):
        name = match.group(1)
        t = match.group(2)
        type[name] = TYPECAST.get(t,str)
        repl += src[start:match.start()]
        tmp = '/(?P<{}>{})'.format(
            name,
            PATTNERTABLE.get(t,PATTNERTABLE['str'])
        )
        repl += tmp
        start = match.end()
    else:
        repl += src[start:]
    return repl,type

k,v = parse( '/student/{name:str}/xxx/{id:int}')
print(v)