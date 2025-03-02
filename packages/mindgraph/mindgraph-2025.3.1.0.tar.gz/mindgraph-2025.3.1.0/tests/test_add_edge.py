from atlantis.ai.memory.graph import GraphBackendInterface
from atlantis.ai.memory.graph import NetworkXGraphBackend
from atlantis.ai.memory.graph import SimpleGraphBackend
import pytest


@pytest.fixture
def simple_graph_backend():
    return SimpleGraphBackend()

@pytest.fixture
def networkx_graph_backend():
    return NetworkXGraphBackend()

@pytest.fixture
def simple(simple_graph_backend):
    return GraphBackendInterface(simple_graph_backend, case_sensitive=True)

@pytest.fixture
def simple_case_insensitive(simple_graph_backend):
    return GraphBackendInterface(simple_graph_backend, case_sensitive=False)

@pytest.fixture
def networkx(networkx_graph_backend):
    return GraphBackendInterface(networkx_graph_backend, case_sensitive=True)

@pytest.fixture
def networkx_case_insensitive(networkx_graph_backend):
    return GraphBackendInterface(networkx_graph_backend, case_sensitive=False)

def test_add_edge(simple, networkx):
    simple._add_edge(source_node="Paris", target_node="France", edge="capital_of", facts_dict={"fact_source": "Wikipedia"})
    networkx._add_edge(source_node="Paris", target_node="France", edge="capital_of", facts_dict={"fact_source": "Wikipedia"})

    edges = {
        ("Paris", "France"): {
            "capital_of": {
                "fact_source": "Wikipedia"
            }
        }
    }
    networkx_edges = networkx._get_edges(source_node="Paris", target_node="France")
    assert ('Paris', 'France') in networkx_edges
    assert 'capital_of' in networkx_edges[('Paris', 'France')]
    capital_of = networkx_edges[('Paris', 'France')]['capital_of']
    assert 'fact_source' in capital_of
    assert capital_of['fact_source'] == "Wikipedia"

    simple_edges = simple._get_edges(source_node="Paris", target_node="France")
    assert ('Paris', 'France') in simple_edges
    assert 'capital_of' in simple_edges[('Paris', 'France')]
    capital_of = simple_edges[('Paris', 'France')]['capital_of']
    assert 'fact_source' in capital_of
    assert capital_of['fact_source'] == "Wikipedia"

    assert networkx._get_edges(source_node="Paris", target_node="France") == edges
    assert simple._get_edges(source_node="Paris", target_node="France") == edges

def test_add_edge_case_insensitive(simple_case_insensitive, networkx_case_insensitive):
    simple_case_insensitive._add_edge(source_node="Paris", target_node="France", edge="capital_of", facts_dict={"fact_source": "Wikipedia"})
    networkx_case_insensitive._add_edge(source_node="Paris", target_node="France", edge="capital_of", facts_dict={"fact_source": "Wikipedia"})

    edges = {
        ("Paris", "France"): {
            "capital_of": {
                "fact_source": "Wikipedia"
            }
        }
    }
    networkx_edges = networkx_case_insensitive._get_edges(source_node="Paris", target_node="France")
    assert networkx_case_insensitive._fix_case('Paris') == 'paris'
    assert ('paris', 'france') in networkx_edges
    assert 'capital_of' in networkx_edges[('paris', 'france')]
    capital_of = networkx_edges[('paris', 'france')]['capital_of']
    assert 'fact_source' in capital_of
    assert capital_of['fact_source'] == "Wikipedia"

    simple_edges = simple_case_insensitive._get_edges(source_node="Paris", target_node="France")
    assert ('paris', 'france') in simple_edges
    assert 'capital_of' in simple_edges[('paris', 'france')]
    capital_of = simple_edges[('paris', 'france')]['capital_of']
    assert 'fact_source' in capital_of
    assert capital_of['fact_source'] == "Wikipedia"


