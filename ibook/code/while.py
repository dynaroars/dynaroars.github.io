"""
Constructs of a simple imperative language that supports
if-then-else, while, assignment, sequence
"""

import z3
from typing import NamedTuple


class Statements(list):
    """
    >>> y = z3.Int('y')
    >>> x = z3.Int('x')    
    >>> s = Statements([Assignment(y,z3.IntVal("1000"))])
    >>> print(s)
    y := 1000;
    >>> s = Statements([Assignment(x,y+10),Skip(),Skip()])
    >>> print(s)
    x := y + 10; Skip; Skip;

    >>> Q = x + y == 7
    >>> s = Statements([Assignment(x,x+1),Assignment(y,y-2),Skip(),Skip()])
    >>> s.wp(Q)
    x + y == 8

    >>> inv = x <= 10
    >>> b = x < 10
    >>> s = Statements([Assignment(x,x+1)])
    >>> s = While(inv, b, s)
    >>> s = Statements([s])
    >>> print(s)
    while [x <= 10] (x < 10) {x := x + 1;}
    >>> Q = x == 10
    >>> P = x < 10
    >>> _ = s.prove(P, Q)
    proved    
    """
    def __init__(self, s):
        self.s = s

    def __str__(self):
        return ' '.join(map(str, self.s))

    def wp(self, Q):
        if len(self.s) == 0:
            return Q
        elif len(self.s) == 1:
            rs = self.s[0].wp(Q)
        else:
            s = Statements(self.s[1:])
            rs = self.s[0].wp(s.wp(Q))
        return rs


    def prove(self, P, Q):
        vc =  z3.Implies(P, self.wp(Q))
        print(z3.prove(vc))

class Skip(NamedTuple):
    """
    >>> print(Skip())
    Skip;

    >>> Skip() == Skip()
    True
    """

    def __str__(self):
        return 'Skip;'

    def wp(self, Q):
        return Q


class Assignment(NamedTuple):
    """
    >>> y = z3.Int('y')
    >>> x = z3.Int('x')
    >>> s1 = Assignment(y,z3.IntVal("1000"))
    >>> print(s1)
    y := 1000;
    >>> print(Assignment(x,y+100))
    x := y + 100;
    >>> Assignment(x,y+100) == Assignment(x,100+y)
    False

    >>> Q =  x + y < 100
    >>> s1.wp(Q)
    Not(-900 <= x)

    """

    lhs: z3.ExprRef
    rhs: z3.ExprRef

    def __str__(self):
        return f"{self.lhs} := {self.rhs};"

    def wp(self, Q):
        return z3.simplify(z3.substitute(Q, (self.lhs, self.rhs)))


class Conditional(NamedTuple):
    """
    >>> y = z3.Int('y')
    >>> x = z3.Int('x')
    >>> b = x>y
    >>> s1 = Statements([Assignment(x,x+y)])
    >>> s2 = Statements([Assignment(x,y+10),Skip(),Skip()])
    >>> print(Conditional(b,s1,s2))
    if (x > y) {x := x + y;} else {x := y + 10; Skip; Skip;}
    >>> assert Conditional(b,s1,s2) == Conditional(b,s1,s2)
    >>> s3 = [Assignment(x,y+11),Skip(),Skip()]
    >>> assert Conditional(b,s1,s2) != Conditional(b,s1,s3)
    """

    b:  z3.ExprRef
    s1: Statements
    s2: Statements

    def __str__(self):
        return f"if ({self.b}) {{{self.s1}}} else {{{self.s2}}}"

    def wp(self, Q):
        rs1 = z3.Implies(self.b, self.s1.wp(Q))
        rs2 = z3.Implies(z3.Not(self.b), self.s2.wp(Q))
        return z3.And(rs1, rs2)


class While(NamedTuple):
    """
    >>> x, y, a1, b1, b2 = z3.Ints("x y a1 b1 b2")
    >>> inv = z3.And(x==a1, b1 <= y, y <= b2)
    >>> b = y < 10
    >>> s = Statements([Assignment(y,y+1)])
    >>> print(While(inv,b,s))
    while [And(x == a1, b1 <= y, y <= b2)] (y < 10) {y := y + 1;}

    >>> inv = x <= 10
    >>> b = x < 10
    >>> s = Statements([Assignment(x, x+1)])
    >>> s = While(inv, b, s)
    >>> print(s)
    while [x <= 10] (x < 10) {x := x + 1;}
    >>> Q = x == 10
    >>> s.wp(Q)
    And(x <= 10,
        Or(Not(And(x <= 10, Not(10 <= x))), x <= 9),
        Or(Not(And(x <= 10, 10 <= x)), x == 10))
    """
    inv: z3.ExprRef
    b: z3.ExprRef
    s: Statements

    def __str__(self):
        return f"while [{self.inv}] ({self.b}) {{{self.s}}}"

    def wp(self, Q):
        """
        wp(while[inv](b){s},Q) == inv and (inv and b => (wp(s,inv))) and (inv and not b => Q)
        See lec7.pdf
        """
        f2 = z3.Implies(z3.And(self.inv, self.b), self.s.wp(self.inv))
        f3 = z3.Implies(z3.And(self.inv, z3.Not(self.b)), Q)
        return z3.simplify(z3.And([self.inv, f2, f3]))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
