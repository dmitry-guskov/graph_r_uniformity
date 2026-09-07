# Removing the large graph-enumeration dependencies

Current dependency status: the final analytic_profile_lemma.md and dimension_two_analytic.md replace every new finite proof dependency in this earlier derivation. Computations are retained as corroboration; the consolidated TeX/PDF is the current proof presentation.

The C3 square C3 square C4 base now has an analytic proof. The dimension-three families with two short sides and one arbitrary long side need only a finite certificate of scalar slice profiles. The earlier large three-dimensional generator-subset scans are independent corroboration, not proof dependencies. Neither the new scalar certificate nor either analytic argument reads previous scan results.

## Analytic base C3 square C3 square C4

Write H=C3 square C3. A singleton selection in H has weight five. A pair has weight six: adjacent vertices have one common neighbor and their binary adjacency output has weight six including both selected vertices; nonadjacent vertices have two common neighbors and adjacency-output weight four, disjoint from the selected pair. Every selection x also has w_H(x)>=|x|.

Suppose a selection in H square C4 has W<=5, hence total cardinality r<=5. Let k be its number of occupied slices. For k=1, the unperturbed H weight plus its two empty neighbors gives W=w_H(x)+2r. This is seven for a singleton, at least ten for a pair, and at least nine for r>=3. For k=2, the exact two-occupied-slice inequality in higher_mixed_extension.md gives W>=w_H(u)+w_H(v). If both sizes are at most two, this is at least ten. Otherwise the possible size pairs are (3,1),(3,2),(4,1), up to order, giving lower bounds eight, nine, nine respectively. Thus k=2 is impossible.

For k=4, all occupied sizes are at most two, so every internal slice weight is at least four. Summing the occupied bounds gives W>=16-2r>=6. For k=3, write the three consecutive sizes as a,b,c, with b the middle. If all sizes are at most two, each slice has internal weight at least four. With m=max(a,c), the occupied-slice maxima and the empty-slice difference bound give

    W >= b+max(a,4-b)+max(c,4-b)+|a-c|
      >= b+2max(m,4-b) >= 4+m.

This is at least six if m>=2. If m=1, the endpoints are singletons and have weight five, so replacing four by five in this bound again gives at least six. The only remaining cardinality profiles are permutations of (3,1,1). For (1,3,1), the occupied slices alone contribute at least 2+3+2=7. For (3,1,1) or its reflection, they contribute at least 3+1+4=8. Every case contradicts W<=5, proving distance at least six.

For the matching witness, let A be the binary adjacency matrix of C3 square C3 square C4, and let B sum the two C3 coordinate adjacencies. Over F_2, A^2=B. The selection x=Ae_v therefore has Ax=Be_v supported inside x, and weight |N(v)|=6. Thus the distance is exactly six. This proof has no finite-enumeration dependency.

## Elementary cross-section profile

For each H in {C3 square C3, C3 square C4, C4 square C4}, singleton weight is five and pair weight is at least six. To see the pair bound, adjacent vertices have at most one common neighbor, while nonadjacent vertices have at most two. For an adjacent pair, its selected vertices already lie in the adjacency output, whose weight is 8-2c>=6. For a nonadjacent pair, selected vertices and adjacency output are disjoint, giving weight 2+8-2c>=6. These common-neighbor counts follow directly by whether the two vertices differ in one or two Cartesian coordinates. In one coordinate, C3 has one common neighbor for an adjacent pair and C4 has two for an opposite pair; in two coordinates there are exactly two intermediate vertices.

For every size s<=7 we may therefore use the analytic lower profile

    f(0..7) = [0,5,6,3,4,5,6,7].

The entries for s>=3 use only w_H(x)>=s. Exact cross-section enumeration is unnecessary for this lower profile.

## Finite profile certificate

Given nonnegative slice cardinalities r_0,...,r_(L-1), the stabilizer weight is at least

    B(r) = sum_(r_t>0) max(r_t, f(r_t)-r_(t-1)-r_(t+1))
           + sum_(r_t=0) |r_(t-1)-r_(t+1)|.

The portable standard-library Python script check_small_slice_profiles.py exhausts every nonnegative profile with 5<=L<=15 and 2<=sum r_t<=7, using the analytically proved f above. There are exactly 489,698 profiles. It checks each per-(L,r) count against the stars-and-bars identity C(L+r-1,r). Every profile has B(r)>=8; the global minimum is exactly eight. The exact per-case counts, minima and witnesses appear in small_slice_profiles.json. This is an explicitly finite computer-assisted part of the proof, not evidence extrapolated from sampled lengths.

The script additionally enumerates 30,134 small cross-section subsets to corroborate f, but its finite profile certificate is computed before and independently of those graph enumerations. The earlier version checked all three exact profiles separately, totaling 1,469,094 scalar profiles; the final proof script removes those redundant checks and uses the one weaker analytic profile.

Run from any directory with Python >=3.10 using `python3 /path/to/check_small_slice_profiles.py`. The script writes small_slice_profiles.json alongside itself and requires no repositories, third-party libraries, network access, or other artifacts.

## Exact reduction from arbitrary long sides

Consider H square C_L with L>=5 and suppose W<=7. Then r<=7. A singleton has weight seven, so suppose r>=2. For L<=15 the finite certificate immediately contradicts W<=7. For L>=16, the occupied projection has at most seven positions. If there were no two consecutive empty positions, sending each empty position to its successor would inject the empty positions into the occupied ones, forcing L<=2r<=14. Thus an adjacent-empty pair exists.

Cut within this empty pair. The first and last occupied slices have distinct outward neighboring empty slices. In each, any selected cross-section vertex of the neighboring occupied slice produces an odd output; in particular there is at least one odd output at each end. These two vertices lie outside S and are distinct, so W>=r+2. Hence W<=7 implies r<=5.

Now shorten every empty gap to length min(gap,2), preserving the occupied slice vectors and their cyclic order. Occupied-slice adjacency outputs do not change: a nonempty gap still contributes a zero neighboring slice. A length-one gap still receives the sum of both occupied boundary slices. A gap of length at least two has distinct boundary empty slices, receiving the two boundary vectors separately, while its interior empty slices contribute zero. Thus this shortening preserves W exactly, even if S is disconnected.

The resulting cycle has length at most k+2k=3k<=3r<=15. If its length is below five, extend a retained gap of length two until the total is five; at least one such gap exists because the original profile had an adjacent-empty pair. This extension also preserves every contribution. We therefore obtain a selection of the same cardinality and weight on a cycle of length in [5,15], contradicting the finite profile certificate.

Consequently each H square C_L in the three stated families has distance seven and only singleton minimum selections for every L>=5. No connected-component assumption, G-squared lift, or enumeration of three-dimensional graph subsets is required by this revised proof.

## Revised dependencies

The all-short induction now uses the published Hamming-code result (including the explicitly recorded C3 cubed base), the analytic C3 squared square C4 base above, and Lemma A. The two-short-direction D3 long-cycle families use the analytic f and the 489,698-profile finite certificate. The one-short/two-long D3 argument and the original all-long theorem retain their existing analytic proofs. Large three-dimensional scans remain useful independent verification, but their results are no longer used to establish this extension.
