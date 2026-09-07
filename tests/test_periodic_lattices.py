import importlib.util
from pathlib import Path
import numpy as np
import pytest

ROOT=Path(__file__).resolve().parents[1]
def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

torus=load(ROOT/'research/periodic_lattices/torus.py','torus')
graphs=load(ROOT/'modules/graph_functions.py','graph_functions')


def test_complete_small_torus_distance_and_extra_minima():
    result=torus.enumerate_anchored([5,5],5)
    assert result['distance_certified'] and result['minimum_multiplicity_certified']
    assert [r['minimum_weight'] for r in result['rows']]==[5,6,7,8,5]
    assert sum(r['global_minimizers_of_fixed_cardinality'] for r in result['rows'] if r['minimum_weight']==5)==35
    with pytest.raises(ValueError): torus.enumerate_anchored([5,5,5],7)


@pytest.mark.parametrize('lengths',[[5],[5,6],[5,5,5]])
def test_canonical_support_gives_rank_deficient_cut(lengths):
    a=torus.adjacency_matrix(lengths)
    masks=torus.adjacency_masks(lengths)
    support=torus.stabilizer_support([0],masks)
    cut=[v for v in range(len(a)) if (support>>v)&1]
    assert len(cut)==2*len(lengths)+1
    complement=[v for v in range(len(a)) if v not in cut]
    cross=a[np.ix_(cut,complement)]
    # The generator at zero supplies an explicit nonzero row dependence.
    assert not cross[cut.index(0)].any()
    assert graphs.binary_rank(cross)<len(cut)


def test_period_four_sharpness_in_multiple_dimensions():
    for d in range(1,5):
        masks=torus.adjacency_masks([4]*d)
        selected=[v for v in range(len(masks)) if (masks[0]>>v)&1]
        assert torus.stabilizer_support(selected,masks).bit_count()==2*d


def test_finite_coverage_is_not_reported_as_complete():
    result=torus.enumerate_anchored([5,5,5],3)
    assert result['distance_upper_bound']==7
    assert not result['distance_certified'] and not result['minimum_multiplicity_certified']
