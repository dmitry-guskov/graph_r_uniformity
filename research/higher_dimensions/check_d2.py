from itertools import combinations, permutations
import json
import time
from pathlib import Path

start = time.perf_counter()
N = 25
neighbors = []
for vertex in range(N):
    row, column = divmod(vertex, 5)
    neighbors.append(sum(1 << v for v in (
        5*((row+1)%5)+column, 5*((row-1)%5)+column,
        5*row+(column+1)%5, 5*row+(column-1)%5)))


def weight(selection):
    x = z = 0
    for vertex in selection:
        x |= 1 << vertex
        z ^= neighbors[vertex]
    return (x | z).bit_count()


records = []
for r in range(1, 6):
    minimum, count, checked = N+1, 0, 0
    for rest in combinations(range(1, N), r-1):
        checked += 1
        w = weight((0,)+rest)
        if w < minimum:
            minimum, count = w, 1
        elif w == minimum:
            count += 1
    assert N*count % r == 0
    records.append(dict(r=r, checked=checked, minimum=minimum,
                        anchored_minimizers=count,
                        global_fixed_r_minimizers=N*count//r))

actual = {p for p in permutations(range(5)) if weight(tuple(5*i+p[i] for i in range(5))) == 5}
predicted = {tuple((c+epsilon*i)%5 for i in range(5)) for c in range(5) for epsilon in (1,-1)}
assert actual == predicted and len(actual) == 10
assert sum(row['global_fixed_r_minimizers'] for row in records if row['minimum'] == 5) == 35
result = dict(records=records, total_anchored_subsets=sum(row['checked'] for row in records),
              permutations_checked=120, exceptional_permutations=[list(p) for p in sorted(actual)],
              minimum_multiplicity=35, seconds=time.perf_counter()-start)
Path(__file__).with_name('d2_checks.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
