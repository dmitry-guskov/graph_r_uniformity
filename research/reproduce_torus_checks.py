"""Independent portable recheck with the readable C++ enumerator.

Run: python research/reproduce_torus_checks.py --binary /tmp/enumerate_tori
Add --include-large for the125-qubit minimum-multiplicity enumeration (~minutes).
This script verifies finite claims; infinite claims also require the proof notes.
"""
import argparse
import hashlib
import json
from math import comb
from pathlib import Path
import subprocess
import time

ROOT=Path(__file__).resolve().parent

def neighbors(v,lengths):
    result=set(); stride=1
    for length in lengths:
        coordinate=v//stride%length
        for step in (-1,1):
            result.add(v+(((coordinate+step)%length)-coordinate)*stride)
        stride*=length
    return result


def run_case(binary,lengths,max_size):
    command=[str(binary),str(max_size),*map(str,lengths)]
    result=json.loads(subprocess.check_output(command,text=True))
    n=result['vertices']
    for row in result['rows']:
        assert row['anchored_subsets']==comb(n-1,row['r']-1)
        chosen=set(row['witness']); odd=set()
        for v in chosen: odd.symmetric_difference_update(neighbors(v,lengths))
        assert len(chosen)==row['r'] and len(chosen|odd)==row['minimum_weight']
        assert n*row['anchored_minimizers']%row['r']==0
        row['global_minimizers_of_fixed_cardinality']=n*row['anchored_minimizers']//row['r']
    result['command']=command
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary',type=Path,required=True)
    parser.add_argument('--include-large',action='store_true')
    parser.add_argument('--output',type=Path,default=ROOT/'torus_recheck.json')
    args=parser.parse_args()
    cases=[([5,5],5)]
    cases += [([a,L],5) for a in (3,4) for L in range(5,12)]
    cases += [([a,b,L],5) for a,b in ((3,3),(3,4),(4,4)) for L in range(5,12)]
    cases += [([3,3],3),([3,4],4),([4,4],4)]
    cases += [([3,3,3],6),([3,3,4],6),([3,4,4],6),([4,4,4],6)]
    if args.include_large: cases += [([5,5,5],7)]
    start=time.perf_counter(); rows=[]
    for lengths,max_size in cases:
        result=run_case(args.binary,lengths,max_size)
        distance=min(row['minimum_weight'] for row in result['rows'])
        if max(lengths)>=5:
            assert distance==2*len(lengths)+1
            if min(lengths)<5 or len(lengths)>=3:
                assert all(row['minimum_weight']>distance for row in result['rows'][1:])
        else:
            expected=3 if lengths==[3,3] else 2*len(lengths)
            assert distance==expected
        rows.append(result)
        print(f'{lengths}: checked through size{max_size}, minimum{distance}',flush=True)
    out={'status':'passed','graphs':rows,'total_anchored_subsets':sum(row['anchored_subsets'] for g in rows for row in g['rows']),
         'seconds':time.perf_counter()-start,'source_sha256':hashlib.sha256((ROOT/'enumerate_tori.cpp').read_bytes()).hexdigest(),
         'binary_sha256':hashlib.sha256(args.binary.read_bytes()).hexdigest(),
         'scope':'Independent exact recheck of finite enumeration, counts and witnesses. Infinite conclusions additionally require the cited proof reductions.'}
    args.output.write_text(json.dumps(out,indent=2)+'\n')


if __name__=='__main__': main()
