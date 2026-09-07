# Periodic graph states: current research result

Assessment: this is the strongest research direction found in the four repositories. There is now a concrete proof candidate, an editable TeX/PDF draft, finite proof certificates, independent exact graph enumeration, and a checked quantum-code application. The mathematical claims have been checked within this session; external proof review and publication priority remain open. The repository's historical graphical rewrite rules are not used as the authority for these distance claims.

## Statement and conventions

Let G be the simple Cartesian product of cycles C_(L1) through C_(LD), with every Li at least three. A nonempty graph-generator selection S has stabilizer weight W(S)=|S union Odd(S)|. Its minimum d(G) is one more than the graph state's exact uniformity. Multiplicity counts stabilizer elements, not orbits or supports modulo local Clifford operations.

For D at least three, the proof draft establishes d(G)=2D when every side is three or four, and d(G)=2D+1 when at least one side is at least five. In the latter case the only minimum elements are the N canonical graph generators. Thus one long side is sufficient and necessary for full 2D-uniformity within this family. For the all-short family, no arbitrary-dimensional minimum-multiplicity classification is claimed.

For D=2 with at least one long side, d(G)=5 and the minimum multiplicity is N, except at C5 square C5, where it is 35: the 25 generators and ten diagonal selections. The all-short distance/multiplicity pairs are (3,6) for C3 square C3, (4,18) for C3 square C4, and (4,28) for C4 square C4. All-short D3 distances are six; their multiplicities are 117, 48, 48 and 64 for C3 cubed, C3 squared square C4, C3 square C4 squared, and C4 cubed.

## Read the proof and its dependencies

The consolidated [proof PDF](periodic_lattices/periodic_cluster_distance.pdf) is built from [the main TeX source](periodic_lattices/periodic_cluster_distance.tex) and [the mixed-side extension](periodic_lattices/mixed_side_extension.tex). The all-sides-at-least-five theorem has an analytic extremal-support and slicing proof. Two general lifting lemmas then extend a regular cross-section with distance at least its degree through C4 or a long cycle. The all-triangle base uses the published binary Hamming-graph code theorem of Fish, Key and Mwambene; the C3 squared square C4 base is proved analytically.

The final mixed-side proof is analytic, conditional only on the explicitly cited published Hamming-graph code theorem. The [analytic profile lemma](higher_dimensions/analytic_profile_lemma.md) rules out every nonsingleton of weight at most seven in the D3 products with two short directions, by occupied-path shapes and seven elementary cardinality partitions. The [analytic D2 proof](higher_dimensions/dimension_two_analytic.md) treats every cycle C_a with a>=3 times a long cycle, including the complete C5 squared exception. These replace the earlier finite checks and compression reductions as proof dependencies. The published Hamming-code theorem itself includes computational subcases in its published proof; those are attributed to that source.

The [higher-dimensional argument](higher_dimensions/higher_mixed_extension.md) gives the abstract lifting lemmas and induction. The earlier [base simplification](higher_dimensions/short_base_simplification.md), [D2 projection argument](higher_dimensions/d2_minimum_correction.md), and [mixed-side enumeration note](mixed_sides/mixed_side_extension.md) are retained as supporting derivations and evidence, with their superseded dependency status explicit. The 489,698-profile certificate and all graph scans now provide independent corroboration.

An independently written readable C++ enumerator rechecked 4,857,170,093 anchored subsets in about 107 seconds in the recorded run. That includes the complete C5 cubed search through generator cardinality seven: 4,700,324,626 anchored subsets, distance seven and 125 minimum elements. `torus_recheck.json` preserves all counts, witnesses, times and source/binary hashes. Translation transitivity justifies anchoring; W(S)>=|S| justifies the cardinality cutoff. This is independent numerical corroboration, not the reason the arbitrary-dimensional theorem holds. The original separate enumerator's 7.40-billion-subset mixed-side run is also preserved.

## Novelty boundaries

The equal-side D2 distance-five family was already stated by [Kovalev, Dumer and Pryadko (2011), Example 6](https://link.aps.org/accepted/10.1103/PhysRevA.84.062319). [Sudevan and Das (2022)](https://arxiv.org/abs/2201.05622) also cover unequal D2 sides at least five and exhibit a diagonal minimum on C5 square C5. The 2023 cluster-state paper proves a sufficient threshold eight and conjectures five; the [2025 version of the CWS follow-up](https://arxiv.org/html/2405.06142v4) retains the side-at-least-eight sufficient condition. The comparison supports investigating the stronger mixed-side theorem; it does not establish its priority.

The [priority challenge](higher_dimensions/priority_challenge.md) records inspected primary statements, including the Hamming-graph code results and the complete Cartesian section of the LCD product paper. The full 2017 Fish cycle-product paper and the full result behind a 2019 JMM diagonal-distance abstract remain concrete unresolved leads. A paper should center on the mixed-side theorem, the abstract lifting lemmas, or the minimum classification only after those overlaps and independent proof review have been addressed.

## Code application

The 3-by-3-by-5 graph gives the pure [[45,1,7]] code span{|G>, Z_all|G>}, with checks K_0 K_v. The [independent verifier](code_application/verify_code.py) checks rank 44, commuting checks, anticommuting logicals, and all 392,176 Pauli errors of weight at most three. Every syndrome is distinct. Splitting any weight-at-most-six Pauli into two such errors proves purity and distance at least seven; a canonical generator is a weight-seven logical and proves equality. This finite code verification also independently certifies the graph-state distance of that instance.

Conditional on the general graph theorem, the established CWS conversion gives [[5 times 3^(D-1),1,2D+1]] for D at least three; the five-qubit case is familiar. The 15-qubit case is explicitly a subcode of the published [[15,3,5]] construction: [the exact check](code_family/NOTE.md) verifies the graph permutation and classical-word inclusion. No novelty, best-code parameters, fault-tolerant implementation, or fixed-dimensional asymptotic locality is claimed for this family.

## Reproduction

Run from the repository root. The corroboration and code scripts require only the Python standard library; ordinary repository tests use `requirements-test.txt`. The exact enumerator requires a C++17 compiler. The large optional check took roughly two minutes on the development machine; default checks are smaller. Outputs are written next to the scripts unless an output path is supplied.

```sh
python -m pytest -q
python research/higher_dimensions/check_small_slice_profiles.py
python research/higher_dimensions/check_d2.py
python research/code_application/verify_code.py
python research/code_family/probe.py
clang++ -O3 -std=c++17 research/enumerate_tori.cpp -o /tmp/enumerate_tori
python research/reproduce_torus_checks.py --binary /tmp/enumerate_tori --output /tmp/torus_recheck.json
python research/reproduce_torus_checks.py --binary /tmp/enumerate_tori --include-large --output /tmp/torus_recheck_large.json
```

Build the PDF with `tectonic research/periodic_lattices/periodic_cluster_distance.tex`. Tectonic may download standard TeX resources on its first build. `manifest.json` records current committed-artifact checksums; original-package provenance files retain earlier source hashes and are explicitly historical. Runtimes and environment metadata can change on reproduction, while counts and binary witnesses should agree exactly.
