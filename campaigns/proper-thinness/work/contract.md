# Prepared input and output contract

The source input is `{"vertices": n, "edges": [[u,v], ...], "classes":
[class_index, ...]}` with a simple undirected graph on `0..n-1` and one
class per vertex. Class labels are canonical nonnegative integers with no
gaps. A source output is `{"order": [vertices]}`. For every `u < v < w`
in that order, if `uw` is an edge, then `u` and `v` sharing a class requires
`vw` to be an edge, and `v` and `w` sharing a class requires `uv` to be an
edge. These are consistency of the order and its reverse. The alternative
`{"status": "NO-SOLUTION"}` is valid exactly when no order works.

The target input is `{"vertices": n, "edges": [[u,v], ...], "budget":
k}` with the same simple-graph rules and nonnegative class budget `k`.
A target output is `{"order": [vertices], "classes": [indices]}` with every
class index in `0..k-1` and the same two consistency conditions. Empty graphs
have a valid empty order and partition even when `k=0`.

A candidate `algorithm.py` reads source JSON from stdin and writes one legal
target JSON object to stdout. With `--extract`, it reads
`{"source": source, "target_solution": output}` and writes a valid source
output. The commands share no memory, exit nonzero on errors and send
diagnostics to stderr. They must be deterministic and polynomial time;
recovery must work for every valid target order and partition.

`check.py --candidate PATH` injects the fixed source corpus, solves targets
independently, and validates recovered source orders or negative decisions.
