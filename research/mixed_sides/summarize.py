from pathlib import Path
from itertools import combinations, product
import json, re, math, hashlib, subprocess
ROOT=Path(__file__).resolve().parent

def neighbors(v,lens):
 out=set();s=1
 for L in lens:
  c=v//s%L
  for step in (-1,1):out.add(v+(((c+step)%L)-c)*s)
  s*=L
 return out

def parse(path):
 graphs=[]
 for line in path.read_text().splitlines():
  if line.startswith('lens'):
   ls,n=line[5:].split(' N=');g={'lengths':list(map(int,ls.split())),'N':int(n),'rows':[]};graphs.append(g)
  else:
   match=re.fullmatch(r'r=(\d+) anchored_subsets=(\d+) minimum_weight=(\d+) anchored_minimizers=(\d+) witness=([\d,]+) seconds=([\d.e+-]+)',line)
   r,c,w,a,ss,t=match.groups();r,c,w,a=map(int,(r,c,w,a));S=set(map(int,ss.strip(',').split(',')));o=set()
   for v in S:o.symmetric_difference_update(neighbors(v,g['lengths']))
   assert len(S)==r and len(S|o)==w and c==math.comb(g['N']-1,r-1)
   assert g['N']*a%r==0
   g['rows'].append({'r':r,'anchored_subsets':c,'minimum_weight':w,'anchored_minimizers':a,'global_minimizers_fixed_r':g['N']*a//r,'witness':sorted(S),'seconds':float(t)})
 for g in graphs:
  g['minimum_over_checked_r']=min(row['minimum_weight'] for row in g['rows'])
  g['distance_certified']=max(row['r'] for row in g['rows'])>=g['minimum_over_checked_r']
  g['minimum_multiplicity']=sum(row['global_minimizers_fixed_r'] for row in g['rows'] if row['minimum_weight']==g['minimum_over_checked_r']) if g['distance_certified'] else None
 return graphs
mixed=parse(ROOT/'mixed_enumeration.txt');cross=parse(ROOT/'cross_section_enumeration.txt')
for g in mixed:
 if len(g['lengths'])==2 and max(g['lengths'])>=5:
  assert g['minimum_over_checked_r']==5 and g['minimum_multiplicity']==g['N']
 if len(g['lengths'])==3 and max(g['lengths'])>=5:
  assert g['minimum_over_checked_r']==7 and g['minimum_multiplicity']==g['N']
for g in cross:
 assert g['rows'][0]['minimum_weight']==7
 assert all(row['minimum_weight']>7 for row in g['rows'][1:])
# Independently enumerate all global minimum supports in C3 cubed and categorize distances.
lens=[3,3,3];adj=[sum(1<<w for w in neighbors(v,lens)) for v in range(27)];classes={};sets=[]
for S in combinations(range(27),6):
 x=sum(1<<v for v in S);z=0
 for v in S:z^=adj[v]
 if (x|z).bit_count()!=6:continue
 coords=[(v%3,v//3%3,v//9) for v in S]
 hist=[sum(sum(a!=b for a,b in zip(u,v))==d for u,v in combinations(coords,2)) for d in (1,2,3)]
 key=str(hist);classes[key]=classes.get(key,0)+1
 sets.append(list(S))
assert len(sets)==117
encode=lambda x:x[0]+3*x[1]+9*x[2]
A={tuple(sorted(neighbors(v,[3,3,3]))) for v in range(27)}
B=set()
for axis in range(3):
 remaining=[i for i in range(3) if i!=axis]
 for pair in combinations(range(3),2):
  for slope,offset in product((1,2),range(3)):
   S=[]
   for t,c in product(range(3),pair):
    x=[0]*3;x[axis]=c;x[remaining[0]]=t;x[remaining[1]]=(slope*t+offset)%3;S.append(encode(x))
   B.add(tuple(sorted(S)))
C=set()
for a1,a2 in product((1,2),repeat=2):
 normal=(1,a1,a2)
 for c in range(3):
  plane={x for x in product(range(3),repeat=3) if sum(a*b for a,b in zip(normal,x))%3==c}
  for u in plane:
   line={tuple((u[i]+t*normal[i])%3 for i in range(3)) for t in range(3)}
   C.add(tuple(sorted(encode(x) for x in plane-line)))
assert len(A)==27 and len(B)==54 and len(C)==36
assert A.isdisjoint(B) and A.isdisjoint(C) and B.isdisjoint(C)
assert A|B|C=={tuple(x) for x in sets}

out={'date':'2026-09-06','compiler':subprocess.check_output(['clang++','--version'],text=True).strip(),'mixed_graphs':mixed,'cross_section_graphs':cross,'total_cpp_anchored_subsets':sum(r['anchored_subsets'] for g in mixed+cross for r in g['rows']),'summed_cpp_enumeration_seconds':sum(r['seconds'] for g in mixed+cross for r in g['rows']),'independent_C3_cubed_minimum_support_count':len(sets),'C3_cubed_minimum_pair_distance_histograms':classes,'C3_cubed_constructive_classification':{'neighborhoods':len(A),'two_coordinate_diagonal_times_pair':len(B),'affine_plane_minus_parallel_full_diagonal':len(C),'constructed_family_equals_all_exact_minima':True},'independently_verified_witness_count':sum(len(g['rows']) for g in mixed+cross),'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('*.cpp')},'log_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('*enumeration.txt')},'verification':'All anchored counts checked against binomial; every reported witness independently checked using neighbor sets; all claimed finite distance/multiplicity values checked.','limitations':'Infinite mixed-side theorem requires the separate compression and slice-bound arguments. No novelty claim for this extension has been researched.'}
(ROOT/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('mixed_graphs','cross_section_graphs','compiler','source_sha256','log_sha256')},indent=2))
