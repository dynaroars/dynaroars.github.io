# import common as CM
# from sage.all import *

from abc import ABC, abstractmethod


class Formula(ABC):
    """
    Abstract class for simple First order logic.
    """

    def __init__(self, f):
        self.f = f

    def val(self):
        return self.f

    @abstractmethod
    def is_atom(self):
        pass

    @abstractmethod
    def fsubs(self, a, b):
        pass

    @abstractmethod
    def fneg(self):
        pass

    @abstractmethod
    def to_cnf(self):
        # http://aima.cs.berkeley.edu/python/logic.html
        pass

    @abstractmethod
    def to_z3py(self):

    @staticmethod
    def implies(f1, f2):
        assert isinstance(f1, Formula) and isinstance(f2, Formula)
        return FOr(f1.fneg(), f2)

    # @staticmethod
    # def collect_coeffs(f, uvs):
    #     """
    #     Collect coefficients for variables in uvs
    #     (variables that are universal quantified)

    #     Input:
    #     fexp: -a2*ld_0*y - a5*ld_1*y + 50*a1*ld_0*x - \
    #     a3*ld_0 + 50*a4*ld_1 - a6*ld_1 - ld_0 - ld_1 + LD == 0
    #     uvs: [x,y]   #universal variables
    #     Output:
    #     1) - a3*ld_0 + 50*a4*ld_1 - a6*ld_1 - ld_0 - ld_1 + LD == 0
    #     #fexp without terms containing variables in uvs
    #     2) sum of coefficients of variables in uvs
    #     collect all terms containing x,y, ...

    #     sage: var('y a1 a2 a3 a4 a5 a6 ld_0 ld_1 LD')
    #     (y, a1, a2, a3, a4, a5, a6, ld_0, ld_1, LD)

    #     sage: Formula.collect_coeffs(-a2*ld_0*y - a5*ld_1*y + 50*a1*ld_0*x \
    #     - a3*ld_0 +  50*a4*ld_1 - a6*ld_1 - ld_0 - ld_1 + LD == 0, uvs=[x,y])
    #     (-a3*ld_0 + 50*a4*ld_1 - a6*ld_1 + LD - ld_0 - ld_1 == 0,
    #     [50*a1*ld_0 == 0, -a2*ld_0 - a5*ld_1 == 0])
    #     """

    #     assert f.is_relational() and f.operator() == operator.eq
    #     uvs_ = [v for v in uvs if v in f.variables()]
    #     assert uvs_

    #     f0 = f
    #     fs = []
    #     for v in uvs_:
    #         f_ = f0.coeffs(v)
    #         # should have only orders 0 and 1 (i.e. const and linear)
    #         assert len(f_) == 2
    #         f0 = f_[0][0]
    #         fs = fs + [f_[1][0]]

    #     return f0, fs

    # @staticmethod
    # def gen_inputs(d):
    #     ks = d.keys()
    #     vs = d.values()
    #     rs = [dict(zip(ks,v)) for v in CartesianProduct(*vs)]
    #     return rs

    # @staticmethod
    # def gen_bounded_val_formula(f,ds):
    #     print len(ds)
    #     assert f.is_cnf()
    #     rs = FOr(*[f.fsubs(d) for d in ds])
    #     rs = rs.fsimplify()
    #     return rs


class FBool(Formula):

    def __init__(self, f):
        assert isinstance(f, bool), f

        super().__init__(f)

    def __eq__(self, other):
        b1 = (other is self)
        b2 = (isinstance(other, FBool)) and self.val() == self.val()
        return b1 or b2
    
    def __str__(self):
        return str(self.val())

    def is_atom(self):
        return True
        
    def fneg(self):
        return FBool(not(self.val()))

    def fsubs(self,d):
        return self

    def fsimplify(self):
        return self

    def is_cnf(self):
        return True

    def to_cnf(self):
        return self

    def to_z3py(self):
        return str(self)



