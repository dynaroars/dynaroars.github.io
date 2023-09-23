import common as CM
from iconstructs import Assignment, Conditional, Break, While
from iconstructs import Formula, FBool, FExp, FAnd, FOr


# from sage.all import *

def wp(S, Q, L, verbose=1):
    """
    Generates weakest precondition using backward propagation.
    S is a list of statements (formulas), Q is the post-condition, L 
    collects the results obtained so far.
    
    sage: print wp(S=[Assignment(x,x+1000)],Q=FExp(x>=100),L=[],verbose=0)[0]
    x + 900 >= 0

    sage: var('y b1 b2 a1')
    (y, b1, b2, a1)

    sage: rs = wp(S=[Assignment(x,1000),Assignment(y,0),\
    While(FExp(y < 10),[Assignment(y,y+1)],inv=FAnd(x==a1, b1 <= y ,y <= b2))],Q=FAnd(True),L=[],verbose=0)
    sage: print rs[0]
    (-a1 + 1000 == 0 and b1 <= 0 and -b2 <= 0)
    sage: print map(str,rs[1])
    ['(((-a1 + x != 0 or b1 - y > 0 or -b2 + y > 0) or y - 10 >= 0) or (-a1 + x == 0 and b1 - y - 1 <= 0 and -b2 + y + 1 <= 0))', '(((-a1 + x != 0 or b1 - y > 0 or -b2 + y > 0) or y - 10 < 0) or True)']

    sage: var('x,y,i,j,k,m, A, B')
    (x, y, i, j, k, m, A, B)
    sage: a6 = Assignment(x,x-y)
    sage: a7 = Assignment(i,i-k)
    sage: a8 = Assignment(j,j-m)
    sage: a10 = Assignment(y,y-x)
    sage: a11 = Assignment(k,k-i)
    sage: a12 = Assignment(m,m-j)
    sage: seq1 = [a6,a7,a8]
    sage: seq2 = [a10,a11,a12]
    sage: cond5 = Conditional(FExp(x>y),seq1,seq2)
    sage: while4 = While(FExp(x!=y),[cond5],inv=FAnd(FExp(x==A*i+B*j),FExp(y==A*k+B*m)))
    sage: Q, L =  wp(while4,Q=FAnd(FBool(True)),L=[],verbose=0)
    sage: print Q
    (-A*i - B*j + x == 0 and -A*k - B*m + y == 0)
    sage: print map(str,L)
    ['(((-A*i - B*j + x != 0 or -A*k - B*m + y != 0) or x - y == 0) or ((x - y <= 0 or (-(j - m)*B - (i - k)*A + x - y == 0 and -A*k - B*m + y == 0)) and (x - y > 0 or (-A*i - B*j + x == 0 and (j - m)*B + (i - k)*A - x + y == 0))))', '(((-A*i - B*j + x != 0 or -A*k - B*m + y != 0) or x - y != 0) or True)']

    sage: Q,L = wp(S=[Conditional(FExp(x==y^2),[Assignment(x,10000)],\
    [Assignment(x,-20000)])],Q=FExp(x>=10),L=[],verbose=0)
    sage: print Q
    ((-y^2 + x != 0 or 9990 >= 0) and (-y^2 + x == 0 or -20010 >= 0))
    sage: print map(str,L)
    []


    sage: var('y c1 c2')
    (y, c1, c2)

    sage: Q,L = wp(S=[While(FExp(x < 10), [Assignment(x,x+1)],inv=FExp(x*c1+c2==0))], Q=FExp(x>=10),L=[],verbose=0)
    
    
    sage: print map(str,L)
    ['((c1*x + c2 != 0 or x - 10 >= 0) or (x + 1)*c1 + c2 == 0)', 
    '((c1*x + c2 != 0 or x - 10 < 0) or x - 10 >= 0)']
    sage: print Q
    c1*x + c2 == 0

    """
    assert isinstance(Q,Formula), 'incorrect Q format %s'%Q
    assert isinstance(L,list), 'incorrect L format %s'%L
    
    if verbose >= 1:
        print 'wp(S=[%s], Q=%s, L=%s)'\
            %(','.join(map(str,S)) if isinstance(S,list) else S,
              Q,','.join(map(str,L)))
    
    if isinstance(S,Break):
        rs = (Q,L)

    elif isinstance(S,Assignment):
        lhs = S.lhs
        rhs = S.rhs
        rs = (Q.fsubs({lhs:rhs}),L)
    
    elif isinstance(S,Conditional):
        Q1,L1 = wp(S.s1,Q,L,verbose)
        Q2,L2 = wp(S.s2,Q,L,verbose)
        rs1 = Formula.implies(S.b,Q1)
        rs2 = Formula.implies(S.b.fneg(),Q2)
        rs = (FAnd(rs1,rs2),[L1,L2])

    elif isinstance(S,While):
        """
        wp(while[inv](b){s},Q) == inv and (inv and b => (s,inv)) and (inv and not b => Q)
        See lec7.pdf
        """
        #lec7.pdf says  wp(s,*Q*,L) , I think it should be wp(s,I,L) instead
        Q_,L_ = wp(S.s,S.inv,L,verbose) 
        L1 = Formula.implies(FAnd(S.inv,S.b),Q_)
        L2 = Formula.implies(FAnd(S.inv,S.b.fneg()),Q)
        rs = (S.inv,[L_,L1,L2])
    
    elif isinstance(S,list):
        if len(S) == 0:
            return (Q,L)
        elif len(S) == 1:
            rs = wp(S[0],Q,L,verbose)
        else:
            Q_,L_= wp(S[1:],Q,L,verbose)
            rs = wp(S[0],Q_,L_,verbose)

    else:
        raise AssertionError('incorrect S format %s'%S)

    Q_,L_ = rs
    Q_.fsimplify()
    L_ = [l for l in L_ if not CM.is_none_or_empty(l)]
    if verbose >= 1: 
        print 'wp Q: %s'%(Q_)
        print 'wp L: %s'%'.'.join(map(str,L_))


    assert isinstance(Q_,Formula) and isinstance(L_,list)
    return Q_,L_


