# Dimension-two minimum classification and correction

Current dependency status: the final analytic_profile_lemma.md and dimension_two_analytic.md replace every new finite proof dependency in this earlier derivation. Computations are retained as corroboration; the consolidated TeX/PDF is the current proof presentation.

The dimension-two minimum classification requires an exception at C5 square C5. The higher-dimensional long-cycle lemma has hypothesis h>=6 and gives uniqueness for D>=3 after the audited dimension-three base.

For L,M>=5, the stabilizer distance of C_L square C_M is five. Its minimum selections are exactly the LM singletons, except when L=M=5, where there are ten additional five-vertex selections. These are

    S_(c,epsilon) = {(i, c+epsilon*i mod 5): i in Z_5},
    c in Z_5, epsilon in {1,-1}.

Consequently the minimum multiplicity is LM except at C5 square C5, where it is 35. The separate audited mixed-side dimension-two result shows singleton uniqueness when one side is 3 or 4 and the other is at least 5. Thus for all dimension-two tori with sides at least three and a long side, the only exception is C5 square C5.

Proof of completeness for L,M>=5. Assume W<=5, hence the selection cardinality r<=5. Slice along either coordinate; each occupied slice has its unperturbed cycle weight at least three, and a two-vertex slice has weight at least four. The latter follows directly from the two selected vertices' neighborhoods: an adjacent pair has its two distinct outward neighbors in support, while a nonadjacent pair has either four odd neighbors or two odd neighbors outside the pair. A cycle of length at least five has neither adjacent twins nor a triangle.

If k>=5 slices are occupied, then k=5 and r=5. Summing occupied-slice bounds gives W>=3k-2r+delta=5+delta, where delta is the weighted induced-degree deficit. Thus delta=0, so the occupied projection is the full coordinate cycle and that cycle is C5. If k=4, r is four or five. When r=4, all slice weights are singleton weights and the degree deficit is at least two, giving W>=12-8+2=6. When r=5 and the occupied projection has at least two components, its deficit is at least four, giving W>=12-10+4=6. Otherwise it is a four-slice path. If either endpoint has size two, its endpoint deficit together with the neighboring empty outputs is at least four, again giving W>=6. The only remaining cardinality profiles are (1,2,1,1) and its reflection, followed by one or more empty slices. The occupied-slice lower bounds for (1,2,1,1) are respectively 1,2,1,2, totaling six. This uses the two-vertex cycle weight four and the maximum with each slice's selected cardinality. Hence k=4 is impossible.

For k<=2, a coordinate cycle of length at least five has two consecutive empty positions: otherwise each empty position's successor would be occupied, implying L-k<=k. For k=3 without two consecutive empty positions, L is 5 or 6. At L=6 the projection is alternating and the occupied slices alone contribute at least nine. At L=5 it consists of an occupied edge with cardinalities a,b and an isolated occupied slice with cardinality c, where a+b+c<=5. The occupied slice bounds and the two empty-slice outputs give

    W >= 9-a-b+|a-c|+|b-c| >= 7.

For c=1, the expression is exactly seven. For c=2, the positive pair (a,b) is (1,1), (1,2), or (2,1), and the expression is nine or seven. For c=3, necessarily a=b=1 and the expression is eleven. No other c is possible. Thus k=3 without an adjacent-empty pair is also impossible.

We have shown that each projection either has an adjacent-empty pair or is the full C5 with r=5. If both projections have adjacent-empty pairs, the audited extremal-support lemma gives W>=r+4, forcing r=1. If either projection is the full C5, the other cannot have an adjacent-empty pair, because the partial extremal-support lemma would give W>=r+2=7. Therefore a nonsingleton minimum requires both coordinate lengths five and exactly one selected vertex in every row and column. Write it as S={(i,f(i))} for a permutation f of Z_5.

Since W=r=5, Odd(S) is contained in S. Every vertex of S has zero neighbors in S, by the one-per-row-and-column property, so actually Odd(S) is empty. Row i of its binary adjacency output is

    e_(f(i-1)) + e_(f(i+1)) + e_(f(i)-1) + e_(f(i)+1) = 0.

Both pairs contain distinct indices. Therefore their unordered sets are equal, so f maps each vertex's two cycle neighbors to the two neighbors of its image. Thus f is an automorphism of C5, namely f(i)=c+epsilon*i. Conversely each of these ten permutations has zero adjacency output and selection cardinality five, verifying every claimed exceptional minimum. QED.

Independent finite check: check_d2.py enumerates every anchored selection of cardinality one through five in C5 square C5 and every permutation graph. Its records are in d2_checks.json; this is a check of the analytic classification, not a finite-case extrapolation.