class FExp(Formula):
    def __init__(self,f):
        assert isinstance(f,Expression) and f.is_relational()
        if not f.rhs() == 0:
            f = f.subtract_from_both_sides(f.rhs())
        super(FExp,self).__init__(f)

    def __eq__(self,other):
        """

        sage: var('y')
        y

        sage: FExp(x >= 0) == FExp(x == 0)
        False
        sage: FExp(x >= 0) == FExp(x >= 0)
        True
        sage: FExp(x -1 >= 0) == FExp(x >= 0)
        False
        sage: FExp(x -1 >= 0) == FExp(x >= 0)
        False
        sage: FExp(x -1 >= 0) == FExp(x >= 1)
        True
        sage: FExp(x -1 == 0) == FExp(x >= 1)
        False
        sage: FExp( -1 + x - y == 0) == FExp(x >= 1 + y)
        False
        sage: FExp( -1 + x - y == 0) == FExp(x == 1 + y)
        True
        sage: FExp( -1 + x - y == 0) == FExp(x == 1 + y)
        True
        """
        
        b1 = (other is self)
        b2 = isinstance(other,FExp) and \
            (self.val().operator() == other.val().operator() and \
             self.val().lhs() == other.val().lhs() and \
             self.val().rhs() == other.val().rhs())
        
        return b1 or bool(b2)
    
    def __str__(self):
        return str(self.val())


    def is_atom(self):
        return True
    
    def fneg(self):
        return FExp(self.val().negation())

    def fsubs(self,d):
        return FExp(self.val().subs(d))

    def fsimplify(self):
        return self

    def is_cnf(self):
        return True

    def to_cnf(self):
        return self

    def to_z3py(self):
        return str(self).replace('^','**')

    ######
    def myconvert(self):
        """
        returns e' < 0
        
        e < 0  =>  e     < 0, 
        e > 0  => -e     < 0, 
        e <= 0 =>  e - 1 < 0, because e <= 0 == e < 1  ==  e - 1 < 0
        e >= 0 => -e - 1 < 0, because e >= 0 == e > -1 ==  e + 1 > 0 ==  -e-1 <0
        e == 0 =>  ????

        sage: var('y, a1, a2, a3')
        (y, a1, a2, a3)

        sage: print FExp(-50*a1+a2*y+a3 >= 0).myconvert()
        -a2*y + 50*a1 - a3 - 1 < 0
        sage: print FExp(-50*a1+a2*y+a3 > 0).myconvert()
        -a2*y + 50*a1 - a3 < 0
        sage: print FExp(-50*a1+a2*y+a3 < 0).myconvert()
        a2*y - 50*a1 + a3 < 0
        sage: print FExp(-50*a1+a2*y+a3 <= 0).myconvert()
        a2*y - 50*a1 + a3 - 1 < 0
        sage: print FExp(-50*a1+a2*y+a3 == 0).myconvert()
        Traceback (most recent call last):
        ...
        AssertionError: dont know how to apply conversion to < from ==
        
        """
        assert self.val().rhs() == 0
        
        if self.val().operator() == operator.lt: #   <
            #already in correct format, i.e., e < 0
            rs = self
        elif self.val().operator() == operator.gt: # >
            rs = FExp(-1 * self.val().lhs()     < 0)
        elif self.val().operator() == operator.le: # <=
            rs = FExp(     self.val().lhs() - 1 < 0)
        elif self.val().operator() == operator.ge: # >=
            rs = FExp(-1 * self.val().lhs() - 1 < 0)
        else:
            assert self.val().operator() == operator.eq # ==
            assert False, 'dont know how to apply conversion to < from =='

        assert isinstance(rs,FExp) and rs.is_cnf() and \
            rs.val().operator() == operator.lt
        return rs

    def farkas(self,uvs,eid=None):
        """
        uvs:  universal quantified variables, e.g., [x,y]
        
        sage: var('y, a1, a2, a3')
        (y, a1, a2, a3)

        sage: print FExp(-50*a1+a2*y+a3 >= 0).farkas([x,y])
        (50*a1*ld - a3*ld + LD - ld == 0 and -a2*ld == 0 and ld >= 0 and LD > 0)

        sage: print FExp(-50*a1+a2*y+a3*x >= 0).farkas([x,y])
        (50*a1*ld + LD - ld == 0 and -a3*ld == 0 and -a2*ld == 0 and ld >= 0 and LD > 0)
        """
        
        rs = self.myconvert()
        
        ld = var('ld%s'%('' if eid is None else '%d'%eid))
        LD = var('LD%s'%('' if eid is None else '%d'%eid))
        rs1 = (ld*rs.val().lhs()).expand() + LD == 0
        rs1,rs2 = Formula.collect_coeffs(rs1,uvs)
        rs3 = [ld >= 0, LD > 0]

        rs = FAnd(*map(FExp,[rs1]+rs2+rs3)).fsimplify()

        assert rs.is_cnf()
        return rs
    

                
