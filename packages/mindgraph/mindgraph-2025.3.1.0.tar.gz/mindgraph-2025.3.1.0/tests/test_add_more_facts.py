from atlantis.ai.memory.graph import GraphBackendInterface
from atlantis.ai.memory.graph import NetworkXGraphBackend
from atlantis.ai.memory.graph import SimpleGraphBackend
import pytest
from datetime import datetime
import pprint
from atlantis.utils import assert_iterables_are_equal

@pytest.fixture
def facts_about_france():
    return [
        ('fact_1', 'Paris', 'city_in', 'France', 'Wikipedia'),
        ('fact_2', 'Paris', 'capital_of', 'France', 'Britannica'),
        ('fact_3', 'Paris', 'capital_of', 'France', 'Wikipedia'),
        ('fact_4', 'France', 'country_in', 'Europe', 'Britannica'),
        ('fact_6', 'Europe', 'continent_of', 'World', 'Britannica'),
        ('fact_7', 'Eiffel_Tower', 'located_in', 'Paris', 'Wikipedia'),
        ('fact_8', 'Eiffel_Tower', 'is_a', 'tower', 'Britannica'),
        ('fact_9', 'French', 'language_spoken_in', 'France', 'Wikipedia')
    ]

@pytest.fixture
def facts_about_germany():
    return [
        ('fact_10', 'Berlin', 'city_in', 'Germany', 'Wikipedia'),
        ('fact_11', 'Berlin', 'capital_of', 'Germany', 'Britannica'),
        ('fact_12', 'Berlin', 'capital_of', 'Germany', 'Wikipedia'),
        ('fact_13', 'Germany', 'country_in', 'Europe', 'Britannica'),
        ('fact_14', 'Germany', 'at_war_with', 'France', 'Britannica')
    ]

@pytest.fixture
def simple_graph_backend():
    return SimpleGraphBackend()

@pytest.fixture
def networkx_graph_backend():
    return NetworkXGraphBackend()

@pytest.fixture
def simple(simple_graph_backend):
    return GraphBackendInterface(simple_graph_backend)

@pytest.fixture
def networkx(networkx_graph_backend):
    return GraphBackendInterface(networkx_graph_backend)

def test_add_facts_about_france(simple, networkx, facts_about_france):

    connected_pairs = set()
    edges = set()
    fact_sources = set()

    for i, fact_tuple in enumerate(facts_about_france):
        connected_pairs.add((fact_tuple[1], fact_tuple[3]))
        edges.add((fact_tuple[1], fact_tuple[3], fact_tuple[2]))
        fact_sources.add((fact_tuple[0], fact_tuple[1], fact_tuple[2], fact_tuple[3]))
        print(f"Adding fact {i+1} of {len(facts_about_france)}: {fact_tuple}")
        simple.add_fact(fact_id=fact_tuple[0], subject=fact_tuple[1], predicate=fact_tuple[2], object=fact_tuple[3], fact_source=fact_tuple[4])
        networkx.add_fact(fact_id=fact_tuple[0], subject=fact_tuple[1], predicate=fact_tuple[2], object=fact_tuple[3], fact_source=fact_tuple[4])
        assert simple.get_number_of_connected_pairs() == len(connected_pairs)
        assert simple.get_number_of_edges() == len(edges)
        assert simple.get_number_of_fact_sources() == len(fact_sources)

        assert networkx.get_number_of_connected_pairs() == len(connected_pairs)
        assert networkx.get_number_of_edges() == len(edges)
        assert networkx.get_number_of_fact_sources() == len(fact_sources) 

