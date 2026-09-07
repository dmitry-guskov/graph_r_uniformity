# Mixed short sides: separate extension note

Status: The D3 proof dependencies in this earlier note are superseded by higher_dimensions/analytic_profile_lemma.md and higher_dimensions/dimension_two_analytic.md; the exact records remain independent corroboration. This is a computer-assisted classification candidate, with complete reductions to explicitly enumerated finite cases and an elementary analytic completion. It does not alter the earlier pure proof for every side length at least five. The mathematical reductions and programs require independent audit before publication. The subsequent priority challenge is recorded in ../higher_dimensions/priority_challenge.md.

For a graph-state generator subset S, write W(S)=|S union Odd(S)| and r=|S|. Multiplicity below means the number of nonidentity stabilizer elements of minimum weight, not the number of supports modulo translations or local Clifford equivalence.

## Result in the requested scope

For D=2, suppose at least one side is three or four. If the other side L is at least five, the stabilizer distance is five and the minimum-weight stabilizers are precisely the 3L or 4L canonical generators. The all-short cases have distance/multiplicity (3,6) for C3×C3, (4,18) for C3×C4, and (4,28) for C4×C4.

For D=3, suppose at least one side is three or four. If at least one other side is at least five, the stabilizer distance is seven and the only minimum-weight elements are the N canonical generators. The all-short cases have distance six. Their respective multiplicities are 117 for C3³, 48 for C3²×C4, 48 for C3×C4², and 64 for C4³.

Thus the condition that every side length is at least five is not individually necessary. In particular C4×C5 is exactly four-uniform, and C4×C5×C5 is exactly six-uniform. This note makes no new claim about minimum multiplicity for D=2 when both sides are at least five; C5×C5 has its known ten extra diagonal minima.

## Compression with exact support preservation

Let G² join two distinct vertices whenever their distance in G is at most two. Decompose S into connected components S_j in G². Their closed neighborhoods in G are pairwise disjoint: a common closed-neighborhood vertex would give a G path of length at most two between two components. The binary Pauli vectors and their supports therefore cannot cancel across components, and W(S)=sum_j W(S_j).

Fix a cycle coordinate of length L and a G²-connected component of cardinality r. If L≥2r+1, its occupied coordinate projection has two consecutive empty positions: otherwise the successor injection from empty to occupied positions would imply L≤2r. Cut the cycle at such an empty pair. No distance-at-most-two edge between selected vertices crosses this cut, since selected vertices on opposite sides are separated by at least three steps through the gap. A spanning tree of S in G² can thus be lifted consistently into H×Z in this coordinate. Each edge changes its lifted coordinate by at most two, so the coordinate span max−min is at most 2(r−1).

Translate the lifted minimum to zero. The selected positions fit into [0,2r−2]. For any b≥r, embed the same positions in C_(2b+1). There remain at least two empty slices at the seam. Adjacencies inside the occupied interval are unchanged. The only nonzero output slices outside that interval are the immediate neighboring empty slices: they carry the first and last nonzero input slices, respectively. Those two output slices stay distinct because the empty gap has length at least two. All other empty slices have zero output. Consequently changing the length of the empty gap preserves the exact support size W, including every odd-neighborhood overlap and cancellation. All other coordinates remain unchanged.

This is an exact compression of a connected component, not an assumption that arbitrary S is connected. For uniqueness, suppose W(S)≤b. Every component has W(S_j)≤b. If the finite/analytic checks imply that each such component must be a singleton of weight b, then there can be only one component. Hence S itself is a singleton. Merely proving that some component is small would not suffice for multiplicity; the preceding argument supplies the missing step.

## D=2 strips: complete finite reduction

Take b=5. A component with W≤5 has r≤5. For L≥11, compress it to C3×C11 or C4×C11, preserving r and W. Lengths 5 through 10 are checked directly. The anchored enumeration exhausts every subset cardinality 1 through 5 for all C_a×C_L with a∈{3,4} and L=5,…,11. It finds W=5 only at r=1; every r=2,…,5 has minimum greater than five. Translation transitivity justifies anchoring one selected vertex at the origin. Larger subsets cannot have W≤5 because W≥r. The component argument then proves the strip claim for every L≥5, including minimum multiplicity.

The program actually also checks L=12,13,14; these additional runs are not needed for the reduction.

## D=3 with two short directions

Let H be C3×C3, C3×C4, or C4×C4, and consider H×C_L with L≥5. First handle r≤5. The same component compression with b=5 reduces every long L≥11 to L=11. Exhaustive checks for L=5,…,11 find weight seven only at r=1, and weight strictly greater than seven at r=2,…,5. This excludes every nonsingleton G²-connected component of these cardinalities having W≤7.

It remains to rule out r=6 or 7, without compression or a connectivity assumption. If the long coordinate has two consecutive empty slices, the extremal-witness lemma in that one coordinate gives two distinct external odd-neighborhood vertices, so W≥r+2≥8.

Otherwise no two empty slices are consecutive. If k slices are occupied, L≤2k≤2r≤14, giving a bounded arithmetic check. Let r_t be the input support sizes in cyclic slices, and let f_H(s) be the minimum internal stabilizer weight on H of an s-element subset. Exhaustive enumeration of all subsets of the three fixed cross-section graphs gives the following values for s=0,…,7:

```
H=C3×C3:  0,5,6,3,4,5,6,7
H=C3×C4:  0,5,6,7,4,5,6,7
H=C4×C4:  0,5,6,7,4,5,6,7
```

In an occupied slice, perturbation by its two neighboring input slices can remove at most r_(t−1)+r_(t+1) elements from the internal support, and its X support cannot disappear. In an empty slice, the output is the XOR of its two neighboring inputs and has support at least the absolute difference of their cardinalities. Therefore the rigorous profile bound is

