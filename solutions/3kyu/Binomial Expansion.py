import re

P = re.compile(r'\((-?\d*)(\w)\+?(-?\d+)\)\^(\d+)')

def expand(expr):
    a,v,b,e = P.findall(expr)[0]
    
    if e=='0': return '1'
    
    o   = [int(a!='-' and a or a and '-1' or '1'), int(b)]
    e,p = int(e), o[:]
    
    for _ in range(e-1):
        p.append(0)
        p = [o[0] * coef + p[i-1]*o[1] for i,coef in enumerate(p)]
    
    res = '+'.join(f'{coef}{v}^{e-i}' if i!=e else str(coef) for i,coef in enumerate(p) if coef)
    
    return re.sub(r'\b1(?=[a-z])|\^1\b', '', res).replace('+-','-')