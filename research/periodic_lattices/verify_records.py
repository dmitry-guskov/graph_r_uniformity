"""Independent set-based checks of C++ witnesses and finite proof ingredients."""
from pathlib import Path
from itertools import combinations, product
import json, math, time

ROOT = Path(__file__).resolve().parent

def neighbors(vertex, lengths):
    result = set()
    stride = 1
    for length in lengths:
        coordinate = vertex // stride % length
        for step in (-1, 1):
            result.add(vertex + (((coordinate + step) % length) - coordinate) * stride)
        stride *= length
    return result

def odd(selected, lengths):
    result = set()
    for vertex in selected:
        result.symmetric_difference_update(neighbors(vertex, lengths))
    return result

def run():
    started = time.perf_counter()
    record = json.loads((ROOT / 'enumeration_results.json').read_text())
    checked_witnesses = 0
    for graph in record['graphs']:
        lengths, n = graph['side_lengths'], graph['vertices']
        for row in graph['rows']:
            selected = set(row['witness_vertex_indices'])
            assert len(selected) == row['generator_subset_size']
            assert 0 in selected and all(0 <= v < n for v in selected)
            assert len(selected | odd(selected, lengths)) == row['minimum_weight']
            assert row['anchored_subsets'] == math.comb(n-1, len(selected)-1)
            checked_witnesses += 1
    projection_cases = 0
    no_gap_cases = {}
    for length in range(5, 31):
        for k in range(1, 5):
            for occupied_tuple in combinations(range(length), k):
                occupied = set(occupied_tuple)
                degrees = {u: ((u-1) % length in occupied) + ((u+1) % length in occupied) for u in occupied}
                if k == 4:
                    assert sum(2-d for d in degrees.values()) >= 2
                gap = any(u not in occupied and (u+1) % length not in occupied for u in range(length))
                if k <= 3 and not gap:
                    assert k == 3 and length in (5,6)
                    assert max(degrees.values()) <= 1
                    key = f'C{length}_occupied{k}'
                    no_gap_cases[key] = no_gap_cases.get(key, 0) + 1
                projection_cases += 1
    sharpness = []
    for dimension in range(1, 7):
        lengths = [4] * dimension
        selected = neighbors(0, lengths)
        o = odd(selected, lengths)
        assert len(selected) == 2 * dimension and not o
        sharpness.append({'side_lengths': lengths, 'generator_subset_size': len(selected), 'odd_neighborhood_size': len(o), 'weight': len(selected | o), 'witness_vertex_indices': sorted(selected)})
    # Directly test both diagonal slopes and their translates on C5 squared.
    diagonals = []
    for slope, offset in product((-1, 1), range(5)):
        selected = {t + 5*((slope*t+offset) % 5) for t in range(5)}
        assert not odd(selected, [5,5])
        diagonals.append(sorted(selected))
    assert len({tuple(s) for s in diagonals}) == 10
    return {'command': 'python3 research/periodic_lattices/verify_records.py', 'status': 'passed', 'independently_checked_cpp_witnesses': checked_witnesses, 'projection_lengths': [5,30], 'projection_cardinalities': [1,4], 'projection_cases': projection_cases, 'no_gap_projection_counts': no_gap_cases, 'C4_sharpness_witnesses': sharpness, 'C5_squared_nonsingleton_minimum_witnesses': diagonals, 'verification_seconds': time.perf_counter()-started, 'limits': 'This verifies recorded witnesses and finite combinatorial ingredients, not every enumerated C++ subset independently and not the infinite theorem.'}

if __name__ == '__main__':
    result = run()
    (ROOT / 'verification_results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
