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
        ('fact_5', 'Eiffel_Tower', 'located_in', 'Paris', 'Wikipedia'),
        ('fact_6', 'Eiffel_Tower', 'is_a', 'tower', 'Britannica'),
        ('fact_7', 'French', 'language_spoken_in', 'France', 'Wikipedia')
    ]

@pytest.fixture
def facts_about_germany():
    return [
        ('fact_8', 'Berlin', 'city_in', 'Germany', 'Wikipedia'),
        ('fact_9', 'Berlin', 'capital_of', 'Germany', 'Britannica'),
        ('fact_10', 'Berlin', 'capital_of', 'Germany', 'Wikipedia'),
        ('fact_11', 'Germany', 'country_in', 'Europe', 'Britannica'),
        ('fact_12', 'Germany', 'at_war_with', 'France', 'Britannica')
    ]

@pytest.fixture
def facts_about_europe():
    return [
        ('fact_13', 'Europe', 'continent_of', 'World', 'Britannica'),
        ('fact_14', 'Denmark', 'country_in', 'Europe', 'Britannica'),
        ('fact_15', 'Sweden', 'country_in', 'Europe', 'Britannica'),
        ('fact_16', 'Switzerland', 'country_in', 'Europe', 'Britannica'),
        ('fact_17', 'Germany', 'country_in', 'Europe', 'Britannica'),
        ('fact_18', 'France', 'country_in', 'Europe', 'Britannica'),
        ('fact_19', 'Italy', 'country_in', 'Europe', 'Britannica'),
        ('fact_20', 'Spain', 'country_in', 'Europe', 'Britannica'),
    ]

@pytest.fixture
def simple_graph_backend(facts_about_france, facts_about_germany, facts_about_europe):
    graph = SimpleGraphBackend()
    return graph

@pytest.fixture
def networkx_graph_backend(facts_about_france, facts_about_germany, facts_about_europe):
    graph = NetworkXGraphBackend()
    return graph

@pytest.fixture
def simple(simple_graph_backend, facts_about_france, facts_about_germany, facts_about_europe):
    gbi = GraphBackendInterface(simple_graph_backend, case_sensitive=True)
    for fact in facts_about_france:
        gbi.add_fact(fact_id=fact[0], subject=fact[1], predicate=fact[2], object=fact[3], fact_source=fact[4])
    for fact in facts_about_germany:
        gbi.add_fact(fact_id=fact[0], subject=fact[1], predicate=fact[2], object=fact[3], fact_source=fact[4])
    for fact in facts_about_europe:
        gbi.add_fact(fact_id=fact[0], subject=fact[1], predicate=fact[2], object=fact[3], fact_source=fact[4])      
    return gbi

@pytest.fixture
def networkx(networkx_graph_backend, facts_about_france, facts_about_germany, facts_about_europe):
    gbi = GraphBackendInterface(networkx_graph_backend, case_sensitive=True)
    for fact in facts_about_france:
        gbi.add_fact(fact_id=fact[0], subject=fact[1], predicate=fact[2], object=fact[3], fact_source=fact[4])
    for fact in facts_about_germany:
        gbi.add_fact(fact_id=fact[0], subject=fact[1], predicate=fact[2], object=fact[3], fact_source=fact[4])
    for fact in facts_about_europe:
        gbi.add_fact(fact_id=fact[0], subject=fact[1], predicate=fact[2], object=fact[3], fact_source=fact[4])
    return gbi

@pytest.fixture
def simple_case_insensitive(simple_graph_backend, facts_about_france, facts_about_germany, facts_about_europe):
    gbi = GraphBackendInterface(simple_graph_backend, case_sensitive=False)
    for fact in facts_about_france:
        gbi.add_fact(fact_id=fact[0], subject=fact[1], predicate=fact[2], object=fact[3], fact_source=fact[4])
    for fact in facts_about_germany:
        gbi.add_fact(fact_id=fact[0], subject=fact[1], predicate=fact[2], object=fact[3], fact_source=fact[4])
    for fact in facts_about_europe:
        gbi.add_fact(fact_id=fact[0], subject=fact[1], predicate=fact[2], object=fact[3], fact_source=fact[4])
    return gbi

@pytest.fixture
def networkx_case_insensitive(networkx_graph_backend, facts_about_france, facts_about_germany, facts_about_europe):
    gbi = GraphBackendInterface(networkx_graph_backend, case_sensitive=False)
    for fact in facts_about_france:
        gbi.add_fact(fact_id=fact[0], subject=fact[1], predicate=fact[2], object=fact[3], fact_source=fact[4])
    for fact in facts_about_germany:
        gbi.add_fact(fact_id=fact[0], subject=fact[1], predicate=fact[2], object=fact[3], fact_source=fact[4])
    for fact in facts_about_europe:
        gbi.add_fact(fact_id=fact[0], subject=fact[1], predicate=fact[2], object=fact[3], fact_source=fact[4])
    return gbi