```
W ≥ Σ_(r_t>0) max{r_t, f_H(r_t) − r_(t−1) − r_(t+1)}
    + Σ_(r_t=0) |r_(t−1) − r_(t+1)|.
```

The program `projection_bounds.py` enumerates every nonnegative cyclic profile of total six or seven on L=5,…,14 with no consecutive zeros, by choosing occupied positions and positive compositions of r. There are exactly 2,689 such profiles per cross-section. The bound is at least ten in every case, hence no W≤7 case is omitted. This completes the all-L argument. Together with the component argument for r≤5 and W≥r for r≥8, it proves the stated distance and multiplicity.

## D=3 with one short and two long directions

Now let G=C_a×C_L×C_M, where a∈{3,4} and L,M≥5. Suppose W≤7, so r≤7. Along either long coordinate, the cross-section is a D=2 strip of distance five, now certified for all lengths. Apply the original slice inequality to its occupied projection P of size k.

If k≥5, W≥5k−2r≥11. If k=4, the occupied projection is a proper subset of a cycle, so the weighted degree deficit is at least two and W≥20−(2r−2)≥8. Thus k≤3. If there are no adjacent empty positions, then k=3 and the cycle length is five or six; the occupied induced maximum degree is at most one, giving W≥15−r≥8. Both long directions therefore have adjacent empty slices.

The extremal witnesses in these two directions are distinct, giving W≥r+4. Thus r≤3. A singleton has weight seven. For a pair, the two vertices have at most two common neighbors, or at most one if adjacent in a triangle. In a degree-six cycle product this yields W≥10, excluding r=2.

For r=3, slice along the short coordinate; each nonzero internal slice has weight at least five by the original theorem for C_L×C_M. If all three selected vertices lie in one short slice, its two empty neighbors contribute six support sites, giving W≥11. If two short slices are occupied, their populations are one and two. On C3, the occupied-slice lower bound is 10−3=7, while the single empty slice contributes at least |2−1|=1, giving W≥8. On C4, adjacent occupied slices have two distinct empty neighbors contributing three in total, giving W≥10; opposite occupied slices have no occupied neighbors, already giving W≥10. If three short slices are occupied, each population is one: C3 gives W≥15−6=9; on C4 the occupied path has weighted degree sum four, giving W≥11. Hence r=3 is excluded, proving that only the canonical generators have weight at most seven.

## All-short witnesses and multiplicities

For any product with every side length three or four, write A=B+C over F2, where B is the sum of coordinate adjacencies from three-cycles and C from four-cycles. The shifts commute; each C3 adjacency squares to itself, while each C4 adjacency squares to zero. Thus A²=B. Choosing x=Ae_v, the indicator of the 2D neighbors of v, gives Ax=Be_v, whose support is contained in that of x. Therefore W=2D. This explains the structural failure at all-short D=3 tori without relying on a random counterexample.

The finite anchored checks through r=7 prove that six is the exact D=3 distance and give the multiplicities stated above. On C3²×C4, the 36 neighborhood witnesses account for 36 minima; the remaining 12 are a three-point diagonal in C3² times an antipodal pair in C4. On C3³, an independent enumeration of all six-element subsets confirms 117 minima, splitting by counts of pair distances (1,2,3) into 27 with histogram (3,12,0), 54 with (3,6,6), and 36 with (0,9,6). The minimum supports have an explicit three-family description, checked against the independent exhaustive enumeration. The first family consists of the 27 neighborhoods. The second consists of a diagonal in two coordinates times a two-element subset in the remaining coordinate, giving 3×6×3=54 supports. For the third, regard coordinates as F3³, choose a normal a=(1,±1,±1), and take the affine plane a·x=c with one of its three parallel lines in direction a removed. There are 4×3×3=36 such supports. The three constructed families are disjoint and their union equals all 117 exact minima, as asserted by `summarize.py`. The third family has zero odd neighborhood: after coordinate sign changes it is a sum-constant plane minus a full diagonal; each vertex outside the plane has three neighbors in the plane and one on the removed line, leaving an even number. Vertices in the plane have no neighbors in the plane.

For D=2 all-short cases, the short C3² diagonals have weight three. Exact anchored checks through r=5 establish the distance/multiplicity values above. These finite exceptional graphs are small enough for direct reproduction.

## Reproduction and limits

`results.json` contains every C++ row with counts, minima, minimizing-subset counts, witnesses, runtimes, compiler identity, source hashes, and log hashes. Each anchored count was checked against binomial(N−1,r−1), and all 318 reported witnesses were independently checked with neighbor sets. The two C++ runs together enumerated 7,397,883,264 anchored subsets in 182.434 summed per-cardinality seconds. This includes redundant exploratory D=3 checks through r=7 and extra D=2 strip lengths; the proof reduction needs only the specified subset of them.

Run these commands to reproduce the records. Timing and source/log hashes in the archived JSON refer to the archived run; `summarize.py` regenerates the structured results from the current logs.

```sh
clang++ -O3 -std=c++17 research/mixed_sides/mixed_probe.cpp -o research/mixed_sides/mixed_probe
research/mixed_sides/mixed_probe > research/mixed_sides/mixed_enumeration.txt
clang++ -O3 -std=c++17 research/mixed_sides/cross_section_probe.cpp -o research/mixed_sides/cross_section_probe
research/mixed_sides/cross_section_probe > research/mixed_sides/cross_section_enumeration.txt
python3 research/mixed_sides/projection_bounds.py
python3 research/mixed_sides/summarize.py
```

The C++ bit capacity is fixed at 640 vertices; all supplied workloads are smaller. The extension has a finite computational proof component and should be described that way; it is stronger than a finite-size conjecture but is not yet a purely symbolic proof or a formally verified theorem.
