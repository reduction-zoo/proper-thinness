# Preparation evidence

Prepared on 2026-09-26 before constructing a candidate. The fixed corpus has
117 distinct legal fixed-partition graph instances: 17 hand-labelled edge
cases and 100 seeded random cases, with 97 YES and 20 NO decisions and zero
to six vertices. `generate_cases.py` retains the generator and seeds;
`cases.json` stores independently checked orders or NO-SOLUTION. The source
oracle enumerates all vertex orders. Each returned order is checked directly
against every three-position consistency condition; exhausting all orders
establishes a negative answer in this finite domain. Hand cases include
paths and cliques that pass, and same-class claws and induced cycles that
fail.

The target oracle uses Z3 4.16.0 with a distinct integer rank per vertex
and a bounded integer class label. For each graph edge `uw` and distinct
middle vertex `v`, it excludes exactly those `u<v<w` rank patterns whose
missing `vw` or `uv` edge violates one of the two consistency implications.
Every satisfying model is checked again by direct triple enumeration.
UNSAT is conclusive; unknown is an error. Independent enumeration of class
assignments and orders agreed with Z3 on 256 small graph and budget
combinations, including empty graphs and zero budgets. Hand fixtures cover
a four-cycle obstruction, successful two-class allocation, malformed input
and invalid negative output.

Reproduce from the repository root:

```sh
uv sync --locked
uv run --locked python campaigns/proper-thinness/work/check.py --self-test
```

The self-test starts with the corpus gate, regenerates random cases,
rechecks every source answer, and runs the independent target comparison.
The candidate runner uses separate forward and recovery subprocesses and
up to three target partitions/orders per case. An incorrect injected
candidate was rejected after target solving and source validation. No
actual reduction candidate exists; these finite checks do not establish
hardness or a general reduction.