def test_get_neighbours(simple, networkx):
    output_type = 'list'
    metadata_type = 'dict'

    simple_facts = simple.get_facts_about(entities='Paris', direction='outgoing', fields=['fact_id', 'fact_source', 'timestamp', 'depth'], depth=1, output_type=output_type, metadata_type=metadata_type)
    networkx_facts = networkx.get_facts_about(entities='Paris', direction='outgoing', fields=['fact_id', 'fact_source', 'timestamp', 'depth'], depth=1, output_type=output_type, metadata_type=metadata_type)
    assert_iterables_are_equal(simple_facts, networkx_facts)
    
    simple_neighbours = simple.get_facts_about(entities='Paris', direction='outgoing', depth=0, output_type=output_type, metadata_type=metadata_type)
    assert len(simple_neighbours) == 0

    simple_neighbours = simple.get_facts_about(entities='Paris' , direction='outgoing', depth=0, output_type=output_type, metadata_type=metadata_type)
    assert len(simple_neighbours) == 0

    simple_neighbours = simple.get_facts_about(entities='Paris', direction='outgoing', depth=0, output_type=output_type, metadata_type=metadata_type)
    assert len(simple_neighbours) == 0

    # with depth 1 we should get 2 facts per subjects
    simple_neighbours = simple.get_facts_about(entities='Paris', direction='outgoing', depth=1, output_type=output_type, metadata_type=metadata_type)
    assert simple.count(simple_neighbours, key='pairs') == 1
    assert simple.count(simple_neighbours, key='edges') == 2
    assert simple.count(simple_neighbours, key='facts') == 3

    incoming_neighbours = simple.get_facts_about(entities='Paris', direction='incoming', depth=1, output_type=output_type, metadata_type=metadata_type)
    assert simple.count(incoming_neighbours, key='pairs') == 1 # Eiffel Tower - Paris
    assert simple.count(incoming_neighbours, key='edges') == 1 
    assert simple.count(incoming_neighbours, key='facts') == 1

    # with depth 1 we should get one fact per nodes
    simple_neighbours = simple.get_facts_about(entities='Paris', direction='outgoing', depth=1, output_type=output_type, metadata_type=metadata_type)
    assert len(simple_neighbours) == 3
    print(simple_neighbours)
    # case sensitive
    assert all(dictionary['source_node'] == 'Paris' and dictionary['target_node'] == 'France' for dictionary in simple_neighbours)


    outgoing_neighbours_depth_2 = simple.get_facts_about(entities='Paris', direction='outgoing', depth=2, output_type=output_type, metadata_type=metadata_type)
    assert simple.count(outgoing_neighbours_depth_2, key='pairs') == 2 # Paris-France, France-Europe
    assert any(dictionary['source_node'] == 'Paris' and dictionary['target_node'] == 'France' for dictionary in outgoing_neighbours_depth_2)
    assert any(dictionary['source_node'] == 'France' and dictionary['target_node'] == 'Europe' for dictionary in outgoing_neighbours_depth_2)
    assert simple.count(outgoing_neighbours_depth_2, key='edges') == 3 # Paris-city_in-France, Paris-capital_of-France, France-in-Europe
    
def test_get_neighbours_case_insensitive(simple_case_insensitive, networkx_case_insensitive):
    simple = simple_case_insensitive
    networkx = networkx_case_insensitive
    output_type = 'list'
    metadata_type = 'tuple'

    simple_facts = simple.get_facts_about(entities='Paris', direction='outgoing', fields=['fact_id', 'fact_source', 'timestamp', 'depth'], depth=1, output_type=output_type, metadata_type=metadata_type)
    networkx_facts = networkx.get_facts_about(entities='Paris', direction='outgoing', fields=['fact_id', 'fact_source', 'timestamp', 'depth'], depth=1, output_type=output_type, metadata_type=metadata_type)
    assert_iterables_are_equal(simple_facts, networkx_facts)
    
    simple_neighbours = simple.get_facts_about(entities='Paris', direction='outgoing', depth=0, output_type=output_type, metadata_type=metadata_type)
    assert len(simple_neighbours) == 0

    simple_neighbours = simple.get_facts_about(entities='Paris', direction='outgoing', depth=0, output_type=output_type, metadata_type=metadata_type)
    assert len(simple_neighbours) == 0

    simple_neighbours = simple.get_facts_about(entities='Paris', direction='outgoing', depth=0, output_type=output_type, metadata_type=metadata_type)
    assert len(simple_neighbours) == 0

    # with depth 1 we should get 2 facts per subjects
    simple_neighbours = simple.get_facts_about(entities='Paris', direction='outgoing', depth=1, output_type=output_type, metadata_type=metadata_type)
    assert isinstance(simple_neighbours, list)
    assert all(isinstance(fact, tuple) for fact in simple_neighbours)

    incoming_neighbours = simple.get_facts_about(entities='Paris', direction='incoming', depth=1, output_type=output_type, metadata_type=metadata_type)
    assert isinstance(incoming_neighbours, list)
    assert all(isinstance(fact, tuple) for fact in incoming_neighbours)

    # with depth 1 we should get one fact per nodes
    simple_neighbours = simple.get_facts_about(entities='Paris', direction='outgoing', depth=1, output_type=output_type, metadata_type=metadata_type)
    assert isinstance(simple_neighbours, list)
    #assert len(simple_neighbours) == 13
    first_fact = simple_neighbours[0]
    assert first_fact[0] == 'paris'
    assert first_fact[2] == 'france'
    assert first_fact[1] == 'city_in'
    assert first_fact[3] == 'fact_1'
    assert first_fact[4] == 'Wikipedia'


    outgoing_neighbours_depth_2 = simple.get_facts_about(entities='Paris', direction='outgoing', depth=2, output_type=output_type, metadata_type=metadata_type)
    # assert simple.count(outgoing_neighbours_depth_2, key='pairs') == 2 # Paris-France, France-Europe
    assert isinstance(outgoing_neighbours_depth_2, list)
    
    paris_france_count = 0
    france_europe_count = 0
    for fact in outgoing_neighbours_depth_2:
        paris_france_count += fact[0] == 'paris' and fact[2] == 'france'
        france_europe_count += fact[0] == 'france' and fact[2] == 'europe'
    assert paris_france_count >= 1
    assert france_europe_count >= 1
    assert simple.count(outgoing_neighbours_depth_2, key='edges') == 3 # Paris-city_in-France, Paris-capital_of-France, France-in-Europe


