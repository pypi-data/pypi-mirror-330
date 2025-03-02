from typing import Dict, Tuple, Union, Optional, Literal, List
from datetime import datetime
import pandas as pd

def convert_facts_to_dataframe(
    facts: Dict[Tuple[str, str], Dict[str, Dict[str, Union[str, int, float, bool, datetime]]]]
) -> pd.DataFrame:
    """
    Converts a dictionary of facts to a pandas DataFrame.
    Args:
        facts (Dict[Tuple[str, str], Dict[str, Dict[str, Union[str, int, float, bool, datetime]]]]): The facts to convert.
        direction (Optional[Literal['LR', 'RL', 'TB', 'BT']]): The direction of the facts.
    Returns:
        pd.DataFrame: A pandas DataFrame containing the facts.
    """
    column_names = ['subject', 'predicate', 'object', 'fact_id', 'fact_source', 'timestamp', 'depth']
    columns = {column_name: [] for column_name in column_names}

    for (_subject, _object), _edges in facts.items():
        for _edge, _facts in _edges.items():
            for _fact in _facts:
                columns['subject'].append(_subject)
                columns['predicate'].append(_edge)
                columns['object'].append(_object)
                columns['fact_id'].append(_fact['fact_id'])
                columns['fact_source'].append(_fact['fact_source'])
                columns['timestamp'].append(_fact['timestamp'])
                columns['depth'].append(_fact['depth'])

    return pd.DataFrame(columns)

def convert_facts_to_list_of_dictionaries(
    facts: Dict[Tuple[str, str], Dict[str, Dict[str, Union[str, int, float, bool, datetime]]]],
) -> List[Dict[str, Union[str, int, float, bool, datetime]]]:
    """
    Converts a dictionary of facts to a list of dictionaries.
    Args:
        facts (Dict[Tuple[str, str], Dict[str, Dict[str, Union[str, int, float, bool, datetime]]]]): The facts to convert.
        direction (Optional[Literal['LR', 'RL', 'TB', 'BT']]): The direction of the facts.
    Returns:
        List[Dict[str, Union[str, int, float, bool, datetime]]]: A list of dictionaries containing the facts.
    """
    df = convert_facts_to_dataframe(facts=facts)
    return df.to_dict(orient='records')