class FAnd(Formula):
    
    def __init__(self,*args):
        assert isinstance(args,tuple) and len(args) >= 1
        _f = lambda a: FBool(a) if isinstance(a,bool) else \
            (FExp(a) if isinstance(a, Expression) else a)
        args = tuple([_f(a) for a in args])
        assert CM.vall(args, lambda a: isinstance(a,Formula))
        super(FAnd,self).__init__(args)
        
    def __eq__(self,other):
        b1 = lambda: other is self
        b2 = lambda: (isinstance(other,FAnd)) and \
            len(self.val())==len(other.val()) and \
            CM.vall(zip(self.val(),other.val()),lambda (x,y): x==y)
        return b1() or b2()
        
    def __str__(self):
        rs = '(%s)' if len(self.val()) > 1 else '%s'
        return rs%(' and '.join(map(str,self.val())))

    def __iter__(self):
        for f in self.val():
            yield f

    def __len__(self):
        return len(self.val())

    ######
    def is_atom(self):
        return False
    
    def fneg(self):
        return FOr(*[f.fneg() for f in self.val()])

    def fsubs(self,d):
        return FAnd(*[f.fsubs(d) for f in self.val()])

    def fsimplify(self):
        """
        Simplify Ands

        sage: var('y')
        y

        sage: print FAnd(FExp(x==y), FExp(x+2==y), FOr(FExp(x+3==y), \
        FExp(x+4==y), FBool(True)), FBool(False)).fsimplify()
        False
        sage: print FAnd(FExp(x==y), FExp(x+2==y), FOr(FExp(x+3==y), \
        FExp(x+4==y),  FBool(True)), FExp(x==y-1)).fsimplify()
        (x - y == 0 and x - y + 2 == 0 and x - y + 1 == 0)
        sage: print FAnd(FExp(x==y),FExp(x+2==y),FOr(FExp(x+3==y), \
        FExp(x+4==y),  FBool(False)), FExp(x==y-1)).fsimplify()
        (x - y == 0 and x - y + 2 == 0 and 
        (x - y + 3 == 0 or x - y + 4 == 0) and x - y + 1 == 0)
        """
        
        fs = [f.fsimplify() for f in self.val()]

        # v1 and  Or(v2,v3)  and And(v4,v5..) ...  =  v1,Or(v2,v3),v4,v5)
        fs = CM.flatten([f.val() if isinstance(f,FAnd) else f for f in fs])

        # False and ...and   => False
        if CM.vany(fs,lambda f: isinstance(f,FBool) and f.val() == False):
            return FBool(False)

        # True and ... and  => and ... and
        if len(fs) >= 2:
            fs = [f for f in fs if not (isinstance(f,FBool) and f.val() == True)]

        return fs[0] if len(fs) == 1 else FAnd(*fs)


    def is_cnf(self):
        """
        sage: var('y, s')
        (y, s)

        sage: (FAnd(FExp(x==0),FExp(y==0), \
        FAnd(FExp(y==0), FExp(s==0)))).is_cnf()
        False
        sage: (FAnd(FExp(x==0),FExp(y==0), \
        FAnd(FExp(y==0), FExp(s==0)))).fsimplify().is_cnf()
        True
        """
        _f = lambda f: f.is_atom() or (isinstance(f,FOr) and f.is_cnf())
        return CM.vall(self,_f)
                        
    def to_cnf(self):
        """
        sage: var('y s')
        (y, s)

        sage: print FAnd(FExp(x==1),FOr(FExp(x==2), \
        FAnd(FExp(x==3),FExp(x==4)))).to_cnf()
        (x - 1 == 0 and (x - 3 == 0 or x - 2 == 0) 
        and (x - 4 == 0 or x - 2 == 0))

        sage: print (FAnd(FExp(x==0),FExp(y==0),\ 
        FAnd(FExp(y==0), FExp(s==0)))).fsimplify().to_cnf()
        (x == 0 and y == 0 and y == 0 and s == 0)

        sage: print FAnd(FOr(x==1,FAnd(x==2,x==3).fneg(), x==4),x==5).to_cnf()
        ((x - 1 == 0 or x - 2 != 0 or x - 3 != 0 or x - 4 == 0) 
        and x - 5 == 0)
        """
        rs = self.fsimplify()
        if rs.is_cnf():
            return rs

        rs = FAnd(*[f.to_cnf() for f in rs.val()])
        rs = rs.fsimplify()

        assert rs.is_cnf()
        return rs

    def to_z3py(self):
        rs = 'And(%s)' if len(self.val()) > 1 else '%s'
        return rs%(','.join(map(lambda f:f.to_z3py(), self)))
    
    ######
    def farkas(self, uvs):
        """
        sage: var('y, a1, a2, a3, a4, a5, a6')
        (y, a1, a2, a3, a4, a5, a6)

        sage: print FAnd(FOr(FBool(False),-50*a1+a2*y+a3 >= 0, \
        -50*a4+a5*y+a6 >= 0),-80*a3+a1+8*a2*y>=0).farkas([x,y])
        (50*a1*ld_0_0 - a3*ld_0_0 + 50*a4*ld_0_1 - 
        a6*ld_0_1 + LD0 - ld_0_0 - ld_0_1 == 0 and
        -a2*ld_0_0 - a5*ld_0_1 == 0 and ld_0_0 >= 0 and ld_0_1 >= 0 
        and LD0 > 0 and -a1*ld1 + 80*a3*ld1 + LD1 - ld1 == 0 and 
        -8*a2*ld1 == 0 and ld1 >= 0 and LD1 > 0)
        
        """
        
        rs = self.to_cnf()
        assert isinstance(rs,FExp) or isinstance(rs,FOr) or isinstance(rs,FAnd)

        if isinstance(rs,FExp) or isinstance(rs,FOr):
            return rs.farkas(uvs)
        else:
            assert isinstance(rs,FAnd) and len(rs) > 1
            #assert CM.vall(rs, lambda f: isinstance(f,FOr))

            rs = [f.farkas(uvs,eid=d) for d,f in enumerate(rs)]
            rs = FAnd(*rs).fsimplify()
            assert rs.is_cnf()
            return rs



