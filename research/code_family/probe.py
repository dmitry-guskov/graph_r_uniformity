from collections import Counter
from itertools import product,combinations
import hashlib,json,pathlib,time
BASE=pathlib.Path(__file__).resolve().parent

def main():
 start=time.perf_counter();sizes=(3,5);vertices=list(product(*(range(q) for q in sizes)));n=len(vertices);ix={v:i for i,v in enumerate(vertices)}
 A=[0]*n
 for i,v in enumerate(vertices):
  for axis,q in enumerate(sizes):
   for sign in (-1,1):
    w=list(v);w[axis]=(w[axis]+sign)%q;A[i]|=1<<ix[tuple(w)]
 assert n==15 and all(a.bit_count()==4 for a in A)
 # Published Table I graph: ZIZIIXIIZIZ, centered on X, offsets +/-3,+/-5.
 published_generator='ZIZIIXIIZIZ'
 offsets=sorted((j-published_generator.index('X'))%n for j,c in enumerate(published_generator) if c=='Z')
 permutation=[(5*a+3*b)%15 for a,b in vertices]
 assert len(set(permutation))==n and offsets==[3,5,10,12]
 for i,row in enumerate(A):
  actual={permutation[j] for j in range(n) if (row>>j)&1}
  expected={(permutation[i]+d)%n for d in offsets}
  assert actual==expected
 published_words=[sum(1<<t for t in range(n) if t%3==r) for r in range(3)]
 assert published_words[0]^published_words[1]^published_words[2]==(1<<n)-1
 published_overlap={'source':'Kovalev, Dumer, Pryadko, PRA 84, 062319 (2011), Example 12 and Table I',
  'graph_generator':published_generator,'circulant_offsets':offsets,'cartesian_to_circulant_permutation':permutation,
  'permutation_formula':'(a,b) -> (5*a+3*b) mod15','adjacency_equal':True,
  'published_classical_basis_hex':[hex(w) for w in published_words],
  'allones_in_published_classical_code':True,'conclusion':'Our repetition-word [[15,1,5]] is a subcode of the published [[15,3,5]] on the identical graph under this permutation.'}
 def image(x,z):
  for i in range(n):
   if (x>>i)&1:z^=A[i]
  return z
 def syn(c):return (c>>1)^(((1<<(n-1))-1) if c&1 else 0)
 def rank(rows):
  pivots={}
  for row in rows:
   while row:
    k=row.bit_length()-1
    if k in pivots:row^=pivots[k]
    else:pivots[k]=row;break
  return len(pivots)
 def sp(a,b):
  x,z=a&((1<<n)-1),a>>n;y,w=b&((1<<n)-1),b>>n
  return ((x&w).bit_count()+(z&y).bit_count())%2
 K=[(1<<i)|(A[i]<<n) for i in range(n)]
 S=[K[0]^K[i] for i in range(1,n)]
 logical_x=((1<<n)-1)<<n;logical_z=K[0]
 assert rank(K)==15 and rank(S)==14
 assert all(sp(a,b)==0 for a in S for b in S)
 assert all(sp(a,logical_x)==sp(a,logical_z)==0 for a in S)
 assert sp(logical_x,logical_z)==1 and rank(S+[logical_x,logical_z])==16
 assert (1|A[0]).bit_count()==5
 def label(x,z):return ''.join('Y' if (x>>i)&1 and (z>>i)&1 else 'X' if (x>>i)&1 else 'Z' if (z>>i)&1 else 'I' for i in range(n))
 single=[(syn(A[i]),syn(A[i]^(1<<i)),syn(1<<i)) for i in range(n)]
 seen={0:(0,0)};collisions=[];digest=hashlib.sha256();digest.update(bytes(6));counts={0:1}
 for weight in (1,2):
  count=0
  for support in combinations(range(n),weight):
   for ts in product(range(3),repeat=weight):
    x=z=s=0
    for i,t in zip(support,ts):
     s^=single[i][t]
     if t in (0,1):x|=1<<i
     if t in (1,2):z|=1<<i
    if s in seen:
     xx,zz=seen[s];fx,fz=x^xx,z^zz
     collisions.append({'first':label(xx,zz),'second':label(x,z),'product':label(fx,fz),'product_weight':(fx|fz).bit_count(),'classical_image':image(fx,fz),'syndrome':s,'product_support_coordinates':[vertices[i] for i in range(n) if ((fx|fz)>>i)&1]})
    else:seen[s]=(x,z)
    count+=1;digest.update(x.to_bytes(2,'little')+z.to_bytes(2,'little')+s.to_bytes(2,'little'))
  counts[weight]=count
 assert counts=={0:1,1:45,2:945}
 minimum=min((c['product_weight'] for c in collisions),default=None)
 # Independently enumerate increasing error weights until first logical witness.
 logical_witnesses=[];normalizer_min=None
 for weight in range(1,6):
  for support in combinations(range(n),weight):
   for ts in product(range(3),repeat=weight):
    x=z=0
    for i,t in zip(support,ts):
     if t in (0,1):x|=1<<i
     if t in (1,2):z|=1<<i
    c=image(x,z)
    if c not in (0,(1<<n)-1):continue
    if normalizer_min is None:normalizer_min=weight
    # S_even is zero-image and even x; otherwise this is a nontrivial logical.
    if c or x.bit_count()%2:
     logical_witnesses.append({'pauli':label(x,z),'weight':weight,'classical_image':c,'x_parity':x.bit_count()%2,'support_coordinates':[vertices[i] for i in support]})
     if len(logical_witnesses)>=10:break
   if len(logical_witnesses)>=10:break
  if logical_witnesses:break
 output={'published_overlap':published_overlap,'stabilizer_rank':rank(S),'graph_stabilizer_rank':rank(K),'normalizer_rank':rank(S+[logical_x,logical_z]),'stabilizer_commutes':True,'logical_pair_anticommutes':True,'canonical_logical_z':label(1,A[0]),'canonical_logical_z_weight':5,'sizes':sizes,'n':n,'degree':4,'vertex_order':'lexicographic (a,b), b fastest; leftmost label corresponds vertex0','enumerated_counts':counts,'total':sum(counts.values()),'distinct_syndromes':len(seen),'collision_count':len(collisions),'minimum_collision_product_weight':minimum,'example_collisions':sorted(collisions,key=lambda c:c['product_weight'])[:10],'independent_minimum_nontrivial_logical_weight':logical_witnesses[0]['weight'],'minimum_normalizer_weight':normalizer_min,'logical_witnesses':logical_witnesses,'canonical_error_syndrome_stream_sha256':digest.hexdigest(),'stream_contract':'weight0..2, lex supports and assignments X,Y,Z, x,z,s two little-endian bytes each, identity first','source_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'seconds':time.perf_counter()-start,'adjacency_hex':[hex(a) for a in A]}
 (BASE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items() if k not in ('adjacency_hex','example_collisions','logical_witnesses')},indent=2));print(json.dumps(logical_witnesses[:2],indent=2))
main()
