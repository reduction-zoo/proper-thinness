from check import legal_source, solve_source, valid_source, legal_target, solve_target, valid_target


def test_hand_cases():
    cycle = {"vertices":4,"edges":[[0,1],[1,2],[2,3],[0,3]],"classes":[0,0,0,0]}
    assert solve_source(cycle) == {"status":"NO-SOLUTION"}
    assert not valid_source(cycle,{"order":[0,1,2,3]})
    empty = {"vertices":0,"edges":[],"classes":[]}
    assert solve_source(empty) == {"order":[]}
    assert not legal_source({"vertices":2,"edges":[[0,1]],"classes":[0]})
    target = {"vertices":4,"edges":cycle["edges"],"budget":1}
    assert solve_target(target) == {"status":"NO-SOLUTION"}
    assert "order" in solve_target({**target,"budget":2})
    assert not valid_target(target,{"order":[0,1,2,3],"classes":[0,0,0,0]})


if __name__ == "__main__":
    test_hand_cases()