class FOr(Formula):
    
    def __init__(self,*args):
        assert isinstance(args,tuple) and len(args) >= 1
        _f = lambda a: FBool(a) if isinstance(a,bool) else \
            (FExp(a) if isinstance(a,Expression) else a)
        args = tuple([_f(a) for a in args])
        assert CM.vall(args, lambda a: isinstance(a,Formula))
        super(FOr,self).__init__(args)

    def __eq__(self,other):
        b1 = lambda: other is self
        b2 = lambda: (isinstance(other,FOr)) and \
            len(self.val())==len(other.val()) and \
            CM.vall(zip(self.val(),other.val()),lambda (x,y): x==y)
        return b1() or b2()
    
    def __str__(self):
        rs = '(%s)' if len(self.val()) > 1 else '%s'
        return rs%(' or '.join(map(str,self.val())))
        

    def __iter__(self):
        for f in self.val():
            yield f

    def __len__(self):
        return len(self.val())

    ######
    def is_atom(self):
        return False

    def fneg(self):
        return FAnd(*[f.fneg() for f in self.val()])

    def fsubs(self,d):
        return FOr(*[f.fsubs(d) for f in self.val()])

    def fsimplify(self):
        """
        Simplify ORs
        
        EXAMPLES:

        sage: var('y')
        y

        sage: print FAnd(x==y,x+2==y,FOr(x+3==y, x+4==y, True)).fsimplify()
        (x - y == 0 and x - y + 2 == 0)
        
        sage: print FOr(FExp(x==y),FExp(x+2==y),FOr(FExp(x+3==y), \
        FExp(x+4==y), FBool(True))).fsimplify()
        True
        """
        
        fs = [f.fsimplify() for f in self.val()]

       
        # v1 or  Or(v2,v3)  or And(v4,v5..) ...  =  v1,v2,v3 or And(v4,v5)
        fs = CM.flatten([f.val() if isinstance(f,FOr) else f for f in fs])


        # True or ...or   => True
        if CM.vany(fs,lambda f: isinstance(f,FBool) and f.val() == True):
            return FBool(True)

        # False or ... or  => or ... or
        if len(fs) >= 2:
            fs = [f for f in fs if not (isinstance(f,FBool) and f.val() == False)]

        
        return fs[0] if len(fs) == 1 else FOr(*fs)
        
    def is_cnf(self):
        """
        sage: var('y')
        y
        sage: FOr(FExp(x==y),FExp(x+2==y), \
        FAnd(FExp(x+3==y), FExp(x+4==y))).is_cnf()
        False
        """
        return CM.vall(self, lambda f: f.is_atom())
                        
    def to_cnf(self):
        """
        http://aima.cs.berkeley.edu/python/logic.html

        sage: print FOr(FExp(x==1),FAnd(FExp(x==2),\
        FExp(x==3)),FExp(x==4)).to_cnf()
        ((x - 2 == 0 or x - 1 == 0 or x - 4 == 0) and 
        (x - 3 == 0 or x - 1 == 0 or x - 4 == 0))
        """

        rs = self.fsimplify()
        if rs.is_cnf():
            return rs

        assert len(rs.val()) > 1, 'FOr len %d'%len(rs.val())

        #find first conj and the rest
        exists_conj,conj = exists(rs.val(), lambda f: isinstance(f,FAnd))
        assert exists_conj, 'no FAnd'
        
        rest = FOr(*[f for f in rs.val() if f is not conj])

        #distrib And over Or
        rs = FAnd(*[FOr(c,rest).to_cnf() for c in conj.val()])
        rs = rs.fsimplify()

        assert rs.is_cnf()
        return rs

    def to_z3py(self):
        rs = 'Or(%s)' if len(self.val()) > 1 else '%s'
        return rs%(','.join(map(lambda f:f.to_z3py(), self)))
    
    ######
    def farkas(self,uvs,eid=None):
        """
        Apply Farkas's lemma
        Input:
        FOr(e1 <  0, e2 < 0, .. , en < 0)
        The above is equivalently to
        FAnd(e1 >= 0, e2 >= 0, .. , en >= 0).fneg()

        Output:
        (ld1*e1 + ld2*e2 + .. + ldn*e3 + LD == 0) and (ld1,ld2,ldn >= 0) and (ld > 0)

        sage: var('y, a1, a2, a3, a4, a5, a6')
        (y, a1, a2, a3, a4, a5, a6)

        sage: print FOr(False,-50*a1+a2*y+a3 >= 0, \
        -50*a4+a5*y+a6 >= 0).farkas([x,y])
        (50*a1*ld_0 - a3*ld_0 + 50*a4*ld_1 - a6*ld_1 + LD - ld_0 - ld_1 == 0 
        and -a2*ld_0 - a5*ld_1 == 0 and ld_0 >= 0 and ld_1 >= 0 and LD > 0)
        """
        rs = self.to_cnf()
        assert isinstance(rs,FExp) or isinstance(rs,FOr)

        if isinstance(rs,FExp):
            return rs.farkas()
        else:
            assert isinstance(rs,FOr) and len(rs) > 1
            assert CM.vall(rs, lambda f: isinstance(f,FExp))

            rs = FOr(*[f.myconvert() for f in rs])
            
            lds = [var('ld_%s%d'%('' if eid is None else '%d_'%eid,ld))
                   for ld in srange(len(rs))]
            LD = var('LD%s'%('' if eid is None else '%d'%eid))
            
            rs1 = [(ld*e_).expand() for ld,e_ in
                   zip(lds,[f.val().lhs() for f in rs])]
            rs1 = sum(rs1) + LD == 0
            
            rs1,rs2 = Formula.collect_coeffs(rs1,uvs)
            
            rs3 = [ld >= 0 for ld in lds] + [LD > 0]

            rs = FAnd(*map(FExp,[rs1]+rs2+rs3)).fsimplify()

            assert rs.is_cnf()
            return rs

        


