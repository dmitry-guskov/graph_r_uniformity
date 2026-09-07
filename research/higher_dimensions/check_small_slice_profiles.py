"""Portable finite support-profile certificate for short cross-sections.

Run with Python >=3.10. Outputs small_slice_profiles.json next to this file.
All arithmetic is exact integer arithmetic. Only cross-section graphs are
enumerated; no three-dimensional graph-generator subsets are enumerated.
"""
from itertools import combinations
from pathlib import Path
import json
import math
import platform
import time


def compositions(total, count):
    if count == 1:
        if total > 0:
            yield (total,)
        return
    for first in range(1, total - count + 2):
        for tail in compositions(total - first, count - 1):
            yield (first,) + tail


def cross_section_profile(lengths):
    n = math.prod(lengths)
    adjacency = []
    for vertex in range(n):
        neighbors = set()
        stride = 1
        for length in lengths:
            coordinate = vertex // stride % length
            for step in (-1, 1):
                neighbors.add(vertex + (((coordinate+step) % length)-coordinate)*stride)
            stride *= length
        adjacency.append(sum(1 << other for other in neighbors))
    minimum = [0] + [n+1]*7
    checked = 0
    for selection in range(1, 1 << n):
        size = selection.bit_count()
        if size > 7:
            continue
        checked += 1
        odd = 0
        remaining = selection
        while remaining:
            bit = remaining & -remaining
            odd ^= adjacency[bit.bit_length()-1]
            remaining ^= bit
        minimum[size] = min(minimum[size], (selection | odd).bit_count())
    assert checked == sum(math.comb(n, r) for r in range(1, 8))
    return minimum, checked


def profile_bound(values, minimum):
    result = 0
    for i, size in enumerate(values):
        left, right = values[i-1], values[(i+1) % len(values)]
        if size:
            result += max(size, minimum[size]-left-right)
        else:
            result += abs(left-right)
    return result


start = time.perf_counter()
# This lower profile is proved analytically, not supplied by graph enumeration.
# A singleton has weight 5; a pair has weight at least 6; w_H(x)>=|x|.
analytic_minimum = [0, 5, 6, 3, 4, 5, 6, 7]
rows, unresolved = [], []
for length in range(5, 16):
    for r in range(2, 8):
        checked, best, witness = 0, 10**9, None
        for k in range(1, min(length, r)+1):
            for positions in combinations(range(length), k):
                for sizes in compositions(r, k):
                    values = [0]*length
                    for position, size in zip(positions, sizes):
                        values[position] = size
                    bound = profile_bound(values, analytic_minimum)
                    checked += 1
                    if bound < best:
                        best, witness = bound, values
                    if bound <= 7:
                        unresolved.append(dict(length=length, r=r,
                                               values=values, bound=bound))
        assert checked == math.comb(length+r-1, r)
        rows.append(dict(length=length, r=r, profiles=checked,
                         minimum_bound=best, witness=witness))
assert not unresolved
certificate_seconds = time.perf_counter()-start

# Independent corroboration only; the proof certificate above never uses these.
corroboration = []
for lengths in ((3,3), (3,4), (4,4)):
    minimum, cross_checked = cross_section_profile(lengths)
    assert all(actual >= lower for actual, lower in zip(minimum, analytic_minimum))
    corroboration.append(dict(lengths=lengths, cross_section_subsets=cross_checked,
                              exact_f=minimum))
result = dict(description='Exact finite profile certificate with analytic lower profile; graph enumeration is independent corroboration only.',
              python=platform.python_version(), analytic_lower_profile=analytic_minimum,
              rows=rows, unresolved=unresolved,
              cross_section_corroboration=corroboration,
              certificate_seconds=certificate_seconds,
              seconds=time.perf_counter()-start,
              total_cross_section_subsets=sum(row['cross_section_subsets'] for row in corroboration),
              total_profiles=sum(row['profiles'] for row in rows))
Path(__file__).with_name('small_slice_profiles.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({key:value for key,value in result.items() if key != 'rows'}, indent=2))
print('Global minimum profile bound:', min(row['minimum_bound'] for row in rows))
