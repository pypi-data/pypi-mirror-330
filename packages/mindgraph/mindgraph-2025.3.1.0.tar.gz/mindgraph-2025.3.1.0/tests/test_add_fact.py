from atlantis.ai.memory.graph import GraphBackendInterface
from atlantis.ai.memory.graph import NetworkXGraphBackend
from atlantis.ai.memory.graph import SimpleGraphBackend
import pytest
from datetime import datetime
import pprint
from atlantis.utils import assert_iterables_are_equal
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
def networkx(networkx_graph_backend):
    return GraphBackendInterface(networkx_graph_backend, case_sensitive=True)

def test_add_fact(simple, networkx):
    # if no fact_id is provided, it should raise an error
    with pytest.raises((ValueError, TypeError)):
        simple.add_fact(subject="Paris", predicate="city_in", object="France", fact_id="fact_1")
    with pytest.raises((ValueError, TypeError)):
        networkx.add_fact(subject="Paris", predicate="city_in", object="France", fact_id="fact_1")

    # if no fact source is provided, it should raise an error
    with pytest.raises((ValueError, TypeError)):
        simple.add_fact(fact_id="fact_1", subject="Paris", predicate="city_in", object="France")
    with pytest.raises((ValueError, TypeError)):
        networkx.add_fact(fact_id="fact_1", subject="Paris", predicate="city_in", object="France")

    # if a fact_id is provided, it should not raise an error
    timestamp = datetime.now()
    simple.add_fact(fact_id="fact_1", subject="Paris", predicate="city_in", object="France", fact_source="Wikipedia", timestamp=timestamp)
    simple_facts = simple.get_facts_about(entities="Paris", metadata_type='tuple', direction='outgoing', depth=1)
    assert len(simple_facts) == 1

    networkx.add_fact(fact_id="fact_1", subject="Paris", predicate="city_in", object="France", fact_source="Wikipedia", timestamp=timestamp)

    # facts should be:
    fields =('source_node', 'edge', 'target_node', 'fact_source', 'depth')
    facts = {
        ('Paris', 'France'): {'city_in': {'fact_1': ('Paris', 'city_in', 'France', 'Wikipedia', 1)}}
    }
    # single node can be provided
    simple_facts = simple.get_facts_about(entities="Paris", metadata_type='tuple', fields=fields, depth=1, direction='outgoing')
    assert len(simple_facts[0]) == len(fields)
    networkx_facts = networkx.get_facts_about(entities="Paris", metadata_type='tuple', fields=fields, direction='outgoing', depth=1)
    assert len(networkx_facts) == 1
    networkx_facts = networkx.get_facts_about(entities="Paris", metadata_type='tuple', fields=fields, direction='both', depth=1)
    assert len(networkx_facts) == 1
    assert len(networkx_facts[0]) == len(fields)
    assert len(simple_facts) == 1
    
    facts =  [('Paris', 'city_in', 'France', 'Wikipedia', 1)]
    assert_iterables_are_equal(simple_facts, facts, 'simple_facts', 'facts')
    assert_iterables_are_equal(networkx_facts, facts, 'networkx_facts', 'facts')

    # multiple nodes can be provided
    simple_facts = simple.get_facts_about(entities=["Paris"], fields=fields, metadata_type='tuple')
    networkx_facts = networkx.get_facts_about(entities=["Paris"], fields=fields, metadata_type='tuple')

    pprint.pprint(simple_facts)
    pprint.pprint(facts)

    assert len(simple_facts[0]) == len(fields)
    assert len(networkx_facts[0]) == len(fields)
    assert len(facts[0]) == len(fields)

    for simple_fact, fact in zip(simple_facts, facts):
        assert simple_fact == fact

    assert_iterables_are_equal(simple_facts, facts, 'simple_facts', 'facts')
    assert_iterables_are_equal(networkx_facts, facts, 'networkx_facts', 'facts')

    # multiple nodes can be provided
    simple_facts = simple.get_facts_about(entities=["Paris", "France"], fields=fields, metadata_type='tuple')
    networkx_facts = networkx.get_facts_about(entities=["Paris", "France"], fields=fields, metadata_type='tuple')

    for simple_fact, fact in zip(simple_facts, facts):
        assert simple_fact == fact

    print(simple_facts)
    assert len(set(simple_facts)) == len(facts)

    assert set(simple_facts) == set(facts)
    assert set(networkx_facts) == set(facts)

    # multiple nodes can be provided
    simple_facts = simple.get_facts_about(entities="Paris", predicates="city_in", fields=fields, metadata_type='tuple')
    networkx_facts = networkx.get_facts_about(entities="Paris", predicates="city_in", fields=fields, metadata_type='tuple')
    assert simple_facts == facts
    assert networkx_facts == facts


