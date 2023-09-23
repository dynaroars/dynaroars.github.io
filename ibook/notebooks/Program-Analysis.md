





# Old stuff

> Analyzing program semantics using Hoare logic is also called **axiomatic semantics**.  In contrast to **operational semantics**, e.g., big-step reduction, where we define the semantics of the program as a transformation from a state to another. For example,  if we start the program with the state $\{ x\mapsto 3, y \mapsto 4 \}$, we get the new state $\{ x \mapsto 7, y \mapsto 2 \}$.
In contrast, in **axiomantic semantics**, the semantics of the program is a transformation from a _set_ of states to another set of states, i.e., from the states satisfying a precondition to the states satisfying the postcondition.
For example, if we start a (division) program with the precondition $y \ne 0$, at the termination of the program, we get the postcondition $r \equiv x/y$.



### WP for Assignment Statement
The wp function $\text{wp}(x:=e, Q) = Q_x^e$ says that we can achieve wp of the assignment  `x:= e` wrt to the postcondition $Q$ by simply replacing all occurences of the variable $x$ in $Q$ with the expression $e$.

#### Examples
1. wp(x:=3, $x +y \equiv 10$) =  $(x +y \equiv 10)_x^3$ = $3 + y \equiv 10$ = $y = 7$
- wp(x:=3, $x +y > 0$) =  $(x +y > 0)_x^{3}$ = $y > -3$
- wp(x:= 3*y + z, $x * y - z > 0$)   =  $(x * y - z > 0)_x^{3*y+z}$ = $(3*y+z) * y - z > 0$

### WP for Sequential Statements
- wp(x := x + 3, $x \equiv z$) = $x + 3 \equiv z$
- wp(x := x + 1; y := y * x , $y \equiv 2 * z$) \
    = wp(x := x + 1 , $(y \equiv 2 * z)_y^{y*x}$) \
    = wp(x := x + 1 , $y*x \equiv 2 * z$) \
    = $(y*x \equiv 2 * z)_x^{x+1}$ \
    = $y*(x+1) \equiv 2 * z$
- wp(if x > 0 then y := x else y := 0,$y > 0$) = $x > 0 \Rightarrow x > 0 ~\wedge~ x \le 0 \Rightarrow 0 > 0$.  Note this wp would be False because in the else branch, after setting y := 0, it's not possible to get the post condition $y > 0$.