"""
Primitive Roots and Power Residues.
"""
from nzmath.arith1 import product as prod
from nzmath.factor.methods import factor
from nzmath.factor.misc import FactoredInteger

def primRootDef(p):
    """
    Input
        p: prime number  p > 2
    Output
        R: the list of primitive roots  r  modulo  p, 1 < r < p
    """
    R = []
    for r in range(2, p):
        x = r
        for _ in range(3, p):
            x = x*r%p
            if x == 1: break
        else: R.append(r)
    return R

def primitive_root(p):
    """
    Return a primitive root of p.
    """
    pd = FactoredInteger(p - 1).proper_divisors()
    for i in range(2, p):
        for d in pd:
            if pow(i, (p - 1)//d, p) == 1: break
        else: return i

def primRootTakagi(p, a = 2):
    """
    Input
        p: prime number, p > 2
        a: initial integer, 1 < a < p
    Output
        a: primitive root modulo  p.
    """
    x = a; X = {a}
    while x > 1:
        x = x*a%p; X.add(x)
    m = len(X) # X = <a> order m
    while m < p - 1:
        b = min(set(range(1, p)) - X); x = b; n = 1
        while x > 1:
            x = x*b%p; n += 1 # <b> order n
        md, nd = dict(factor(m)), dict(factor(n))
        m0d = {p:md[p] for p in md if p not in nd or md[p] >= nd[p]}
        n0d = {p:nd[p] for p in nd if p not in md or md[p] < nd[p]}
        m0, n0 = prod(p**m0d[p] for p in m0d), prod(p**n0d[p] for p in n0d)
        a = a**(m//m0)%p*b**(n//n0)%p; m = m0*n0; x = a; X = {a}
        while x > 1:
            x = x*a%p; X.add(x)
    return a

