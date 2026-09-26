# Strongly consistent ordering with a given partition → Proper thinness with an input class budget

Category: Complexity open

## Source

The source gives a graph and a vertex partition. Its outputs are orders for which both the order and its reverse are consistent with the partition: if u<v<w, u and v share a class, and uw is an edge, then vw is an edge. Otherwise return NO-SOLUTION.

## Target

The source supplies a graph and vertex partition and asks for an order strongly consistent in both directions. The target supplies only a graph and a class budget, and asks for both a partition within that budget and such an order.

## Required result

Construct deterministic polynomial-time maps F and G: F sends every legal source instance to a legal target instance, and G(x,y) is a valid source output for every valid output y of F(x). Preserve the stated threshold, domain and promises. The requested complexity conclusion is NP-hardness for the stated target problem.

## Acceptance

Give explicit construction and recovery algorithms, a general proof for every legal input and every valid target output, and polynomial runtime and encoding-size bounds. Specify finite output encodings and handle NO-SOLUTION outputs when applicable. Tests compare recovered source outputs with independent source solutions.

## Why it matters

The question isolates the complexity contributed by choosing the partition in an ordering-based graph representation.

## Difficulty

The target may choose a different partition; forcing the intended classes without fixing them externally is the missing step.

## Literature context

Strong consistency with a supplied partition differs from finding both a partition and an order under a class budget.

Literature checked 2026-09-16. This summarizes the archived literature search on the date above. Unpublished, unindexed and overlooked work remains outside coverage; no new novelty assessment was performed.

## References

- [On the thinness and proper thinness of a graph](https://arxiv.org/abs/1704.00379): Bonomo and de Estrada, On the thinness and proper thinness of a graph, full preprint Theorem 5 (pp.8–10), proves the source NP-complete by Non-Betweenness. The forward source construction admits a strongly consistent order, not only a one-sided consistent order. Theorem 2 distinguishes the polynomial problem with a supplied order from this hard problem with a supplied partition.
- [Graph thinness: a lower bound and complexity](https://msp.org/pjm/2025/339-2/pjm-v339-n2-p07-s.pdf): Shitov, Graph thinness: a lower bound and complexity, Pacific Journal of Mathematics 339(2) (2025), 333–343, Theorem 3, establishes ordinary thinness hardness. Definition 11 and Lemmas 12–13 (pp.335–337) give the forcing pair B(G,U): two nonadjacent new vertices adjacent exactly to V(G) minus U. Lemma 13 extends a one-sided certificate by putting both new vertices last and in U's class. Definitions 14 and 22 and Section 4 compose these pairs and padding. None of these completeness statements establishes reverse consistency.
- [The 2025 primary preprint Trees with proper thinness 2](https://arxiv.org/abs/2505.11382): The 2025 primary preprint Trees with proper thinness 2: its introduction explicitly retains the complexity question for the proper variant after citing ordinary thinness hardness. Its tree-specific results do not settle general proper thinness. The 2025 author conference abstract, printed p.325, also retains fixed-two recognition as open; that is corroborative, not the sole evidence for the variable-budget target.
- [author conference abstract](https://sedici.unlp.edu.ar/bitstream/handle/10915/190942/Documento_completo.pdf?sequence=1): The 2025 primary preprint Trees with proper thinness 2: its introduction explicitly retains the complexity question for the proper variant after citing ordinary thinness hardness. Its tree-specific results do not settle general proper thinness. The 2025 author conference abstract, printed p.325, also retains fixed-two recognition as open; that is corroborative, not the sole evidence for the variable-budget target.

Fixed from board record `website/questions/proper-thinness.json` in board checkout at 6c7d3bd9c0a8f595279969a9c0a4d1853a3f5c17; the record was copied from the current working tree.
