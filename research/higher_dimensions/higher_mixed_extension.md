# Candidate extension: one long side suffices in every dimension

Status: the final proof now uses analytic_profile_lemma.md and dimension_two_analytic.md in place of every new finite proof dependency. The product lemmas and induction below remain unchanged. The published Hamming-graph code theorem is an external dependency; all new finite computations are corroboration. External proof review and publication priority remain open. The consolidated TeX/PDF is the current presentation.

## Definitions and elementary slice estimates

For a finite simple graph H with binary adjacency matrix A, put w_H(x)=|supp(x) union supp(Ax)| and d(H)=min_{x != 0} w_H(x). Suppose H is h-regular and d(H)>=h. A singleton has weight h+1. Write G=H square C_L, its generator-selection vector as x=(x_t), r_t=|supp(x_t)|, r=sum r_t, and k=|{t:r_t>0}|. Its weight W is the sum of the slice weights

    W_t = |supp(x_t) union supp(Ax_t+x_(t-1)+x_(t+1))|.

All vector operations in this note are over F_2. For occupied slices,

    W_t >= max(r_t, h + 1_{r_t=1} - r_(t-1) - r_(t+1)).                 (1)

For empty slices,

    W_t = |supp(x_(t-1)+x_(t+1))| >= |r_(t-1)-r_(t+1)|.              (2)

Let P be the occupied vertices of C_L, let deg_P denote their induced degrees, and set delta=sum_(t in P)(2-deg_P(t))r_t. Summing (1), without its maximum, gives

    W >= kh - 2r + delta + number of singleton occupied slices
         + sum of the actual empty-slice weights.                  (3)

These estimates count each slice separately; they assume no disjointness of cancellations within a slice.

We also need an exact two-occupied-slice bound. If the slices are not adjacent, their occupied-slice weights are unchanged from H, so W>=2h. If they are adjacent, write their selections u,v. Perturbation by v can remove at most |supp(v) minus supp(u)| from the first slice's original support; the symmetric loss from the second is at most |supp(u) minus supp(v)|. The sum of these losses is |supp(u+v)|. For L=3 the single remaining slice contributes exactly this quantity. For L>=4 the other neighbors of the two occupied slices are distinct empty slices and contribute |u|+|v|, which is at least the loss. Thus

    k=2 implies W >= w_H(u)+w_H(v) >= 2h.                          (4)

For nonadjacent occupied slices on C4 or longer cycles, their output on an empty common neighbor can cancel, but this does not affect their two unchanged occupied-slice weights. Formula (4) therefore covers every arrangement.

## Lemma A: adjoining C4 preserves distance at least the degree

If h is an even integer at least 2, H is h-regular, and d(H)>=h, then d(H square C4)>=h+2.

Proof. Suppose W<=h+1, hence r<=h+1. For k=1 the two neighboring empty slices give W=w_H(x_t)+2r_t>=h+2. For k=2, (4) gives W>=2h>h+1. For k=4, h=2 is impossible since r>=4>h+1; for h>=4, (3) gives W>=4h-2r>=2h-2>h+1.

For k=3, label the three consecutive occupied slices a,b,c by their positive cardinalities, with b in the middle and the fourth slice empty. Set m=max(a,c), s=min(a,c). By (1)-(2),

    W >= b + max(a,h-b)+max(c,h-b)+|a-c|
      >= b + 2 max(m,h-b)
      >= h+m.

The middle inequality follows by the three cases h-b<=s, s<=h-b<=m, and m<=h-b. The final inequality follows by b>=h-m or b<=h-m. If m>=2 this is at least h+2. If m=1, both endpoints are singletons, so replace h by h+1 in this same bound to obtain W>=h+2. Every case contradicts W<=h+1. QED.

## Lemma B: adjoining a long cycle gives full distance and unique minimum selections

If h>=6, H is h-regular, and d(H)>=h, then for every L>=5,

    d(H square C_L)=h+3,

and the only selections attaining h+3 are singleton selections. Consequently the minimum stabilizer multiplicity is |V(H)|L.

Proof. A singleton attains h+3. Suppose W<=h+3, hence r<=h+3. We show any nonsingleton is impossible.

