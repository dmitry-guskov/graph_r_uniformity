#!/usr/bin/env python3
"""Exact binary verification of the C3 square C3 square C5 repetition CWS code.
No statevectors, floating arithmetic, randomized tests, or external packages.
"""
from collections import Counter,deque
from itertools import combinations,product
import hashlib,json,math,pathlib,time
BASE=pathlib.Path(__file__).resolve().parent

def rank(rows):
    piv={}
    for row in rows:
        while row:
            bit=row.bit_length()-1
            if bit in piv:row^=piv[bit]
            else:piv[bit]=row;break
    return len(piv)

def sp(a,b):
    x,z=a;xx,zz=b
    return ((x&zz).bit_count()+(z&xx).bit_count())%2

def encode(a,n):return a[0]|(a[1]<<n)

def main():
    start=time.perf_counter();sizes=(3,3,5)
    vertices=list(product(*(range(q) for q in sizes)));n=len(vertices);index={v:i for i,v in enumerate(vertices)}
    adjacency=[0]*n;edges=set()
    for i,v in enumerate(vertices):
        for axis,q in enumerate(sizes):
            for sign in (-1,1):
                other=list(v);other[axis]=(other[axis]+sign)%q;j=index[tuple(other)]
                adjacency[i]|=1<<j;edges.add(tuple(sorted((i,j))))
    assert n==45 and len(edges)==135 and all(row.bit_count()==6 for row in adjacency)
    assert all(not (row>>i)&1 for i,row in enumerate(adjacency))
    assert all(((adjacency[i]>>j)^(adjacency[j]>>i))&1==0 for i in range(n) for j in range(n))
    K=[(1<<i,adjacency[i]) for i in range(n)]
    assert rank([encode(k,n) for k in K])==45
    assert all(sp(a,b)==0 for a,b in combinations(K,2))
    star=[(K[0][0]^K[v][0],K[0][1]^K[v][1]) for v in range(1,n)]
    tree=[];seen={0};queue=deque([0])
    while queue:
        u=queue.popleft()
        for v in range(n):
            if (adjacency[u]>>v)&1 and v not in seen:
                seen.add(v);queue.append(v);tree.append((u,v))
    tree_rows=[(K[u][0]^K[v][0],K[u][1]^K[v][1]) for u,v in tree]
    star_rank=rank([encode(row,n) for row in star]);tree_rank=rank([encode(row,n) for row in tree_rows]);union_rank=rank([encode(row,n) for row in star+tree_rows])
    assert (star_rank,tree_rank,union_rank)==(44,44,44)
    assert all(sp(a,b)==0 for a,b in combinations(star,2))
    allones=(1<<n)-1;logical_x=(0,allones);logical_z=K[0]
    assert all(sp(row,logical_x)==sp(row,logical_z)==0 for row in star)
    assert sp(logical_x,logical_z)==1
    assert rank([encode(row,n) for row in star+[logical_x,logical_z]])==46
    assert (logical_z[0]|logical_z[1]).bit_count()==7
    # Packed syndrome against K_0 K_v, v=1..44.
    def syndrome_from_image(c):
        return (c>>1)^(((1<<(n-1))-1) if c&1 else 0)
    single=[]
    for i in range(n):
        sx=syndrome_from_image(adjacency[i]);sz=syndrome_from_image(1<<i)
        single.append((sx,sx^sz,sz)) # X, Y, Z
        for masks,syn in [((1<<i,0),sx),((1<<i,1<<i),sx^sz),((0,1<<i),sz)]:
            direct=sum(sp(masks,row)<<j for j,row in enumerate(star))
            assert syn==direct
    seen_syndromes={0:(0,0)};digest=hashlib.sha256();digest.update(bytes(18))
    counts={0:1};collisions=[]
    for weight in range(1,4):
        count=0
        for support in combinations(range(n),weight):
            for assignments in product(range(3),repeat=weight):
                syndrome=0;x=z=0
                for i,t in zip(support,assignments):
                    syndrome^=single[i][t]
                    if t in (0,1):x|=1<<i
                    if t in (1,2):z|=1<<i
                if syndrome in seen_syndromes:
                    collisions.append({'first_masks':seen_syndromes[syndrome],'second_masks':[x,z],'syndrome':syndrome})
                else:seen_syndromes[syndrome]=(x,z)
                # Canonical ordered record: x,z,syndrome, six little-endian bytes each.
                digest.update(x.to_bytes(6,'little'));digest.update(z.to_bytes(6,'little'));digest.update(syndrome.to_bytes(6,'little'))
                count+=1
        assert count==math.comb(n,weight)*3**weight
        counts[weight]=count
    assert sum(counts.values())==392176
    assert not collisions and len(seen_syndromes)==392176
    # All 135 geometrically neighboring pair products remain valid checks.
    edge_check_weights=Counter((K[u][0]^K[v][0]|K[u][1]^K[v][1]).bit_count() for u,v in sorted(edges))
    tree_check_weights=Counter((x|z).bit_count() for x,z in tree_rows)
    out={'lattice_sizes':sizes,'vertex_order':'lexicographic tuples (a,b,c), c fastest; bit i corresponds to vertex i','n':n,'edges':len(edges),'degree':6,'graph_generator_rank':45,'star_check_rank':star_rank,'spanning_tree_check_rank':tree_rank,'union_check_rank':union_rank,'normalizer_basis_rank':46,'logical_x_masks':[0,allones],'logical_z_masks':list(logical_z),'logical_z_weight':7,'all_single_pauli_syndrome_formula_checks':3*n,'enumerated_errors_by_weight':counts,'total_enumerated_errors':sum(counts.values()),'distinct_syndromes':len(seen_syndromes),'collision_count':len(collisions),'collisions':collisions,'canonical_error_syndrome_stream_sha256':digest.hexdigest(),'stream_contract':'weight increasing 0..3; support itertools.combinations(range(45),r); assignments lexicographic X,Y,Z; each record x,z,syndrome encoded as six little-endian bytes each; identity first','tree_check_weight_histogram':dict(tree_check_weights),'all_edge_pair_check_weight_histogram':dict(edge_check_weights),'independent_distance_result':'No nonidentity Pauli of weight<=6 commutes with all 44 checks, since it splits into two disjoint errors of weight<=3 and would collide in syndrome. K_0 is a weight7 nontrivial logical. Thus pure [[45,1,7]] independently verified.','source_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'seconds':time.perf_counter()-start,'adjacency_rows_hex':[hex(row) for row in adjacency],'star_checks_hex':[[hex(x),hex(z)] for x,z in star],'spanning_tree_edges':tree}
    (BASE/'verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('adjacency_rows_hex','star_checks_hex','spanning_tree_edges')},indent=2))
if __name__=='__main__':main()
