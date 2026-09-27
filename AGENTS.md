# Research instructions

Read the [fixed question](campaigns/proper-thinness/question.md), [prior state](campaigns/proper-thinness/state.md) and [preparation notes](campaigns/proper-thinness/work/preparation.md). The fixed [test corpus](campaigns/proper-thinness/work/cases.json) and [verifier](campaigns/proper-thinness/work/check.py) are the starting evidence; the preparation notes state their coverage and any pending checks.

Run `uv sync --locked`, then `uv run --locked python campaigns/proper-thinness/work/check.py --self-test` before relying on that evidence. Follow the current user's AutoResearch pipeline. Preserve prior evidence, commit new work incrementally and make only evidence-backed claims.