If k>=5, (3) gives W>=5h-2r>=3h-6>=h+6. If k=2, (4) gives W>=2h>=h+6. If k=1 and r>=2, its two distinct neighboring empty slices give W>=h+2r>=h+4.

For k=3, first suppose the occupied induced graph has at most one edge. Its occupied-degree weighted sum is at most r-1, so W>=3h-r+1>=2h-2>=h+4. If it has two edges, the three slices form a consecutive path, with positive cardinalities a,b,c. Because L>=5, the two empty neighbors outside this path are distinct and contribute a+c. Put u=a+c and sigma=1_{a=1}+1_{c=1}. Discarding the middle slice's parity output while retaining its b selected vertices, (1) gives

    W >= 2h-b+u+sigma >= h-3+2u+sigma.

For u>=4 this is at least h+5; for u=3, sigma=1 and it is at least h+4. If u=2, both endpoints are singletons, and the sharper maximum in (1) gives

    W >= b+2 max(1,h+1-b)+2 >= h+4.

For k=4, the occupied induced graph is a union of paths. If it has at least two components, delta>=4, since each component's endpoint degree deficits sum to two and every occupied cardinality is positive. Thus (3) gives W>=4h-2r+4>=2h-2>=h+4. If there is one component, the four occupied slices form a path, whose endpoint cardinalities are a,d. Then delta=a+d. If L=5 its unique empty slice contributes at least |a-d|; if L>=6 its two distinct neighboring empty slices contribute a+d, again at least |a-d|. Therefore delta plus empty-slice contributions is at least 2 max(a,d). If max(a,d)>=2 this is at least four. Otherwise a=d=1, and the two singleton bonuses in (3) raise the total contribution from two to four. Again W>=4h-2r+4>=h+4. All nonsingleton cases have been excluded. QED.

## Published all-triangle base and all-short tori

For H=C3^a with adjacency A, A^2=A over F_2. Therefore every selection x splits as y=Ax and z=(A+I)x, with y in im(A), z in ker(A), and x=y+z. Its stabilizer support is exactly supp(y) union supp(z). Hence

    d(C3^a)=min(d(im A),d(ker A)).                                 (5)

Fish, Key and Mwambene, "Codes, designs and groups from the Hamming graphs," J. Combin. Inform. System Sci. 34 (2009), 169-182, Theorem 1 and Propositions 1-2, prove d(im A)=2a for all a>=1 and d(ker A)=2a+1 for a>=4; Proposition 1 identifies the dual as im(A+I). Thus (5) gives d(C3^a)=2a for a>=4. Proposition 2 also classifies the minimum words in im(A) as adjacency rows for a>=4. This supplies an existing literature result for the all-triangle subfamily, not a new result of this investigation.

Primary full text, uploaded by author Jennifer D. Key: https://www.researchgate.net/publication/268301204_Codes_designs_and_groups_from_the_Hamming_graphs . Inspected Theorem 1, Proposition 1, Proposition 2; publisher citation appears on the first page. The full-text theorem has the dual-distance restriction a>=4; it must not be silently extended to a=2 or a=3.

The published Hamming-code proof explicitly records d(C3^3)=6 through its primal and dual distances. The analytic argument in short_base_simplification.md proves d(C3^2 square C4)=6 using only singleton weight five, pair weight six, and support cardinality bounds; no finite graph enumeration is needed. The one-dimensional bases C3 and C4 both have distance two. Applying Lemma A repeatedly now proves that every all-short torus C3^a square C4^b of dimension d=a+b>=3 has distance at least 2d. The cases partition as follows: a>=4 starts at the published C3^a base; a=3 starts at C3^3; a=2 starts at C3^2 square C4, which exists because d>=3; a=1 starts at C3 and adds the C4 factors; a=0 starts at C4 and adds the others.

The matching upper bound is algebraic. Write A=B+C, where B is the sum of the C3 coordinate adjacencies and C is the sum of the C4 coordinate adjacencies. Commutativity and characteristic two give A^2=B, because each C3 adjacency squares to itself and each C4 adjacency squares to zero. For x=Ae_v, Ax=Be_v has support contained in x. Thus w_H(x)=|N(v)|=2d. Every all-short torus of dimension d>=3 consequently has distance exactly 2d. No general minimum-multiplicity classification for all-short mixtures is asserted here.