def test_get_edges(simple, networkx):
    simple._add_edge(source_node="Paris", target_node="France", edge="capital_of", facts_dict={"fact_source": "Wikipedia"})
    networkx._add_edge(source_node="Paris", target_node="France", edge="capital_of", facts_dict={"fact_source": "Wikipedia"})
    simple._add_edge(source_node="Paris", target_node="France", edge="city_in", facts_dict={"fact_source": "Wikipedia"})
    networkx._add_edge(source_node="Paris", target_node="France", edge="city_in", facts_dict={"fact_source": "Wikipedia"})
    simple._add_edge(source_node="Paris", target_node="Europe", edge="city_in", facts_dict={"fact_source": "Wikipedia"})
    networkx._add_edge(source_node="Paris", target_node="Europe", edge="city_in", facts_dict={"fact_source": "Wikipedia"})

    paris_france_edges = {
        ('Paris', 'France'): {
            'capital_of': {
                'fact_source': 'Wikipedia'
            },
            'city_in': {
                'fact_source': 'Wikipedia'
            }
        }
    }
    print(networkx._get_edges(source_node="Paris", target_node="France"))
    assert networkx._get_edges(source_node="Paris", target_node="France") == paris_france_edges
    assert simple._get_edges(source_node="Paris", target_node="France") == paris_france_edges

    paris_capital_of_france_edges = {
        ('Paris', 'France'): {
            'capital_of': {
                'fact_source': 'Wikipedia'
            }
        }
    }

    assert networkx._get_edges(source_node="Paris", target_node="France", edge="capital_of") == paris_capital_of_france_edges
    assert simple._get_edges(source_node="Paris", target_node="France", edge="capital_of") == paris_capital_of_france_edges

    paris_city_in_france_edges = {
        ('Paris', 'France'): {
            'city_in': {
                'fact_source': 'Wikipedia'
            }
        }
    }

    assert networkx._get_edges(source_node="Paris", target_node="France", edge="city_in") == paris_city_in_france_edges
    assert simple._get_edges(source_node="Paris", target_node="France", edge="city_in") == paris_city_in_france_edges

    paris_city_in_europe_edges = {
        ('Paris', 'Europe'): {
            'city_in': {
                'fact_source': 'Wikipedia'
            }
        }
    }   

    assert networkx._get_edges(source_node="Paris", target_node="Europe", edge="city_in") == paris_city_in_europe_edges
    assert simple._get_edges(source_node="Paris", target_node="Europe", edge="city_in") == paris_city_in_europe_edges

    paris_city_in_edges = {
        ('Paris', 'Europe'): {
            'city_in': {
                'fact_source': 'Wikipedia'
            }
        },
        ('Paris', 'France'): {
            'city_in': {
                'fact_source': 'Wikipedia'
            }
        }
    }

    assert networkx._get_edges(source_node="Paris", edge="city_in") == paris_city_in_edges
    assert simple._get_edges(source_node="Paris", edge="city_in") == paris_city_in_edges

    france_edges = {
        ('Paris', 'France'): {
            'city_in': {
                'fact_source': 'Wikipedia'
            },
            'capital_of': { 
                'fact_source': 'Wikipedia'
            }
        }
    }

    assert networkx._get_edges(target_node="France") == france_edges
    assert simple._get_edges(target_node="France") == france_edges
    
    city_in_france_edges = {
        ('Paris', 'France'): {
            'city_in': {
                'fact_source': 'Wikipedia'
            }
        }
    }

    assert networkx._get_edges(target_node="France", edge="city_in") == city_in_france_edges
    assert simple._get_edges(target_node="France", edge="city_in") == city_in_france_edges


    capital_of_edges = {
        ('Paris', 'France'): {
            'capital_of': {
                'fact_source': 'Wikipedia'
            }
        }
    }

    assert networkx._get_edges(edge="capital_of") == capital_of_edges
    assert simple._get_edges(edge="capital_of") == capital_of_edges

    capital_of_france_edges = {
        ('Paris', 'France'): {
            'capital_of': {
                'fact_source': 'Wikipedia'
            }
        }
    }

    assert networkx._get_edges(edge="capital_of", target_node="France") == capital_of_france_edges
    assert simple._get_edges(edge="capital_of", target_node="France") == capital_of_france_edges
