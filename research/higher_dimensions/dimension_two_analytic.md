# Analytic two-dimensional classification

For a>=3 and L>=5, the graph G=C_a square C_L has minimum nonidentity stabilizer weight five. Its minimum elements are precisely the aL canonical generators, except when a=L=5, where ten additional five-generator selections occur. This argument uses no finite enumeration. It is a working proof for independent review.

Slice along C_L. Write r_t for each selected slice's cardinality, r=sum r_t, k for the number of occupied slices, and f(s)=3 if s=1 and f(s)=s otherwise. The internal cycle C_a has singleton weight three and every selection has weight at least its cardinality. Consequently

W >= sum_(r_t>0) max(r_t,f(r_t)-r_(t-1)-r_(t+1)) + sum_(r_t=0) |r_(t-1)-r_(t+1)|.

Assume W<=5, hence r<=5. A singleton gives weight five. We exclude every r>=2 except the stated diagonal cases.

If k=1, its two empty neighbors contribute 2r, giving W>=f(r)+2r>=6.

If k=2, each occupied position in a cycle of length at least five has at least one empty neighbor that is not adjacent to the other occupied position. Those exclusive empty slices are distinct and contribute the two cardinalities, hence at least r in total. The selected vertices contribute another r. This excludes r>=3. If r=2, both occupied slices are singletons: when nonadjacent their unperturbed internal weights already sum to six; when adjacent, the exact two-slice inequality W>=w_H(u)+w_H(v) from the product-lemma note also gives six.

If k=3 and the occupied induced graph has no edges, the occupied contributions alone are sum f(r_t)>=7 under 3<=r<=5. If it has one edge, let a,b denote its endpoint populations and c the isolated population. For a+b=2 the two occupied edge endpoints contribute at least four and f(c)>=2. For a+b=3 the pair contributes at least three; this suffices for c=1. The only other case is c=2, where the occupied lower bound is five. The two empty gaps connecting the isolated component to the occupied edge contribute at least |a-c|+|b-c|>=|a-b|=1: a length-one gap contributes the corresponding difference, while a longer gap contributes the sum of the boundary populations, at least the difference. For a+b=4, necessarily c=1, and the edge pair contributes at least four while the isolated singleton adds three. Thus every one-edge case gives at least six.

The remaining k=3 shape is a path with consecutive populations a,b,c. Its two outward empty neighbors are distinct because L>=5 and contribute u=a+c. Retaining selected sites gives W>=b+2u>=7 when u>=3. If u=2, both endpoints are singletons, and

W >= b+2+2 max(1,3-b) >=6,

for b=1,2,3. This excludes all three-slice cases.

If k=4 and r=4, every occupied slice is a singleton. The projection is a proper subset of C_L, so its total induced-degree deficit delta=sum_(t occupied)(2-deg_P t) is at least two. The occupied contributions give W>=12-2r+delta>=6.

If k=4 and r=5, there is one double slice and three singleton slices. Let e be the number of induced occupied edges and d the degree of the double slice in that induced graph. Summing internal weights minus neighbor populations gives 11-2r+delta. Here delta=10-2e-d. At the double slice, replacing the bound 2-d by its mandatory two selected sites improves the sum by d, since all its occupied neighbors are singletons. Hence W>=11-2e. If e<=2 this is at least seven. If e=3, the projection is a four-slice path. Up to reversal the profiles are (2,1,1,1) and (1,2,1,1). Their individual occupied-slice maxima are respectively (2,1,1,2) and (1,2,1,2), each summing to six. No empty-slice contribution is needed.

Finally k=5 forces r=5 with all five occupied slices singletons. Their occupied contribution is 15-2r+delta=5+delta. If the projection is a proper subset of the cycle, delta>=2 and W>=7. Thus a nonsingleton minimum can occur only when L=5 and exactly one vertex is selected in every slice.

Write that vertex as a_t in C_a. Since W=r=5, every Z-output slice is supported only at its selected vertex. Its parity is even: the internal cycle adjacency output has two entries and its two neighboring singleton inputs have even combined parity. A vector supported on one coordinate with even parity is zero. Therefore

A_(C_a) e_(a_t) = e_(a_(t-1)) + e_(a_(t+1)).

The left side is the pair of distinct neighbors of a_t. Thus the sequence is a closed nonbacktracking walk of length five on C_a. A nonbacktracking walk on a cycle keeps a fixed orientation, so a_t=a_0+epsilon t modulo a, with epsilon=+1 or -1. Closure requires a to divide five. Since a>=3, this forces a=5. The five offsets and two orientations give exactly ten distinct selections; each has zero odd neighborhood and weight five. Along with the 25 generators, they yield multiplicity 35. All other cases have only the aL canonical minima.

Priority: the distance-five statement for square tori is explicit in Kovalev, Dumer and Pryadko (2011), Example 6; rectangular sides at least five and a diagonal example appear in Sudevan and Das (2022). The present argument supplies a unified analytic proof including a short side and the complete minimum classification. Novelty of that extension is not established.
