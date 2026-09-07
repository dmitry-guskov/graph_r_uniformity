"""Finite sanity checks of analytic slice-profile bounds; not a proof by sampling."""
from itertools import combinations, product
import json
import time
from pathlib import Path


def compositions(total, count):
    if count == 1:
        if total > 0:
            yield (total,)
        return
    for first in range(1, total - count + 2):
        for tail in compositions(total - first, count - 1):
            yield (first,) + tail


def lower_bound(values, h):
    out = 0
    for t, r in enumerate(values):
        left, right = values[t - 1], values[(t + 1) % len(values)]
        f = h + 1 if r == 1 else max(h, r)
        out += max(r, f - left - right) if r else abs(left - right)
    return out


def check_c4(h):
    count, minimum, witness = 0, 10**9, None
    for k in range(1, 5):
        for positions in combinations(range(4), k):
            for r in range(k, h + 2):
                for sizes in compositions(r, k):
                    values = [0] * 4
                    for t, size in zip(positions, sizes):
                        values[t] = size
                    w = lower_bound(values, h)
                    count += 1
                    if w < minimum:
                        minimum, witness = w, values
                    assert w >= h + 2, (h, values, w)
    return dict(h=h, profiles=count, minimum=minimum, witness=witness)


def check_long(h):
    count, minimum, witness = 0, 10**9, None
    # Gap length 2 represents every length >=2; internal extra empty slices
    # contribute zero. A compressed cycle below length 5 is admissible only
    # when a length-2 gap can be expanded to make the actual length >=5.
    for k in range(1, 5):
        for gaps in product((0, 1, 2), repeat=k):
            if k + sum(gaps) < 5 and 2 not in gaps:
                continue
            for r in range(max(2, k), h + 4):
                for sizes in compositions(r, k):
                    values = []
                    for size, gap in zip(sizes, gaps):
                        values.extend([size] + [0] * gap)
                    w = lower_bound(values, h)
                    count += 1
                    if w < minimum:
                        minimum, witness = w, values
                    assert w >= h + 4, (h, values, w)
    return dict(h=h, profiles=count, minimum=minimum, witness=witness)


start = time.perf_counter()
results = {
    'description': 'Finite checks of scalar inequalities only; analytic proof in higher_mixed_extension.md is the theorem.',
    'C4': [check_c4(h) for h in (2, 4, 6, 8, 10, 12)],
    'long_cycle': [check_long(h) for h in (6, 8, 10, 12)],
}
results['seconds'] = time.perf_counter() - start
base_path = Path(__file__).resolve().parents[1] / 'mixed_sides/results.json'
base_results = json.loads(base_path.read_text())
results['imported_bases'] = [
    dict(lengths=row['lengths'], distance=row['minimum_over_checked_r'],
         distance_certified=row['distance_certified'],
         minimum_multiplicity=row['minimum_multiplicity'])
    for row in base_results['mixed_graphs']
    if row['lengths'] in ([3, 3, 3], [3, 3, 4])
]
results['imported_base_source'] = str(base_path)
destination = Path(__file__).with_name('profile_checks.json')
destination.write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps(results, indent=2))
