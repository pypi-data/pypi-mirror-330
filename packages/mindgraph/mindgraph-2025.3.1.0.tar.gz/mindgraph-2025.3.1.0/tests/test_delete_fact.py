from atlantis.ai.memory.graph import GraphBackendInterface
from atlantis.ai.memory.graph import NetworkXGraphBackend
from atlantis.ai.memory.graph import SimpleGraphBackend
from atlantis.utils import assert_iterables_are_equal
import pytest
import pprint

@pytest.fixture
def simple_graph_backend():
    return SimpleGraphBackend()

@pytest.fixture
def networkx_graph_backend():
    return NetworkXGraphBackend()

@pytest.fixture
def simple(simple_graph_backend):
    simple_graph_backend_interface = GraphBackendInterface(simple_graph_backend, case_sensitive=True)
    simple_graph_backend_interface._add_edge(source_node="Paris", target_node="France", edge="capital_of", facts_dict={"fact_source": "Wikipedia"})
    simple_graph_backend_interface._add_edge(source_node="Paris", target_node="France", edge="city_in", facts_dict={"fact_source": "Wikipedia"})
    simple_graph_backend_interface._add_edge(source_node="Paris", target_node="Europe", edge="city_in", facts_dict={"fact_source": "Wikipedia"})
    return simple_graph_backend_interface

@pytest.fixture
def networkx(networkx_graph_backend):
    networkx_graph_backend_interface = GraphBackendInterface(networkx_graph_backend, case_sensitive=True)
    networkx_graph_backend_interface._add_edge(source_node="Paris", target_node="France", edge="capital_of", facts_dict={"fact_source": "Wikipedia"})
    networkx_graph_backend_interface._add_edge(source_node="Paris", target_node="France", edge="city_in", facts_dict={"fact_source": "Wikipedia"})
    networkx_graph_backend_interface._add_edge(source_node="Paris", target_node="Europe", edge="city_in", facts_dict={"fact_source": "Wikipedia"})
    return networkx_graph_backend_interface

@pytest.fixture
def simple_case_insensitive(simple_graph_backend):
    simple_graph_backend_interface = GraphBackendInterface(simple_graph_backend, case_sensitive=False)
    simple_graph_backend_interface._add_edge(source_node="Paris", target_node="France", edge="capital_of", facts_dict={"fact_source": "Wikipedia"})
    simple_graph_backend_interface._add_edge(source_node="Paris", target_node="France", edge="city_in", facts_dict={"fact_source": "Wikipedia"})
    simple_graph_backend_interface._add_edge(source_node="Paris", target_node="Europe", edge="city_in", facts_dict={"fact_source": "Wikipedia"})
    return simple_graph_backend_interface

@pytest.fixture
def networkx_case_insensitive(networkx_graph_backend):
    networkx_graph_backend_interface = GraphBackendInterface(networkx_graph_backend, case_sensitive=False)
    networkx_graph_backend_interface._add_edge(source_node="Paris", target_node="France", edge="capital_of", facts_dict={"fact_source": "Wikipedia"})
    networkx_graph_backend_interface._add_edge(source_node="Paris", target_node="France", edge="city_in", facts_dict={"fact_source": "Wikipedia"})
    networkx_graph_backend_interface._add_edge(source_node="Paris", target_node="Europe", edge="city_in", facts_dict={"fact_source": "Wikipedia"})
    return networkx_graph_backend_interface


@pytest.fixture
def edges():
    return {
        ("Paris", "France"): {'capital_of': {'fact_source': 'Wikipedia'}, 'city_in': {'fact_source': 'Wikipedia'}},
        ("Paris", "Europe"): {'city_in': {'fact_source': 'Wikipedia'}}
    }

@pytest.fixture
def edges_case_insensitive():
    return {
        ("paris", "france"): {'capital_of': {'fact_source': 'Wikipedia'}, 'city_in': {'fact_source': 'Wikipedia'}},
        ("paris", "europe"): {'city_in': {'fact_source': 'Wikipedia'}}
    }

