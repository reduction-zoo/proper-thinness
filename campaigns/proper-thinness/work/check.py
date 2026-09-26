"""Independent strongly consistent ordering and proper-thinness oracles."""

import argparse
import json
import random
import subprocess
import sys
from itertools import permutations, product
from pathlib import Path

import z3


def legal_graph(n, edges):
    if type(n) is not int or n < 0 or not isinstance(edges,list):
        return False
    seen = set()
    for edge in edges:
        if (not isinstance(edge,list) or len(edge) != 2
                or any(type(v) is not int or not 0 <= v < n for v in edge)
                or edge[0] == edge[1]):
            return False
        key = tuple(sorted(edge))
        if key in seen:
            return False
        seen.add(key)
    return True


def canonical_classes(classes,n):
    return (isinstance(classes,list) and len(classes) == n
            and all(type(c) is int and c >= 0 for c in classes)
            and set(classes) == set(range(max(classes,default=-1)+1)))


def legal_source(source):
    return (isinstance(source,dict)
            and legal_graph(source.get("vertices"),source.get("edges"))
            and canonical_classes(source.get("classes"),source["vertices"]))


def legal_target(target):
    return (isinstance(target,dict)
            and legal_graph(target.get("vertices"),target.get("edges"))
            and type(target.get("budget")) is int and target["budget"] >= 0)


def direct_order(n,edges,classes,order):
    if not (isinstance(order,list) and len(order) == n
            and all(type(v) is int for v in order)
            and set(order) == set(range(n))):
        return False
    adjacent = {tuple(sorted(edge)) for edge in edges}
    for a in range(n):
        for b in range(a+1,n):
            for c in range(b+1,n):
                u,v,w = order[a],order[b],order[c]
                uw = tuple(sorted((u,w))) in adjacent
                if not uw:
                    continue
                if classes[u] == classes[v] and tuple(sorted((v,w))) not in adjacent:
                    return False
                if classes[v] == classes[w] and tuple(sorted((u,v))) not in adjacent:
                    return False
    return True


def solve_source(source):
    if not legal_source(source):
        raise ValueError("Illegal fixed-partition ordering instance")
    n = source["vertices"]
    for order in permutations(range(n)):
        if direct_order(n,source["edges"],source["classes"],list(order)):
            return {"order":list(order)}
    return {"status":"NO-SOLUTION"}


def valid_source(source,output):
    if not legal_source(source) or not isinstance(output,dict):
        return False
    if output == {"status":"NO-SOLUTION"}:
        return solve_source(source) == output
    return set(output) == {"order"} and direct_order(source["vertices"],source["edges"],source["classes"],output["order"])


def target_solutions(target,limit=3):
    if not legal_target(target):
        raise ValueError("Illegal proper-thinness instance")
    n,k = target["vertices"],target["budget"]
    ranks = [z3.Int(f"rank_{v}") for v in range(n)]
    classes = [z3.Int(f"class_{v}") for v in range(n)]
    solver = z3.Solver()
    if ranks:
        solver.add(z3.Distinct(*ranks))
    for r,c in zip(ranks,classes):
        solver.add(r >= 0,r < n,c >= 0,c < k)
    adjacent = {tuple(sorted(edge)) for edge in target["edges"]}
    for u,v,w in permutations(range(n),3):
        if tuple(sorted((u,w))) not in adjacent:
            continue
        in_order = z3.And(ranks[u] < ranks[v],ranks[v] < ranks[w])
        if tuple(sorted((v,w))) not in adjacent:
            solver.add(z3.Not(z3.And(in_order,classes[u] == classes[v])))
        if tuple(sorted((u,v))) not in adjacent:
            solver.add(z3.Not(z3.And(in_order,classes[v] == classes[w])))
    outputs = []
    flat = ranks+classes
    while len(outputs) < limit:
        result = solver.check()
        if result == z3.unsat:
            break
        if result != z3.sat:
            raise RuntimeError(f"Inconclusive target solver: {result}")
        model = solver.model()
        rank_values = [model.eval(r).as_long() for r in ranks]
        class_values = [model.eval(c).as_long() for c in classes]
        order = sorted(range(n),key=lambda v:rank_values[v])
        output = {"order":order,"classes":class_values}
        if not direct_order(n,target["edges"],class_values,order):
            raise AssertionError("Z3 output violates direct order predicate")
        outputs.append(output)
        solver.add(z3.Or(*[var != model.eval(var) for var in flat]))
    return outputs or [{"status":"NO-SOLUTION"}]


