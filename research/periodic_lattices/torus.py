"""Finite exact probes accompanying periodic_cluster_distance.tex.

Vertices use mixed-radix indices: coordinate0 has stride1. These helpers do
not extrapolate finite enumeration into a general distance certificate.
"""
from itertools import combinations
from math import comb, prod
import numpy as np


def _lengths(side_lengths):
    values=tuple(side_lengths)
    if not values or any(not isinstance(v,(int,np.integer)) or v<3 for v in values):
        raise ValueError('Expected at least one integer cycle length >=3.')
    return tuple(map(int,values))


def adjacency_masks(side_lengths):
    """Return exact integer neighborhood masks for a product of simple cycles."""
    lengths=_lengths(side_lengths); n=prod(lengths)
    masks=[]
    for vertex in range(n):
        mask=0; stride=1
        for length in lengths:
            coordinate=(vertex//stride)%length
            for step in (-1,1):
                neighbor=vertex+(((coordinate+step)%length)-coordinate)*stride
                mask|=1<<neighbor
            stride*=length
        masks.append(mask)
    return masks


def adjacency_matrix(side_lengths):
    masks=adjacency_masks(side_lengths); n=len(masks)
    return np.array([[(mask>>v)&1 for v in range(n)] for mask in masks],dtype=np.uint8)


def stabilizer_support(selected, masks):
    """Support mask of product of canonical generators indexed by selected."""
    selected=tuple(selected)
    if len(set(selected))!=len(selected) or any(not 0<=v<len(masks) for v in selected):
        raise ValueError('Expected distinct valid generator indices.')
    x=z=0
    for vertex in selected:
        x|=1<<vertex; z^=masks[vertex]
    return x|z


def enumerate_anchored(side_lengths, max_size, *, max_subsets=1000000):
    """Exhaust exact minima by generator-subset cardinality, up to a work cap.

    Translation symmetry ensures every subset has an origin-containing
    representative. Distance is certified only if every potentially smaller
    weight is covered, since support weight is at least generator cardinality.
    """
    lengths=_lengths(side_lengths); n=prod(lengths)
    if not isinstance(max_size,(int,np.integer)) or not 1<=max_size<=n:
        raise ValueError('Expected 1 <= max_size <= number of vertices.')
    required=sum(comb(n-1,r-1) for r in range(1,max_size+1))
    if required>max_subsets:
        raise ValueError(f'{required} subsets exceed cap {max_subsets}; use the C++ probe explicitly.')
    masks=adjacency_masks(lengths); rows=[]
    for r in range(1,max_size+1):
        minimum=n+1; minimizers=0; witness=None; count=0
        for rest in combinations(range(1,n),r-1):
            selected=(0,)+rest; weight=stabilizer_support(selected,masks).bit_count(); count+=1
            if weight<minimum:
                minimum,minimizers,witness=weight,1,selected
            elif weight==minimum:
                minimizers+=1
        assert count==comb(n-1,r-1)
        rows.append({'generator_subset_size':r,'anchored_subsets':count,
                     'minimum_weight':minimum,'anchored_minimizers':minimizers,
                     'global_minimizers_of_fixed_cardinality':n*minimizers//r,
                     'witness_vertex_indices':list(witness)})
    smallest=min(row['minimum_weight'] for row in rows)
    return {'side_lengths':list(lengths),'vertices':n,'rows':rows,
            'distance_upper_bound':smallest,
            'distance_certified':max_size>=smallest-1,
            'minimum_multiplicity_certified':max_size>=smallest}