def test_delete_fact(simple, networkx, edges):
    assert simple._get_edges() == edges
    assert networkx._get_edges() == edges

    simple.remove_facts(subject="Paris", predicate="city_in", object="France")
    networkx.remove_facts(subject="Paris", predicate="city_in", object="France")
    del edges[("Paris", "France")]['city_in']
    if edges[("Paris", "France")] == {}:
        del edges[("Paris", "France")]

    assert simple._get_edges() == edges
    assert networkx._get_edges() == edges

    simple.remove_facts(subject="Paris", predicate="city_in", object="Europe")
    networkx.remove_facts(subject="Paris", predicate="city_in", object="Europe")
    del edges[("Paris", "Europe")]['city_in']
    if edges[("Paris", "Europe")] == {}:
        del edges[("Paris", "Europe")]

    assert simple._get_edges() == edges
    assert networkx._get_edges() == edges

def test_delete_fact_case_insensitive(simple_case_insensitive, networkx_case_insensitive, edges_case_insensitive):

    assert_iterables_are_equal(simple_case_insensitive._get_edges(), edges_case_insensitive)
    assert_iterables_are_equal(networkx_case_insensitive._get_edges(), edges_case_insensitive)

    simple_case_insensitive.remove_facts(subject="Paris", predicate="city_in", object="France")
    networkx_case_insensitive.remove_facts(subject="Paris", predicate="city_in", object="France")
    del edges_case_insensitive[("paris", "france")]['city_in']
    if edges_case_insensitive[("paris", "france")] == {}:
        del edges_case_insensitive[("paris", "france")]

    assert_iterables_are_equal(simple_case_insensitive._get_edges(), edges_case_insensitive)
    assert_iterables_are_equal(networkx_case_insensitive._get_edges(), edges_case_insensitive)

    simple_case_insensitive.remove_facts(subject="Paris", predicate="city_in", object="Europe")
    networkx_case_insensitive.remove_facts(subject="Paris", predicate="city_in", object="Europe")
    del edges_case_insensitive[("paris", "europe")]['city_in']
    if edges_case_insensitive[("paris", "europe")] == {}:
        del edges_case_insensitive[("paris", "europe")]

    assert_iterables_are_equal(simple_case_insensitive._get_edges(), edges_case_insensitive)
    assert_iterables_are_equal(networkx_case_insensitive._get_edges(), edges_case_insensitive)

def test_delete_facts_by_predicate(simple, networkx, edges):
    pprint.pprint(simple._get_edges())
    pprint.pprint(networkx._get_edges())
    pprint.pprint(edges)

    simple.remove_facts(predicate="city_in")
    networkx.remove_facts(predicate="city_in")
    del edges[("Paris", "France")]['city_in']
    del edges[("Paris", "Europe")]['city_in']
    if edges[("Paris", "France")] == {}:
        del edges[("Paris", "France")]
    if edges[("Paris", "Europe")] == {}:
        del edges[("Paris", "Europe")]
    print('\n\nsimple')
    pprint.pprint(simple._get_edges())
    print('\n\nnetworkx')
    pprint.pprint(networkx._get_edges())
    print('\n\nedges')
    pprint.pprint(edges)
    assert simple._get_edges() == edges 
    assert networkx._get_edges() == edges

def test_delete_facts_by_subject(simple, networkx, edges):
    simple.remove_facts(subject="Paris")
    networkx.remove_facts(subject="Paris")
    del edges[("Paris", "France")]
    del edges[("Paris", "Europe")]
    assert simple._get_edges() == edges
    assert networkx._get_edges() == edges

def test_delete_facts_by_object(simple, networkx, edges):
    simple.remove_facts(object="France")
    networkx.remove_facts(object="France")
    del edges[("Paris", "France")]
    assert simple._get_edges() == edges
    assert networkx._get_edges() == edges