## Arbitrary-dimensional mixed-side consequence

The prior audited dimension-three classification proves that every dimension-three torus with side lengths at least three has distance at least six; if a side is at least five, its distance is seven and only singleton selections minimize. The all-short argument above supplies the corresponding lower bound 2d for every dimension d>=3.

Induct on D>=4. In a D-dimensional torus with at least one side L>=5, select that long side as the final Cartesian factor. Its (D-1)-dimensional cross-section H has degree h=2D-2. If H is all short, the preceding paragraph gives d(H)=h. If H has a long side, the inductive hypothesis gives d(H)=h+1. In both cases Lemma B applies, yielding

    d(C_(L1) square ... square C_(LD))=2D+1

whenever every Li>=3 and at least one Li>=5. For D>=3, every minimum selection is a singleton, so the multiplicity is N=product Li. The distance statement extends to D=2 by the prior results. Singleton uniqueness in D=2 has been established for mixed tori with a side 3 or 4, but must not be asserted for every D=2 torus: C5 square C5 has ten additional minimum selections. Dimension one also has distance three for L>=5, but singleton uniqueness fails at C5.

This proves, subject to independent audit, that requiring each individual side length to be at least five is unnecessary: one long side suffices in all dimensions. For D>=3 it is also necessary within the family Li>=3, since all-short tori have distance 2D. The small all-short dimension-two exceptions remain as in the separate mixed-side classification.

## Dependencies and limitations

The analytic Lemmas A and B are independent of torus structure and require only regularity and a lower bound on stabilizer distance. The all-short bases now follow from the published Hamming-code theorem and the analytic C3^2 square C4 proof. For the dimension-three induction base with two short directions and one long direction, analytic_profile_lemma.md proves the required lower bound directly for every cycle length, by occupied-path shapes and seven integer partitions. The separate dimension_two_analytic.md removes the D2 strip-enumeration dependency. Neither a finite certificate nor gap compression is needed in the final proof. The large three-dimensional scans, and the small cross-section graph enumerations, are independent corroboration only. The distinct check_profiles.py checks of Lemmas A and B remain sanity checks rather than proof dependencies.

An additional source check found that Proposition 2's proof explicitly gives the small dual-code distances 3,3,6 at a=1,2,3. Thus the C3^3 distance-six base is directly literature-supported through (5). The published proof uses a Magma a=4 base and small computational subcases. Our analytic C3^2 square C4 argument is independent of those computations.

Running `python3 research/higher_dimensions/check_profiles.py` checked 232,009 scalar profiles in approximately 1.18 seconds. These cover Lemma A's bounded profiles for h=2,4,6,8,10,12 and Lemma B's k<=4 nonsingleton profiles for h=6,8,10,12. Every tested C4 profile has lower bound at least h+2 and every tested long-cycle profile at least h+4. Exact counts and imported base records are in profile_checks.json. The unbounded-h proof is analytic; these checks are not extrapolated into a theorem.

The primary paper by Key and Rodrigues, "Binary codes from m-ary n-cubes Q_n^m," Advances in Mathematics of Communications 15 (2021), 507-524, https://www.aimsciences.org/article/doi/10.3934/amc.2020079, has an abstract stating exact binary adjacency-code and dual parameters for dimension n=2 and odd m. Its full general statements have not yet been audited for this extension. The author-hosted "Special LCD codes from products of graphs" by Fish, Key and Mwambene, https://www.math.clemson.edu/~keyj/Key/FKM16JRev.pdf, Theorem 1, proves preservation of the reflexive-LCD property under several graph products. That statement is not the stabilizer-distance lifting lemma proved above. The complete Cartesian-product section has now been inspected; its LCD-preservation and codeword-construction results do not supply this support-union lower bound. See priority_challenge.md. Another relevant source is Fish's 2017 "Binary codes and permutation decoding sets from the graph products of cycles," DOI 10.1007/s00200-016-0310-y; its full text was not inspected. Thus a broader priority check remains necessary, and this note does not assert novelty of Lemmas A or B.
