"""
Primitive Roots, Indices
"""
from random import randint, choice
from nzmath.arith1 import inverse
from nzmath.equation import e1_ZnZ
from nzmath.factor.methods import factor
from nzmath.gcd import lcm_, gcd_
from nzmath.prime import generator_eratosthenes, randPrime
from nzmath.residue import primitive_root, primRootDef, primRootTakagi
from utils import HitRet

size = 100 # maximum data size, positive integer
length = 10 # maximum data length, positive integer

print("\n===============================================================")
print("By Fermat's theorem, for prime  p > 0  and  a != 0 (mod p), we")
print("have  a**(p-1) == 1 (mod p).  If  a**e != 1 (mod p)  for any")
print("e, 0 < e < p-1, we say  a  is a primitive root modulo  p.")
print("===============================================================")

HitRet()

print("Table of Primitive Roots")
print("========================")
print("We give all primitive roots  mod p  for small  p's.\n")
P = [p for p in generator_eratosthenes(100) if p > 2]
R = {p:primRootDef(p) for p in P}
for p in P:
    print(f"p = {p}  ==>  {len(R[p])}  primitive roots  {R[p]}")

HitRet()

print("Existence of Primitive Roots")
print("============================")
print("Takagi gives a constructive proof of the existence of primitive roots.")
print("That is summarized as a Python function 'cyclotomic.primRootTakagi'")
print("implemented in NZMATH.  You understand its algorithm by reading the")
print("next example together:")

HitRet()

print("Example")
print("=======")
print("For  p = 41, we are going to find a primitive root  a  modulo  p.  Put")
print("I = {1, ..., p-1}  and let  o(x) = min({i for i in I if x**i%p == 1})")
print("for any integer  x  with  GCD(p, x) == 1.")
print("    p = 41; I = set(range(1, p))")
print("    def o(x): return min({i for i in I if x**i%p == 1})")
p = 41; I = set(range(1, p))
def o(x): return min({i for i in I if x**i%p == 1})
print("We search  a  with  o(a) == p-1 == 40.  Let  a = min(I - {1}) == 2")
print("be the first candidate.  Compute  X = {a**i%p for i in I}.  Then  X ==")
print("{1, 2, 4, 5, 8, 9, 10, 16, 18, 20,",
            "21, 23, 25, 31, 32, 33, 36, 37, 39, 40}")