def vc(P,S,Q,verbose=1):
    """
    Generates Verification Conditions (vc's) using Hoare's logic 
    using weakest precondition.
    P is the precondition, S is a list of statements (the program), and 
    Q is the postcondition.

    EXAMPLES:
    sage: print vc(P=FExp(x==100),S=[Assignment(x,x+1000)],Q=FExp(x>=1000),verbose=0)
    (x - 100 != 0 or x >= 0)

    sage: var('a1 a2 a3 a4 a5 a6 y')
    (a1, a2, a3, a4, a5, a6, y)
    sage: P = FBool(True)
    sage: S = [Assignment(x,-50),While(FExp(x<0),[Assignment(x,x+y),Assignment(y,y+1)], \
    inv=FOr(FExp(a1*x+a2*y+a3 >= 0), FExp(a4*x+a5*y+a6>=0)))]
    sage: Q = FExp(y > 0)
    sage: print vc(P,S,Q,verbose=0)
    ((a2*y - 50*a1 + a3 >= 0 or a5*y - 50*a4 + a6 >= 0) and ((a1*x + a2*y + a3 < 0 and a4*x + a5*y + a6 < 0) or x >= 0 or (y + 1)*a2 + (x + y)*a1 + a3 >= 0 or (y + 1)*a5 + (x + y)*a4 + a6 >= 0) and ((a1*x + a2*y + a3 < 0 and a4*x + a5*y + a6 < 0) or x < 0 or y > 0))


    sage: print vc(P,S,Q,verbose=0).to_cnf()
    ((a2*y - 50*a1 + a3 >= 0 or a5*y - 50*a4 + a6 >= 0) and (a1*x + a2*y + a3 < 0 or x >= 0 or (y + 1)*a2 + (x + y)*a1 + a3 >= 0 or (y + 1)*a5 + (x + y)*a4 + a6 >= 0) and (a4*x + a5*y + a6 < 0 or x >= 0 or (y + 1)*a2 + (x + y)*a1 + a3 >= 0 or (y + 1)*a5 + (x + y)*a4 + a6 >= 0) and (a1*x + a2*y + a3 < 0 or x < 0 or y > 0) and (a4*x + a5*y + a6 < 0 or x < 0 or y > 0))


    sage: var('nn,m,x,y,a0,a1,a2,a3,a4,b0,b1,b2,b3,b4')
    (nn, m, x, y, a0, a1, a2, a3, a4, b0, b1, b2, b3, b4)

    sage: P = FAnd(*map(FExp,[nn>=1,nn<=1,m>=1,m<=1,x>=0,x<=1,y>=0,y<=1]))
    sage: I = FAnd(*map(FExp,[a0+a1*x+a2*y+a3*nn+a4*m >= 0,b0+b1*x+b2*y+b3*nn+b4*m>=0]))
    sage: Q = FExp(y>=100)
    sage: S = While(FExp(x<100),[Assignment(x,x+nn),Assignment(y,y+m)],inv=I)
    sage: print vc(P,S,Q,verbose=0)
    ((nn - 1 < 0 or nn - 1 > 0 or m - 1 < 0 or m - 1 > 0 or x < 0 or 
    x - 1 > 0 or y < 0 or y - 1 > 0 or (a1*x + a2*y + a3*nn + a4*m + a0 >= 0 and 
    b1*x + b2*y + b3*nn + b4*m + b0 >= 0)) and 
    (a1*x + a2*y + a3*nn + a4*m + a0 < 0 or 
    b1*x + b2*y + b3*nn + b4*m + b0 < 0 or x - 100 >= 0 or 
    ((nn + x)*a1 + (m + y)*a2 + a3*nn + a4*m + a0 >= 0 and 
    (nn + x)*b1 + (m + y)*b2 + b3*nn + b4*m + b0 >= 0)) and 
    (a1*x + a2*y + a3*nn + a4*m + a0 < 0 or 
    b1*x + b2*y + b3*nn + b4*m + b0 < 0 or x - 100 < 0 or y - 100 >= 0))

    # Example 1 Mccune (illustrates the usage of these constructs
    # to write  this small program)
    sage: S=[Assignment(x,2),Assignment(y,3)]
    sage: b1 = [Assignment(y,-y+4),Assignment(x,-x+3)]
    sage: b2 = [Assignment(x,-x-3),Assignment(y,-y+5)]
    sage: sb = [Conditional(FExp(y >= 2),b1,b2)]
    sage: wl = While(FExp(x+y>=0),sb,inv=FBool(True))

    """
    Q_,L_ = wp(S,Q,[],verbose)
    rs = Formula.implies(P,Q_)


    if not CM.is_none_or_empty(L_):
        rs = FAnd(rs,FAnd(*L_))
        rs = rs.fsimplify()

    return rs



