"""Fix seeded fixed-partition ordering cases before construction."""

import json
import random
from pathlib import Path


def graph(n, edges, classes):
    return {"vertices":n,"edges":edges,"classes":classes}


EDGE_CASES = [
    (graph(0,[],[]),True),
    (graph(1,[],[0]),True),
    (graph(2,[],[0,0]),True),
    (graph(2,[[0,1]],[0,0]),True),
    (graph(3,[[0,1],[1,2]],[0,0,0]),True),
    (graph(3,[[0,1],[1,2],[0,2]],[0,0,0]),True),
    (graph(3,[],[0,0,0]),True),
    (graph(4,[[0,1],[1,2],[2,3]],[0]*4),True),
    (graph(4,[[0,1],[1,2],[2,3],[0,3]],[0]*4),False),
    (graph(4,[[0,1],[0,2],[0,3]],[0]*4),False),
    (graph(4,[[u,v] for u in range(4) for v in range(u+1,4)],[0]*4),True),
    (graph(4,[],[0]*4),True),
    (graph(4,[[0,1],[1,2],[2,3],[0,3]],[0,1,2,3]),True),
    (graph(5,[[0,1],[1,2],[2,3],[3,4],[0,4]],[0]*5),False),
    (graph(5,[[0,1],[1,2],[2,3],[3,4]],[0]*5),True),
    (graph(5,[[0,i] for i in range(1,5)],[0]*5),False),
    (graph(5,[],[0]*5),True),
]


def random_source(seed):
    rng = random.Random(seed)
    n = rng.randint(3,6)
    edges = [[u,v] for u in range(n) for v in range(u+1,n) if rng.random() < 0.48]
    if seed % 2 == 0:
        classes = list(range(n))
    else:
        classes = [0]*n
    return graph(n,edges,classes)


def build_cases():
    from check import solve_source
    cases, seen = [], set()

    def add(source,kind,seed=None,hand_answer=None):
        key = json.dumps(source,sort_keys=True,separators=(",", ":"))
        if key in seen:
            return False
        seen.add(key)
        answer = solve_source(source)
        if hand_answer is not None and ("order" in answer) != hand_answer:
            raise AssertionError(f"Hand label disagrees with oracle: {source}")
        case = {"source":source,"kind":kind,"expected":answer}
        if seed is not None:
            case["seed"] = seed
        cases.append(case)
        return True

    for source,expected in EDGE_CASES:
        add(source,"edge",hand_answer=expected)
    seed = 0
    while sum(case["kind"] == "random" for case in cases) < 100:
        add(random_source(seed),"random",seed=seed)
        seed += 1
    return cases


if __name__ == "__main__":
    path = Path(__file__).with_name("cases.json")
    cases = build_cases()
    path.write_text(json.dumps(cases,indent=2)+"\n")
    print(f"Wrote {len(cases)} cases to {path}")