def solve_target(target):
    return target_solutions(target,1)[0]


def valid_target(target,output):
    if not legal_target(target) or not isinstance(output,dict):
        return False
    if output == {"status":"NO-SOLUTION"}:
        return solve_target(target) == output
    if set(output) != {"order","classes"}:
        return False
    classes = output["classes"]
    if not (isinstance(classes,list) and len(classes) == target["vertices"]
            and all(type(c) is int and 0 <= c < target["budget"] for c in classes)):
        return False
    return direct_order(target["vertices"],target["edges"],classes,output["order"])


def exhaustive_target(target):
    n,k = target["vertices"],target["budget"]
    for classes in product(range(k),repeat=n):
        for order in permutations(range(n)):
            if direct_order(n,target["edges"],classes,list(order)):
                return {"order":list(order),"classes":list(classes)}
    return {"status":"NO-SOLUTION"}


def self_test():
    from generate_cases import EDGE_CASES, random_source
    from test_oracle import test_hand_cases

    root = Path(__file__).resolve().parents[3]
    path = Path(__file__).with_name("cases.json")
    subprocess.run([sys.executable,str(root/"research/validate_preparation.py"),str(path)],check=True,cwd=root)
    cases = json.loads(path.read_text())
    for source,expected in EDGE_CASES:
        assert ("order" in solve_source(source)) == expected
    for case in cases:
        source = case["source"]
        if case["kind"] == "random":
            assert random_source(case["seed"]) == source
        current = solve_source(source)
        assert ("order" in current) == ("order" in case["expected"])
        assert valid_source(source,current) and valid_source(source,case["expected"])
    test_hand_cases()
    checked = 0
    for seed in range(64):
        rng = random.Random(seed)
        n = rng.randrange(5)
        edges = [[u,v] for u in range(n) for v in range(u+1,n) if rng.randrange(2)]
        for k in range(4):
            target = {"vertices":n,"edges":edges,"budget":k}
            assert ("order" in solve_target(target)) == ("order" in exhaustive_target(target))
            checked += 1
    print(f"Self-test passed: {len(cases)} independently labelled source cases and {checked} exhaustive target thresholds")


def candidate_check(path):
    self_test()
    cases = json.loads(Path(__file__).with_name("cases.json").read_text())
    recovered = 0
    for case in cases:
        source = case["source"]
        forward = subprocess.run([sys.executable,str(path)],input=json.dumps(source),text=True,capture_output=True,check=True)
        target = json.loads(forward.stdout)
        if not legal_target(target):
            raise AssertionError(f"Illegal proper-thinness target: {target}")
        for output in target_solutions(target):
            if not valid_target(target,output):
                raise AssertionError(f"Invalid target oracle output: {output}")
            payload = {"source":source,"target_solution":output}
            extraction = subprocess.run([sys.executable,str(path),"--extract"],input=json.dumps(payload),text=True,capture_output=True,check=True)
            recovered_output = json.loads(extraction.stdout)
            if not valid_source(source,recovered_output):
                raise AssertionError(f"Invalid recovery from {output}: {recovered_output}")
            recovered += 1
    print(f"Candidate check passed: {len(cases)} source cases, {recovered} target outputs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test",action="store_true")
    group.add_argument("--candidate",type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        candidate_check(args.candidate)
