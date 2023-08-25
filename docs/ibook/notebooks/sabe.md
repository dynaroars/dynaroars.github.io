# Software Analysis By Examples

## CEGAR

### General Algorithm 
1. Run the analyzer on the program `P` using an initial (simple) abstract domain `A`.
1. If the analyzer says `P` is `safe`, then __return__ `safe` (abstraction `A` is sufficiently strong to prove the safety of `P`).
1. Otherwise (i.e., the analyzer says `P` is `unsafe`), the analyzer reports a counterexample (cex), from which we need to check for validity (i.e., the counterexample represent an error in the abstract program, but it might not be true in the real program).  Two possible cases:
  1. The cex is `valid`, then __return__ `unsafe` (we can also extract a concrete trace showing the violation).
  1. Otherwise, refine the abstraction `A` to `A'`and repeat the analysis on `A`.

### Examples

#### Sign Domain

__Source__: http://www.cs.tau.ac.il/~msagiv/courses/asv/cegar.pdf


```C
z = 5;
if (y > 0)
   x = z;
else
   x = -y;
assert(x > 0);
```

Clearly, the assertion `x > 0` holds in this program. Let's apply CEGAR to achieve this.


First, assume the analyzer starts the abstract domain `sign(x)`, which consists of only three possible values: `P` positive `>= 0`, `N` negative `< 0`, or `?` can be either. The following shows the analyzer determines the sign of `x` at every program location.

```C
// sign(x) = ?
z = 5;
// sign(x) = ?
if (y > 0)
   // sign(x) = ?  
   x = z;     
   // sign(x) = ?
else
   // sign(x) = ?
   x = -y;
   // sign(x) = ?

//sign(x) = ? (union of the two branches)
assert(x > 0);
```

Thus, when using the abstract domain `sign(x)`, the analyzer cannot prove that the assertion holds because `x` could be anything.

Assume the analyzer decides to refine the domain by using both the signs of `x` and `y`, i.e., `sign(x), sign(y)`.  The analysis on the new domain is then

```C
// sign(x) = ?, sign(y) = ?
z = 5;
// sign(x) = ?, sign(y) = ?
if (y > 0)
   // sign(x) = ?, sign(y) = P
   x = z;     
   // sign(x) = ?, sign(y) = P
else
   // sign(x) = ?, sign(y) = N
   x = -y;
   // sign(x) = P, sign(y) = N

//sign(x) = ?, sign(y) = ?  (union of two branches, e.g., sign(y) = ? because Y or N is ? )
assert(x > 0);
```

Once again, the analyzer cannot prove the assertion when using the domain `sign(x), sign(y)`.

Let's refine the domain again by using `sign(x), sign(y), sign(z)`.

```C
// sign(x) = ?, sign(y) = ?, sign(z) = ?
z = 5;
// sign(x) = ?, sign(y) = ?, sign(z) = P
if (y > 0)
   // sign(x) = ?, sign(y) = P, sign(z) = P
   x = z;     
   // sign(x) = P, sign(y) = P, sign(z) = P
else
   // sign(x) = ?, sign(y) = N, sign(z) = P
   x = -y;
   // sign(x) = P, sign(y) = N, sign(z) = P

//sign(x) = P, sign(y) = ?, sign(z) = P
assert(x > 0);
```

With this new, more precise domain, the analyzer finally verifies the assertion.


#### Predicate Abstraction

```C
lock = 0;
do{
    lock = 1;
	old = new;
	if(*){
        lock =0;
        new++;
	}
}while (new != old);

if (lock == 0)
    error();

lock = 0
```

In this program, `error()` is not reachable, i.e.,  after existing the while loop, we always have `lock == 1`.

Let's start the analysis using the initial abstraction constaining of the predicates `lock==0` and `lock==1`.
The analysis can reach `error()` and return a counterexample path 

```C
lock = 0;   
//lock == 0
do{
    //lock == 0
    lock = 1;
    //lock == 1
    old = new;
    //lock == 1
    if(*){
        //lock == 1
        lock =0;
        //lock == 0
        new++;
        //lock == 0;
    }
    else{
    //lock == 1
    }
}while (new != old);

//lock == 0 | lock == 1
if (lock == 0)
    error();

lock = 0
```

### Resources 

