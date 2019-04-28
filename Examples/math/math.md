Emma Bernstein, Cole Hollant
MATH 332
December 3, 2018

**Exercise 22.22.** Find a polynomial of degree $> 0$ in $\mathbb{Z}_4\left[x\right]$ that is a unit. $\lozenge$

**Proof.** Let $\phi(x) = (2x+1)$. In $\mathbb{Z}_4$, then $\phi(x) \cdot \phi(x) = (2x+1)^2 = 4x^2 + 4x + 1 \equiv 1 (\text{mod } 4)$. Therefore $\phi(x)$ is a unit with degree $>0$. $\square$

**Excercise 22.24.** If $D$ is an integral domain, then $D[x]$ is an integral domain. $\lozenge$

**Proof.** Let $f,g \in D[x]$ such that $f(x)=a_0 + a_1 x + \ldots + a_n x^n$ is a polynomial of degree $n$ and $g(x)= b_0 + b_1 x + \ldots + b_mx^m$ is a polynomial of degree $m$. Let $f(x) \neq 0$ and $g(x) \neq 0$. Then $f(x) \cdot g(x) = a_0 b_0 + (a_0 b_1 + a_1 b_0)x + \ldots + a_n b_m x^{n+m}$.

@@ Suppose $f(x) g(x) = 0$. Then all coefficients $a_i, b_j$ for $0 \leq i \leq n$ and $0 \leq j \leq m$ must be 0 because $D$ is an integral domain and therefore has no zero divisors. Then, because $D$ has no zero divisors, then $a_n=0$ or $b_m=0$, and either the degree of $f\neq n$ or the degree of $g\neq m$. Hence $D[x]$ is an integral domain. $\square$