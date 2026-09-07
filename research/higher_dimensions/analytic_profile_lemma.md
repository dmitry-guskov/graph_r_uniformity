# Analytic replacement for the finite slice-profile certificate

Status: independently audited analytic proof draft. This replaces the 489,698-profile check as a proof dependency; that check remains independent corroboration. External mathematical review and priority checks remain open.

Let L>=5 and let r_0,...,r_(L-1) be nonnegative integers with 2<=r=sum r_t<=7. Set

    f(0)=0, f(1)=5, f(2)=6, and f(s)=s for 3<=s<=7,

and define the cyclic slice bound

    B = sum_(r_t>0) max(r_t, f(r_t)-r_(t-1)-r_(t+1))
        + sum_(r_t=0) |r_(t-1)-r_(t+1)|.

Then B>=8. In particular, no finite enumeration or reduction to finitely many cycle lengths is needed.

## General estimates

Let P be the occupied positions, k=|P|, and let deg_P(t) be the degree of t in the subgraph of C_L induced by P. Define

    delta = sum_(t in P) (2-deg_P(t)) r_t.

Discarding the maximum's first argument and the nonnegative empty contributions gives

    B >= sum_(t in P) f(r_t) - 2r + delta.                         (1)

Whenever k<L, the occupied induced graph is a disjoint union of paths, including isolated vertices as paths. Each component contributes at least two to delta. If delta=2, there is exactly one occupied path and both its endpoint cardinalities are one. We also use B>=r and f(s)>=3 for every occupied size s.

## One or two occupied positions

If k=1, its two empty neighbors are distinct and give B=f(r)+2r. This is ten when r=2 and at least nine when r>=3.

If k=2, with cardinalities a,b, each occupied position has a neighboring empty position whose other neighbor is empty. These two private empty neighbors are distinct. Indeed, adjacent occupied positions each have their outward neighbor, while nonadjacent positions have at most one common cycle neighbor when L>=5. Thus the empty-position contributions alone are at least a+b=r. If r>=4, the selected-cardinality terms give B>=2r>=8. If r=2 or 3, both a,b are at most two and f(a)=a+4, f(b)=b+4. The two occupied contributions are at least f(a)-b+f(b)-a=8, so B>=8+r>=10. This bound also holds when the occupied positions are not adjacent, because subtracting a nonexistent occupied-neighbor contribution only weakens the estimate.

## Three occupied positions

For k=3, the occupied subgraph has zero, one, or two edges, since L>=5.

With zero edges, the three occupied contributions are their unperturbed f-values, totaling at least nine.

With one edge, let its endpoint cardinalities be a,b and let the isolated cardinality be c. The edge contributes at least

    g(a,b)=max(a,f(a)-b)+max(b,f(b)-a).

For a+b>=5, g(a,b)>=a+b>=5. For a+b<=4, the unordered positive pairs are (1,1), (1,2), (1,3), (2,2); their g-values are respectively 8,8,5,8. Hence g(a,b)>=5 in every case. The isolated occupied position contributes f(c)>=3, proving B>=8 without using any empty-position contribution.

With two edges, the occupied positions form a three-position consecutive path. Write its cardinalities as a,b,c, with b in the middle, and put u=a+c. Because L>=5, the two outward empty neighbors of this path are distinct and each has only one occupied neighbor; together they contribute u. Keeping the selected-cardinality contribution b in the middle gives

    B >= u+b+max(a,f(a)-b)+max(c,f(c)-b).                          (2)

If u>=4, the two maxima contribute at least a+c=u, so B>=2u+b>=9. If u=2, then a=c=1 and (2) gives

    B >= 2+b+2max(1,5-b).

For b<=3 this is at least 12-b>=9; for b>=4 it is at least b+4>=8. If u=3, the endpoint sizes are one and two, so

    B >= 3+b+max(1,5-b)+max(2,6-b).

For b<=4 this is at least 14-b>=10. For b>=5 it is at least b+6>=11. This completes k=3.

## Four occupied positions

Now k=4<L, so delta>=2. The positive cardinalities have total at most seven. Their only unordered partitions are

    (1,1,1,1), (2,1,1,1), (3,1,1,1), (2,2,1,1),
    (4,1,1,1), (3,2,1,1), (2,2,2,1).

For these partitions, the right-hand side sum f(r_t)-2r+2 of (1) is respectively

    14, 13, 8, 12, 7, 7, 11.

Only the two partitions with preliminary bound seven remain. For either of them, sum f(r_t)-2r=5. If delta>=3, (1) already gives B>=8. If delta=2, the four occupied positions form one path with both endpoint sizes one. Up to reversal, their cardinality profiles must therefore be (1,4,1,1) or (1,3,2,1). In the first case the four occupied contributions are at least (1,4,1,4), totaling ten. In the second they are at least (2,3,2,3), also totaling ten. These follow directly from each occupied term's maximum in B, with zero outside the path. Empty contributions can only increase the bound. Thus k=4 also gives B>=8.

This is an explicit classification of seven integer partitions, with their bounds derived from (1); it is not a computer-enumerated profile table.

## At least five occupied positions

Since r<=7 and k>=5, every occupied size is at most three, and at most one size is three. Sizes one and two have f-values at least five, while f(3)=3. Consequently

    sum_(t in P) f(r_t) >= 5k-2.

Using delta>=0 in (1),

    B >= 5k-2-2r >= 5k-16 >= 9.

All values of k have been covered, establishing B>=8. QED.

## Scope and dependency change

The already established graph-to-profile inequality applies to H square C_L for each short cross-section H in {C3 square C3, C3 square C4, C4 square C4}. For these H, singleton weight five and pair weight at least six follow from the degree and common-neighbor counts, and all larger selections have weight at least their cardinality. Hence the f above is an analytic lower profile.

If a nonsingleton selection in H square C_L had weight at most seven, its cardinality would lie between two and seven. The proved inequality would force its weight to be at least eight. A singleton attains seven. Thus the three dimension-three families have distance seven and singleton minimum selections for every L>=5, by a direct analytic argument.

This lemma removes both the finite scalar-profile check and the empty-gap compression from the proof dependencies of those families. The existing 489,698-profile certificate, small cross-section enumerations, and larger graph scans remain independent corroboration. The original higher-dimensional Lemmas A and B and the other prior analytic arguments are unchanged. The published Hamming-code theorem remains an external dependency for the arbitrary-dimensional all-short induction; its published computational subcases should still be accurately attributed.
