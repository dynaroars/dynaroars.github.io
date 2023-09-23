import common as CM
from smt import SMT
from time import time
from sage.all import *

class Cegar(object):

    @staticmethod
    def randCounterExL(vs,ceN=10,verbose=0):
        """
        generate a random list of values given variables vs
        """
     
        rs = [[randint(-1000,1000) 
               for _ in srange(len(vs))] 
        for _ in srange(ceN)]

        return [dict(zip(vs,rs_)) for rs_ in rs]
    
    @staticmethod
    def createTemplate(vsU,vsK,verbose=0):
        ts = Miscs.genTerms(1,vsK,verbose=verbose)
        #ts = [t for t in ts if t != 1]
        ps = [Miscs.createTemplate(ts,rv=None,prefix=str(v)+'_',verbose=verbose) 
              for v in vsU]

        return dict(zip(vsU,ps))

    @staticmethod
    def parseF(f):
        vs = Miscs.getVars(f)
        
        vsK, vsU = CM.vpartition(vs,lambda v: str(v).startswith('uk'))
        vsTypesU = [(str(v),'Int') for v in vsU]
        vsTypesK = [(str(v),'Int') for v in vsK]
        return vsU,vsK,vsTypesU,vsTypesK
            
    @staticmethod
    def go(f,seed=0,verbose=0):
        """
        Return sat if f is satisfiable
        Otherwise, return unsat or unknown
        """
        
        seed = time() if seed is None else seed
        set_random_seed(seed)

        if verbose >= 1:
            print 'seed', seed

        vsU,vsK,_,_=Cegar.parseF(f)
        rs = Cegar.createTemplate(vsU,vsK,verbose=verbose)
        f_ = f(rs)

        s,assignment = Cegar.solve(f_,verbose=verbose)
        if assignment is not None:
            assert s == 'sat'
            rs_ = dict([(k,c(assignment)) for k,c in rs.items()])
            return s,rs_
        else:
            return s
        
    @staticmethod
    def solve(f,iterMax=10,verbose=0):
        
        vsU,vsK,vsTypesU,vsTypesK=Cegar.parseF(f)


        counterexL=Cegar.randCounterExL(vsK,verbose=verbose)
        iterN = 0
        assignment = None

        if verbose >= 1:
            print 'begin Cegar for',f
        while(True):
            if iterN > iterMax:
                return 'unknown',None

            gf,assignment= Cegar.synthesizer(f,counterexL,
                                             vsTypes=vsTypesU,verbose=verbose)
              
            if verbose >= 1:
                print '%d. %s (%s)'%(iterN,gf,assignment)


            if gf is None:
                return 'unsat',None

            ce = Cegar.verifier(gf,vsTypes=vsTypesK,verbose=verbose)

            if ce is None:
                return 'sat',assignment

        
            counterexL = counterexL + [ce]
            iterN = iterN + 1

    @staticmethod
    def doSMT(f,vsTypes,verbose=0):

        f = SMT.i2p_l(f,b='and')
        f = SMT.smt2_format(vsTypes,f,verbose=verbose)

        cmd = 'z3 -smt2 -in -m'
        #cmd = 'cvc3 +model -lang smt2'

        is_true,rs,rs_err = SMT.run(cmd,f,true_kw='sat',
                                    retBool=False,getModel=True,
                                    verbose=verbose)

        if issat:
            rs = SMT.parse_result(rs)
            return rs
        else:
            return None
    
    @staticmethod
    def synthesizer(f,counterexL,vsTypes,verbose=0):
        """
        Synthesize f' such that f' satisfies the counterexamples
        
        Inputs:
        counterexL is a list of dict
        
        """
        fs = [f(ce) for ce in counterexL]
        rs = Cegar.doSMT(f=fs,vsTypes=vsTypes,verbose=verbose)

        if rs is None:
            return None,None
        else:
            return f(rs),rs

    @staticmethod
    def verifier(f,vsTypes,verbose=0):
        """
        Verify f by looking for counterexamples. 
        If there exists none, returns None 
        else, return counterexample
        """
        f_neg = f.negation()
        rs = Cegar.doSMT(f=f_neg,vsTypes=vsTypes,verbose=verbose)
        
        if rs is None:
            return None
        else:
            return rs
