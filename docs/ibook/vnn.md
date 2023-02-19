# Reluplex
- website
- author

## Algorithm
## Example
### Problem 
- ![dnn example](files/dnn1.pdf)

### Step-by-step illustration

## Strengths and Limitations


# Marabou
- website
- author

# Reluval
- website
- author

# ERAN
- website
- author

# nnenum
- website
- author

# (Standard) Symbolic Execution

## Symbolic states for the DNN in Fig. :
n00 ≡ ite(i0 − i1 >= 0, i0 − i1, 0) and
n01 ≡ ite(i0 + i1 >= 0, i0 + i1, 0) and
n10 ≡ ite( n00
2 − n01
5 >= 0, n00
2 − n01
5 , 0) and
n11 ≡ ite(−n00
2 + n01
10 >= 0, −n00
2 + n01
10 , 0) and
o0 ≡ n10 + −n11 and
o1 ≡ −n10 + n11


Now, we can reason about the DNN using the computed symbolic states. For example, to check
that the DNN in Fig. 1 has the property 𝑃1 = (𝑛00 > 0.0 ∧ 𝑛01 ≤ 0.0) ⇒ o0 > o1) shown in § 2.2,
i.e., checking that the implication 𝐹 ⇒ 𝑃1 is valid, we can use Z3 to show that the negation of
the implication is unsat, i.e., isSat(¬(𝐹 ⇒ 𝑃1)) = isSat(𝐹 ∧ ¬𝑃1)) = unsat. Here, Z3 returns
unsat, which verifies that 𝑃1 is a property of the DNN.
Similarly, we would obtain unsat for property 𝑃2 shown in § 2.2 indicating that 𝑃2 a valid property
of the DNN. However, for property 𝑃3 shown in § 2.2, we would get sat from Z3, indicating that
𝑃3 is not a valid property of the DNN. Moreover, we can extract from Z3 a satisfying assignment
representing a counterexample showing the violation.
