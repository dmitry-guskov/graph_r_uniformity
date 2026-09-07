import importlib.util
from pathlib import Path
from itertools import combinations
import json
import networkx as nx
import numpy as np
import pytest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('graph_functions',ROOT/'modules/graph_functions.py')
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def graph_state(a):
    n=len(a)
    indices=np.arange(2**n)
    bits=((indices[:,None]>>np.arange(n-1,-1,-1))&1)
    parity=sum((bits[:,i]*bits[:,j] for i in range(n) for j in range(i+1,n) if a[i,j]), np.zeros(2**n, dtype=int))
    return (-1.)**parity/np.sqrt(2**n)

def test_gf2_differs_from_real_rank():
    a=np.array([[1,1,0],[1,0,1],[0,1,1]])
    assert np.linalg.matrix_rank(a)==3
    assert m.binary_rank(a)==2
    assert m.binary_rank(np.zeros((0,3)))==0

@pytest.mark.parametrize('n',[2,3,4,5])
def test_cut_certificate_against_partial_trace(n):
    for seed in range(4):
        a=nx.to_numpy_array(nx.gnp_random_graph(n,.53,seed=seed),dtype=int)
        state=graph_state(a).reshape([2]*n)
        for k in range(n//2+1):
            for cut in combinations(range(n),k):
                remaining=[i for i in range(n) if i not in cut]
                psi=state.transpose(list(cut)+remaining).reshape(2**k,-1)
                rho=psi@psi.conj().T
                exact=np.allclose(rho,np.eye(2**k)/2**k,atol=1e-13)
                assert m.is_maximally_mixed(a,cut)==exact
                assert np.linalg.matrix_rank(rho,tol=1e-10)==2**m.cut_rank(a,cut)

def test_peeling_false_negative_and_wheel():
    cross=np.array([[1,1,1],[1,0,1],[0,1,1]])
    a=np.block([[np.zeros((3,3)),cross],[cross.T,np.zeros((3,3))]])
    g=m.generate_graph(6,a)
    g.set_rules(m.spread,m.disconnect)
    m.genereate_given_state(g,[0,1,2])
    assert not g.simplify()
    assert m.is_maximally_mixed(a,[0,1,2])
    wheel=nx.to_numpy_array(nx.wheel_graph(6),dtype=int)
    assert m.is_k_uniform(wheel,3)
    assert not m.is_k_uniform(wheel,4)

def test_saved_examples_and_failure_witness():
    records=json.loads((ROOT/'data/recovered_graphs.json').read_text())['graphs']
    for record in records:
        a=np.array(record['adjacency'])
        assert m.is_k_uniform(a,record['exact_uniformity'])
        assert not m.is_k_uniform(a,record['exact_uniformity']+1)
    c=m.uniformity_certificate(np.zeros((4,4)),1)
    assert c=={'is_uniform':False,'k':1,'retained':[0],'rank':0}

def test_seeded_bernoulli_probability_and_validation():
    a=m.adjacency_matrix_binomial(500,.3,seed=19)
    assert abs(a.sum()/(500*499)-.3)<.01  # rejects historical p squared sampling
    np.testing.assert_array_equal(a,m.adjacency_matrix_binomial(500,.3,seed=19))
    assert np.array_equal(a,a.T) and not np.any(np.diag(a))
    with pytest.raises(ValueError):m.is_k_uniform([[0,1],[0,0]],1)
    with pytest.raises(ValueError):m.cut_rank([[0,1],[1,0]],[0,0])
    with pytest.raises(ValueError):m.uniformity_certificate([[0]],-1)