"""
Constructs of a simple imperative language that supports 
if-then-else, while, assignment, sequence
"""


class Construct(object):
    def __init__(self,verbose):
        pass

class Break(Construct):
    """
    sage: print Break()
    break

    sage: Break() == Break()
    True
    """
    def __init__(self,verbose=1):
        super(Break,self).__init__(verbose)


    def __eq__(self,other):
        b1 = other is self
        return b1 or isinstance(other,Break)
    
    def __str__(self):
        return 'break'
    
class Assignment(Construct):
    """
    sage: var('y')
    y
    sage: print Assignment(x,1000)
    x := 1000
    sage: print Assignment(x,y+100)
    x := y + 100

    sage: Assignment(x,y+100) == Assignment(x,100+y)
    True
    """
    def __init__(self,lhs,rhs,verbose=1):
        assert lhs.is_symbol()
        
        super(Assignment,self).__init__(verbose)
        self.lhs = lhs
        self.rhs = rhs

    def __eq__(self,other):
        b1 = other is self

        #b2 might evaluated to as an expression, thus convert to bool
        b2 = isinstance(other,Assignment) and \
            bool(self.lhs == other.lhs and self.rhs == other.rhs)
        return b1 or b2 

    def __str__(self):
        return '%s := %s'%(self.lhs,self.rhs)