print("and  m = o(a) == len(X) == 20.  Since  m < p-1, we cannot take  a  to")
print("be a primitive root modulo  p.  Hence let  b = min(I - {1} - X) == 3")
print("and compute  n = o(b) == 8.")
print("    a = min(I - {1}); X = {a**i%p for i in I}; m = o(a)")
a = min(I - {1}); X = {a**i%p for i in I}; m = o(a)
print("    b = min(I - {1} - X); n = o(b)")
b = min(I - {1} - X); n = o(b)
print("Take divisors  m0  of  m  and  n0  of  n  so that  l = LCM(m, n) == 40")
print("== m0*n0  with  GCD(m0, n0) = 1 (Sec.4_Prob.11), then  m0 = 5, n0 = 8.")
print("Let now  a**(m//m0)*b**(n//n0)%p  be new  a  again.  Then  o(a) ==")
print("m0*n0 == 40  for  a == 2**(20//5)*3**(8//8)%41 == 16*3%41 == 7.  Hence")
print("a == 7  is a primitive root modulo  p == 41.")
print("    m0 = 5; n0 = 8; a = a**(m//m0)*b**(n//n0)%p")
m0 = 5; n0 = 8; a = a**(m//m0)*b**(n//n0)%p; print(f"a, o(a) == {a}, {o(a)}")

HitRet()

print("Theorem 1.27")
print("============")
print("For prime  p, there exists a primitive root  r  modulo  p, and")
print("        [r**k%p for k in range(p-1)]")
print("is a list of reduced representatives modulo  p.\n")
for _ in range(5):
    p = randPrime(2); r = primRootTakagi(p, p-1)
    print(f"p = {p}, then  r = {r}  and representatives are"); x, X = 1, [1]
    for _ in range(p - 2):
        x = x*r%p; X.append(x)
    print(X); print()

print("Remark")
print("======")
print("For prime  p, the exponent of  r**k  is  (p-1)/GCD(k, p-1), where")
print("    r  is a primitive root modulo  p.\n")
def o(x): return min({i for i in range(1, p) if pow(x, i, p) == 1})
for _ in range(5):
    p = randPrime(2); r = primRootTakagi(p); k = randint(0, p - 2)
    print(f"p = {p}, then the exponent of  r**k == {r}**{k}  is  {o(r**k)}")
    print(f"        while  (p-1)//GCD(k, p-1) == {(p-1)//gcd_(k, p-1)}")

HitRet()

print("Compare Several Methods")
print("=======================")
print("respectively by definition, by Takagi and by factoring  p - 1.\n")
for p in [randPrime(3) for _ in range(20)]:
    x, y, z = primRootDef(p)[randint(0, 2)], \
        primRootTakagi(p, randint(2, 5)), primitive_root(p)
    print(f"p = {p}, then  {x}, {y}, {z}  are primitive roots mod  p")

HitRet()

print("Bijection via Index")
print("=====================")
print("Let  p  be a prime and  r  be a primitive root modulo  p.  Then the map")
print("    Ind: Z - pZ --> Z; r**al == a --> al == Ind(a)")
print("induces a bijection  (Z/p)* --> Z/(p-1)  from the reduced residues")
print("modulo  p  to the residues modulo  p-1.")

HitRet()

print("We generalize the computation of the textbook as a program.")
print("Take and fix a prime number  p  and a primitive root  r  modulo  p.")
p=choice([7,11,13,17,19,23]); r=primRootTakagi(p,randint(2,p-1))#; p = 13; r = 2
print('    p=choice([7,11,13,17,19,23]);r=primRootTakagi(p,randint(2,p-1))')
print(f"prime  p == {p}, primitive root  r == {r}  modulo  p.\n")

print("Do the following preparation in advance:")
TN = [-1]*(p-1); x = r; TI = [1, r]
for _ in range(p-3):
    x = x*r%p; TI.append(x)
for i in range(p-1): TN[TI[i] - 1] = i
def Ind(N): return TN[N%p - 1]
def Pow(I): return TI[I%(p-1)]
print('    TN = [-1]*(p-1); x = r; TI = [1, r]')
print('    for _ in range(p-3):')
print('        x = x*r%p; TI.append(x)')
print('    for i in range(p-1): TN[TI[i] - 1] = i')
print('    def Ind(N): return TN[N%p - 1]')
print('    def Pow(I): return TI[I%(p-1)]')
print("Then we can utilize the facts bellow in our computation:")
print("    r**I==N (mod p) <==> Ind(N)==I (mod p-1) <==> Pow(I)==N (mod p)")
print("    TI==[r**I%p for I in range(p-1)],",
                    "TN==[Ind(N) for N in range(1,p)]")
print("    Pow(I) == TI[I%(p-1)], Ind(N) == TN[N%p -1]")
print("We may also use the next tables  N-->I=Ind(N)  and  I-->N=Pow(I):")
print("-"*(3*p+6)); print(" "*7+"N|{:>2}".format(1),end="")
for i in range(2,p): print("|{:>2}".format(i),end="")
print("|"); print("Ind(N)=I|{:>2}".format(TN[0]),end="")
for i in range(1,p-1): print("|{:>2}".format(TN[i]),end="")
print("|"); print("-"*6+"--+"*p); print(" "*7+"I|{:>2}".format(0),end="")
for i in range(1,p-1): print("|{:>2}".format(i),end="")
print("|"); print("Pow(I)=N|{:>2}".format(TI[0]),end="")
for i in range(1,p-1): print("|{:>2}".format(TI[i]),end="")
print("|"); print("-"*(3*p+6))
print("===============================================================")
print("By this preparation, every computation of index  Ind(N)  or its")
print("inverse  Pow(I)  will be obtained only by looking tables above.")
print("Or, you may be able to quote data in the lists  TN  and  TI.")
print("===============================================================")
HitRet()

print("Example")
print("=======")
print(f"prime  p == {p}, primitive root  r == {r}  modulo  p.")
i = randint(10, 50); n = 0
while not n%p: n = randint(100, 200)
#n = 100; i = 9
print(f"constants  n == {n}, i == {i}.")

HitRet()

print(f"1)  Compute  Ind(n)==Ind(n%p)==Ind({n%p})"+
                f"(==TN[{n%p-1}])=={TN[n%p-1]}  use  TN  or by table.")
print(f"2)  Compute  Ind(-1)==Ind(p-1)==Ind({p-1})"+
                f"=={TN[p-2]}  use  TN  or by table.")
print(f"3)  Solve Ind(N)==i, N==Pow(i%(p-1))"+
                f"==Pow({i%(p-1)})=={TI[i%(p-1)]}  use  TI  or by table.")
print(f"4)  Solve Ind(N)==-1, N==Pow(-1%(p-1))"+
                f"==Pow({-1%(p-1)})=={TI[-1%(p-1)]}  use  TI  or by table.")

HitRet()

print("Theorem 1.28")
print("============")
print("Let  p  be a prime and  r  be a primitive root modulo  p.  Then the")
print("above bijection  Ind: (Z/p)* --> Z/(p-1)  is a homomorphism, so is an")
print("isomorphism from multiplicative to additive cyclic groups of order p-1.")

HitRet()

print("Examples 1, 2, 3")
print("================")
print("Notatons and assumptions being as above, we continue computation.")
a,b,c,d,e,f,g=randint(2,p-1),randint(1,p-1),randint(3,p-1),randint(2,p-1),\
        randint(1,p-1),randint(1,p-1),randint(1,p-1); D=(f*f+4*e*g)%p
while Ind(d)%c or (p-1)%c: c,d=randint(3,p-1),randint(2,p-1)
while D==0 or Ind(D)&1:
    e,f,g=randint(1,p-1),randint(1,p-1),randint(1,p-1); D=(f*f+4*e*g)%p
#a>1,b>0,c>2,d>1,e>0,f>0,g>0;Ind(d)%c==(p-1)%c==0;D=(f*f+4*e*g)%p>0,Ind(D)&1==0
#a, b, c, d, e, f, g = 11, 5, 3, 5, 5, 3, 10

HitRet()
print(f"prime  p == {p}, primitive root  r == {r}  modulo  p.")
print(f"a == {a}, b == {b}, a*b%p > 0.\n")

print(f"E1) Solve  a*x == b (mod p)  <==>  {a}*x == {b} (mod {p}).")
print("  Usually we solve the diophantine equation  a*u + p*v == 1, get")
print("the inverse  u  of  a  modulo  p, a*u == 1 (mod p), and obtain the")
print("answer  x = b*u (mod p).  For example, NZMATH can realize it by the")
print("function 'equation.e1_ZnZ([b,-a],p)' but call 'gcd.extgcd(a,p)' still.")
print(f"Then  x == e1_ZnZ([b,-a],p)[1][0] == {e1_ZnZ([b,-a],p)[1][0]}.")
print("  If we may apply the 'index table' (or the computed lists  TI, TN),")
print("we can solve this problem as follows without extended GCD algorithm:")
print("    Ind(a)+Ind(x)==Ind(b), Ind(x)==Ind(b)-Ind(a) (mod p-1).")
print("    x==Pow(Ind(b)-Ind(a))==TI[(TN[b%p-1]-TN[a%p-1])%(p-1)]")
print(f"     ==TI[(TN[{b%p-1}]-TN[{a%p-1}])%{(p-1)}]"+
            f"==TI[({TN[b%p-1]}-{TN[a%p-1]})%{(p-1)}]"+
            f"==TI[{(TN[b%p-1]-TN[a%p-1])}%{(p-1)}]"+
            f"==TI[{(TN[b%p-1]-TN[a%p-1])%(p-1)}]"+
            f"=={TI[(TN[b%p-1]-TN[a%p-1])%(p-1)]} (mod p).")
x = TI[(TN[b%p - 1] - TN[a%p -1])%(p-1)]
print(f"Really  a*x=={a}*{x}%{p}=={a*x%p}=={b%p}==b (mod {p}).")

HitRet()
print(f"prime  p == {p}, primitive root  r == {r}  modulo  p.")
print(f"c == {c}, d == {d}, c*d%p > 0, Ind(d)%c == (p-1)%c == 0.\n")

print(f"E2) Solve  x**c == d (mod p)  <==>  x**{c} == {d} (mod {p}).")
print("  Solve the equivalent index equation  c*Ind(x) == Ind(d) (mod p-1).")
print("We may apply the above quoted NZMATH function  e1_ZnZ, but we shall")
print(f"directly treat this.  Since  c=={c}  divides  Ind(d)=={Ind(d)}  and")
print(f"p-1=={p-1}, holds  Ind(x) == Ind(d)//c (mod (p-1)//c).  By mod p-1,")
print(f"holds  Ind(x) == Ind(d)//c + i*(p-1)//c for i in range(c) (mod p-1).")
X = [Pow((Ind(d)//c)%((p-1)//c) + i*((p-1)//c)) for i in range(c)]
print(f"So  X = [Pow((Ind(d)//c)%((p-1)//c) + i*((p-1)//c)) for i in range(c)]")
print(f"is the list of solutions")
print(f"    X == {X} (mod {p}).\nReally for x in X:")
for x in X:
    print(f"    x**c-d == {x**c-d} == {(x**c-d)//p}*{p} == (x**c-d)//p*p")
    if (x**c - d)%p:
        raise RuntimeError(f"x**c==d (mod p), (x,c,d,p)={(x,c,d,p)}")

HitRet()
print(f"prime  p == {p}, primitive root  r == {r}  modulo  p.")
print(f"e,f,g=={e,f,g}, e*f*g%p>0, D=(f**2+4*e*g)%p=={D}>0, Ind(D)&1==0.\n")

print(f"E3) Solve e*x**2+f*x-g == 0 (mod p)"+
        f"<==>{e}*x**2+{f}*x-{g} == 0 (mod {p}).")
print(f"  All job will be done by the 'index table' or the lists  TN, TI.")
s = Pow(p-1 - Ind(e)); t = f*s%p; u = g*s%p; T = Pow(p-1 - Ind(-2)); v = T*t
print(f"Since  p > 2  and  D  is non-zero square, this has 2 distinct roots.")
print(f"Multiply the both sides of equation by  s = Pow(p-1 - Ind(e)) == {s},")
print(f"i.e. the inverse of e mod p.  The equation is x**2 + t*x - u == 0")
print(f"(mod p) now, and is monic, where  t = f*s%p == {t}, u = g*s%p == {u}.")
print(f"Let  T  be the inverse of  -2  mod p, namely  -2*T == 1 (mod p), and")
print(f"put v=T*t=={v}.  Then (x - v)**2 == v**2 + u (mod p), so 2*Ind(x - v)")
print(f"== Ind(v**2 + u) (mod p-1).  Further  Ind(x - v) == Ind(v**2 + u)//2")
print(f"or Ind(v**2 + u)//2 + (p-1)//2 (mod p-1).  Consequently, we obtained")
print(f"x - v == Pow(Ind(v**2 + u)//2)  or  Pow(Ind(v**2 + u)//2 + (p-1)//2)")
print(f"(mod p).  So, x == {Pow(Ind(v**2 + u)//2) + v}  or  "+
                f"{Pow(Ind(v**2 + u)//2 + (p-1)//2) + v} (mod p).",end="  ")
X = [(Pow(Ind(v**2 + u)//2) + v)%p, (Pow(Ind(v**2 + u)//2 + (p-1)//2) + v)%p]
print(f"Finally, x == {X[0]} or {X[1]} (mod {p}).")
print(f"Actually  {e}*{X[0]}**2 + {f}*{X[0]} - {g} "+
        f"== {(e*X[0]**2 + f*X[0] - g)%p}, {e}*{X[1]}**2 + {f}*{X[1]} - {g} "+
        f"== {(e*X[1]**2 + f*X[1] - g)%p} (mod {p}).")

HitRet()

