from itertools import combinations
from pathlib import Path
import json

def compositions(total,n):
 if n==1:
  if total>0: yield (total,)
  return
 for i in range(1,total-n+2):
  for c in compositions(total-i,n-1):yield (i,)+c

def neighbors(v,lens):
 out=set();s=1
 for l in lens:
  c=v//s%l
  for z in (-1,1):out.add(v+(((c+z)%l)-c)*s)
  s*=l
 return out

summary=[]
for lens in ([3,3],[3,4],[4,4]):
 n=lens[0]*lens[1]; A=[sum(1<<u for u in neighbors(v,lens)) for v in range(n)]
 f=[n+1]*8;f[0]=0
 for x in range(1,1<<n):
  r=x.bit_count()
  if r>7:continue
  z=0
  for i in range(n):
   if x>>i&1:z^=A[i]
  f[r]=min(f[r],(x|z).bit_count())
 unresolved=[];count=0; minima={}
 for L in range(5,15):
  for k in range((L+1)//2,8):
   if k>L:continue
   for P in combinations(range(L),k):
    p=set(P)
    if any(i not in p and (i+1)%L not in p for i in range(L)):continue
    for r in (6,7):
     for comp in compositions(r,k):
      v=[0]*L
      for i,x in zip(P,comp):v[i]=x
      bound=sum(max(x,f[x]-v[t-1]-v[(t+1)%L]) if x else abs(v[t-1]-v[(t+1)%L]) for t,x in enumerate(v))
      count+=1
      key=f'L{L}_r{r}'
      minima[key]=min(minima.get(key,999),bound)
      if bound<=7:unresolved.append({'L':L,'r':r,'slice_sizes':v,'lower_bound':bound})
 summary.append({'cross_section':lens,'f_by_cardinality':f,'no_gap_patterns_checked':count,'minimum_lower_bounds':minima,'unresolved':unresolved})
p=Path(__file__).with_name('projection_bounds.json');p.write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps([dict(cross_section=x['cross_section'],f=x['f_by_cardinality'],checked=x['no_gap_patterns_checked'],unresolved_count=len(x['unresolved']),unresolved_lengths=sorted(set(y['L'] for y in x['unresolved']))) for x in summary],indent=2))