class Conditional(Construct):
    """
    sage: var('y')
    y

    sage: print Conditional(FExp(x>y),[Assignment(x,x+y)], \
    [Assignment(x,y+10),Break(),Break()])
    if (x - y > 0) {x := x + y} else {x := y + 10; break; break}

    sage: Conditional(FExp(x>y),[Assignment(x,x+y)], \
    [Assignment(x,y+10),Break(),Break()]) == \
    Conditional(FExp(x>y),[Assignment(x,x+y)], \
    [Assignment(x,y+10),Break(),Break()])
    True

    sage: Conditional(FExp(x>y),[Assignment(x,x+y)],\
    [Assignment(x,y+10),Break(),Break()]) == \ 
    Conditional(FExp(x>y),[Assignment(x,x+y)],\ 
    [Assignment(x,10+y),Break(),Break()])
    True

    sage: Conditional(FExp(x>y),[Assignment(x,x+y)], \
    [Assignment(x,y+10),Break(),Break()]) == \
    Conditional(FExp(x>y),[Assignment(x,x+y)], \
    [Assignment(x,11+y),Break(),Break()])
    False

    """
    def __init__(self,b,s1,s2,verbose=1):
        assert isinstance(b,Formula)
        assert isinstance(s1,list) and len(s1) > 0 \
            and CM.vall(s1, lambda s: isinstance(s,Construct))
        assert isinstance(s2,list) and len(s2) > 0 \
            and CM.vall(s2, lambda s: isinstance(s,Construct))
        
        super(Conditional,self).__init__(verbose)
        self.b  = b
        self.s1 = s1
        self.s2 = s2

    def __eq__(self,other):
        b1 = other is self

        _f = lambda l1,l2 : len(l1)==len(l2) \
            and CM.vall(zip(l1,l2),lambda (x,y): x==y)
        b2 = isinstance(other,Conditional) and \
            self.b == other.b and \
            _f(self.s1,other.s1) and \
            _f(self.s2,other.s2)

        return b1 or b2        

    def __str__(self):
        s = "if (%s) {%s} else {%s}"
        return s%(self.b,'; '.join(map(str,self.s1)),'; '.join(map(str,self.s2)))
                                         

class While(Construct):
    """
    sage: var('y, a1, b1, b2')
    (y, a1, b1, b2)

    sage: print While(FExp(y < 10), [Assignment(y,y+1)], \
    inv=FAnd(FExp(x==a1), FExp(b1 <= y), FExp(y <= b2)))
    while [(-a1 + x == 0 and b1 - y <= 0 and -b2 + y <= 0)] (y - 10 < 0) {y := y + 1}

    sage: While(FExp(y < 10), [Assignment(y,y+1)], \
    inv=FAnd(FExp(x==a1), FExp(b1 <= y) , FExp(y <= b2))) == \
    While(FExp(y < 10), [Assignment(y,y+1)], \
    inv=FAnd(FExp(x==a1), FExp(b1 + 2 <= y) , FExp(y <= b2)))
    False
    """
    def __init__(self,b,s,inv,verbose=0):
        assert isinstance(b,Formula)
        assert isinstance(inv,Formula)
        assert isinstance(s,list) and len(s) > 0 and \
            CM.vall(s, lambda s_: isinstance(s_,Construct))
        
        super(While,self).__init__(verbose)

        self.b = b
        self.s = s
        self.inv = inv

    def __eq__(self,other):
        b1 = other is self

        _f = lambda l1,l2 : len(l1)==len(l2) \
            and CM.vall(zip(l1,l2),lambda (x,y): x==y)
        b2 = isinstance(other,While) and \
            self.b == other.b and \
            self.inv == other.inv and \
            _f(self.s,other.s)

        return b1 or b2
    
    def __str__(self):
        s = "while [%s] (%s) {%s}"
        return s%(self.inv,self.b,'; '.join(map(str,self.s)))
    


    
    


#(P & Q) | (~P & R) | (~Q & ~R) => (P | R | ~Q) & (Q | ~P | ~R)



"""
need to do hash inorder to apply uniq
print FAnd([FExp(x==y),FExp(x+2==y),FOr([FExp(x+3==y), FExp(x+4==y), FBool(True)]), FExp(x+y==y+y),FExp(x==y)])
(x - y == 0 and x - y + 2 == 0 and (x - y + 3 == 0 or x - y + 4 == 0 or True) and x - y == 0 and x - y == 0)

"""
