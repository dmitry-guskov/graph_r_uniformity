# Exact graph state certification

For a simple graph with binary adjacency A, the graph-state Schmidt rank across S and its complement is 2 to the power rank_GF2(A[S, complement]). Its marginal on S is maximally mixed exactly when that binary rank equals the size of S. is_maximally_mixed implements this exact criterion. is_k_uniform checks every k-subset; uniformity_certificate additionally returns a failing cut and its rank. The exhaustive subset check is combinatorial in k, not an efficient general distance algorithm.

Graph.simplify remains a sufficient visual certificate. Failure is inconclusive: a full-rank 3 by 3 cut matrix can have no degree-one elimination pivot. Searches now use exact cut rank. Random graph sampling is not exhaustive enumeration of graphs, even in notebooks whose historical filenames say enumeration. Failure to find a graph does not prove nonexistence.

adjacency_matrix_binomial now samples each undirected edge once with the requested probability; the old construction implicitly required two Bernoulli successes. Pass seed for reproducibility. The regular-graph sampler also accepts seed. Mutating graph rules iterate over snapshots of the lists they change.

Four saved adjacency matrices were recovered from historical notebook text outputs and retained in data/recovered_graphs.json with baseline commit and cell provenance. Two have exact uniformity 4 and two have exact uniformity 3, as individually recorded. This is an independent certification of those matrices; the original random search was not reproduced. Updated search outputs were cleared. A k-uniform graph state must have minimum degree at least k, so any k-regular example attains the edge lower bound ceil(n*k/2) in the direct graph-state CZ preparation model. This does not establish novelty, minimum graph order, or optimal routed circuit depth.

Run `python -m pip install -r requirements-test.txt` then `python -m pytest tests -q`. Tests compare cut-rank certificates to independent graph-state partial traces, distinguish GF(2) rank from real rank, reproduce a peeling false negative and the six-vertex wheel, recertify all saved examples, and check sampling and failure witnesses.

The cut-rank and stabilizer-distance characterizations are established theory; see Cattaneo and Perdrix, https://arxiv.org/abs/1503.04702, and Sudevan et al., https://doi.org/10.1103/PhysRevA.108.022426. These changes repair the research tooling and do not constitute a new theorem.
