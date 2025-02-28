

from typing import Any, List, Dict
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import pandas as pd

# define the search types for the page
text_search_types = ['synonym', 'suggest', 'fuzzy', 'exact']
fuzzy_search_types = ['fuzzy']
semantic_sparse_search_types = ['sparse']
semantic_dense_search_types = ['dense']
hybrid_search_types = ['hybrid']

all_search_types = text_search_types + semantic_sparse_search_types + semantic_dense_search_types + hybrid_search_types

def get_elastic_client(cloud_url, api_key):
    """
    Get the Elasticsearch client.

    Args:
        cloud_url (str): The cloud ID for the Elasticsearch cluster.
        api_key (str): The API key for authentication.

    Returns:
        Elasticsearch: The Elasticsearch client.
    """

    elastic_client = Elasticsearch(
        cloud_url,
        api_key=api_key,
    )

    return elastic_client



def replace_with_highlight(hit):
    """

        Replace the original text with the exerpts of highlighted text from Elasticsearch.

        Args:       
            hit (dict): The hit from Elasticsearch.  This is expected to be in the dictionary
            format returned by an elasticsearch client or from the elasticsearch_dsl.
            It will try to detect which is which.

        Returns:
            dict: The hit with the highlighted text.

    """    

    
    # A hit rom an elasticsearch client hit.
    if '_source' in hit and 'highlight' in hit:
        for key in hit['highlight']:
            if key in hit['_source']:
                hit['_source'][key] = ' '.join(hit['highlight'][key])
        return hit
    
    # A hit from an elasticsearch_dsl hit
    if hasattr(hit, 'meta') and 'highlight' in hit.meta:
        for key in hit.meta['highlight']:
            if key in hit.keys():
                hit[key] = ' '.join(hit.meta['highlight'][key])
        return hit

    # if we can't figure it out, we just won't do anything
    return hit

def flatten_hits(hits: List[dict], excluded_fields=['_id', '_index']) -> List[dict]:
    """
    Flatten the hits from an Elasticsearch query.

    Args:
        hits (list): A list of dictionaries containing the hits from an Elasticsearch query.

    Returns:
        pandas.DataFrame: A dataframe containing the values in hits.
    """

    tmp = pd.DataFrame(hits)

    # Flatten the meta information into the main dictionary for each hit
    flattened_hits = []
    for hit in hits:

        # Check if the hit is from an elasticsearch_dsl hit
        if hasattr(hit, 'meta'):
            flattened_hit = {**hit.meta.to_dict(),**hit}
            flattened_hits.append(flattened_hit)
        # Otherwise, assume it is from an elasticsearch client hit
        else:
            flattened_dict = {**hit, **hit['_source']}
            del flattened_dict['_source']
            flattened_hits.append(flattened_dict)
        
    # Convert the list of dictionaries into a DataFrame
    tmp = pd.DataFrame(flattened_hits)

    valid_fields = set(excluded_fields).intersection(set(tmp.columns))       
    df = tmp.drop(valid_fields, axis=1)

    return df

def build_dsl_text_search(searchterm,
                    index_name,
                    search_type,
                    included_fields,
                    client,
                    fuzziness="AUTO"):

    """
    Build a text search query with elasticsearch_dsl

    Args:
        searchterm: str - the search term to use
        index_name: str - the name of the index to search
        search_type: str - the type of search to perform
        included_fields: List[str] - the fields to include in the search
        fuzziness: str - the fuzziness to use
        client: Elasticsearch - the elasticsearch client to use
        include_field_metadata: bool - whether to include the field metadata
        
    Returns:
        Search: the elasticsearch_dsl search object
    """


    # common parameters for all text search types
    query_params = {
        "query": searchterm,
        "fields": included_fields
        }

    # Add fuzziness if the search type is 'fuzzy'
    if search_type in fuzzy_search_types:
        query_params["fuzziness"] = fuzziness

    query_type = "multi_match"

    s = (
        Search(using=client, index=index_name)
            .query(query_type, **query_params)
            .highlight(*included_fields)
    )

    return s

def build_semantic_search_query(field_name,
                                searchterm,
                                included_fields,):
    """
    Build a semantic search query for elasticsearch.  Unfortunately, as of 8.15 these are not supported by 
    elasticsearch_dsl, but may be soon.

    Args:
        field_name: str - the name of the field to search
        searchterm: str - the search term to use
        include_fields: List[str] - the fields to search

    Returns:
        dict: the search query that looks like:

        {'_source': {
                'includes': ['file_name',
                             'heading',
                             'text',
                             'text_sparse_embedding']},
                 'query': {
                    'semantic': {'
                        field': 'text_sparse_embedding', 
                        'query': 'yellow'}
                        }
            }
    """

    query_body= {
        '_source': {
            'includes': included_fields
            },
            'query': {
                'semantic': {
                    'field': field_name,
                    'query': searchterm
                }
            }
        }
    
    ic(query_body)
    return query_body


def build_text_query(searchterm, included_fields, boost):
    """
    Build a single multi_match query for the text fields
    
    Args:
        searchterm: str - the search term to use
        included_fields: List[str] - the fields to include in the search
        boost: float - the boost to apply to the search
    
    Returns:
        dict: the query that looks like:
        {
            "standard": {
                "query": {
                    "multi_match": {
                        "fields": included_fields,
                        "query": searchterm,
                        "boost": boost
                    }
                }
            }
        }
    """
    text_query = {}

    # build a single multi_match query for the text fields
    text_query = {
        "standard": {
            "query": {
                "multi_match": {
                    "fields": included_fields,
                    "query": searchterm,
                    "boost": boost
                }
            }
        }
    }

    return text_query

def build_semantic_query(searchterm, included_field, boost):
    """
    Build a single semantic query for the semantic fields

    Args:
        searchterm: str - the search term to use
        included_field: str - the field to include in the search
        boost: float - the boost to apply to the search
    
    Returns:
        dict: the query that looks like:
        {
            "semantic": {
                "field": included_field,
                "query": searchterm,
                "boost": boost
            }
        }
    """

    # build a single semantic query for the semantic fields
    semantic_query = {
        "standard": {
            "query": {
                "semantic": {
                    "field": included_field,
                    "query": searchterm,
                    "boost": boost
                }
            }
        }
    }

    return semantic_query

def build_hybrid_search_query(searchterm,
                              semantic_field_names,
                              text_included_fields,
                              semantic_boost=1.0,
                              text_boost=1.0):
    """
    Build a hybrid search query for elasticsearch.  Unfortunately, as of 8.15 these are not supported by
    elasticsearch_dsl, but may be soon.

    Args:
        searchterm: str - the search term to use
        semantic_field_names: List[str] - the name of the fields to search
        semantic_boost: float - the boost to apply to the semantic search
        text_field_name: str - the name of the field to search
        text_included_fields: List[str] - the fields to search
        text_boost: float - the boost to apply to the text

    Returns:
        A bool query that can look at both text fields and semantic fields.
    """

    # build multi_match query for text fields
    # build semantic queries for semantic field

    retrievers=[]

    
    text_query = build_text_query(searchterm, 
                                  text_included_fields, 
                                  text_boost)
    ic((text_query), type(text_query))
    retrievers.append(text_query)

    # build a separate semantic query for each semantic field
    for semantic_field_name in semantic_field_names:

        semantic_query = build_semantic_query(searchterm, 
                                              semantic_field_name, 
                                              semantic_boost)
        retrievers.append(semantic_query)

    query = {
        "retriever": {
            "rrf": {
                "retrievers": retrievers
            }
        }
    }

    return query

def execute_query (index_name: str, 
                  query_body: dict,
                  search_type: str = "exact",
                  include_metadata: bool = False,
                  highlight: bool = False,
                  highlight_fields: list = None,
                  client= None) -> List[Any]:
    """
    Query Elasticsearch by fields.

    Args:
        index_name (str): The name of the Elasticsearch index to search in.
        search_type (str): The type of search to perform. Options: "match" (default), "fuzzy".
        include_metadata (bool): Whether to include metadata in the search results. Default is False.
        query_body (dict): The query body to use in the Elasticsearch query.
        highlight (bool): Whether to highlight the search term in the results. Default is False.
        highlight_fields (list): A list of fields to highlight in the results. Default is None.
        client (Elasticsearch): The Elasticsearch client to use for the query.

    Returns:
        list: A list of Elasticsearch hits, each of which is a dictionary keyed by the field name.

    """

    if search_type in semantic_dense_search_types or \
        search_type in semantic_sparse_search_types or \
            search_type in hybrid_search_types:
        highlight = False

    # make an empty entry
    if 'highlight' not in query_body:
        query_body['highlight'] = {}

    # make the top level highlight entry
    if 'fields' not in query_body['highlight']:
        query_body['highlight']['fields'] = {}

    # add the fields to highlight
    if highlight:
        for field_name in highlight_fields:
            query_body["highlight"]["fields"][field_name] = {}
    
    response = client.search(index=index_name, body=query_body)
    hits = response['hits']['hits']

    # get a list of the fields that are being queried
    query_fields = query_body["query"]["multi_match"]['fields']
    
    # create an array of dictionaries with the fields that are being queried
    if search_type in text_search_types:
        filtered_hits = []
        # take all the hits
        for hit in hits:
            filtered_hit = {}

            if include_metadata:
                filtered_hit['_id'] = hit['_id']
                filtered_hit['_index'] = hit['_index']
                filtered_hit['_score'] = hit['_score']

            # filter out any fields that weren't specified in the query
            for field in query_fields:
                if field in hit['_source']:
                    # create the filtered hit, if necessary
                    if field not in filtered_hits:
                        filtered_hit[field] = {}
                try:
                    filtered_hit[field] = hit['_source'][field]
                except KeyError:
                    pass
            # add the filtered hit to the list
            filtered_hits.append(filtered_hit)
    
    return filtered_hits

def query_elastic_by_single_field(searchterm: str,                                   
                  index_name: str = None, 
                  field_name="",
                  search_type="match",
                  fuzziness: str = None,
                  highlight: bool = False,
                  model: str = None,
                  client=None) -> List[Any]:
    """
    Query Elasticsearch by field.

    Args:
        searchterm (str): The search term to query.
        index_name (str): The name of the Elasticsearch index to search in.
        field_name (str): The name of the field to search in.
        search_type (str): The type of search to perform. Options: "match" (default), "fuzzy".
        fuzziness (str): The fuzziness parameter for fuzzy search. Default is None.
        highlight (bool): Whether to highlight the search term in the results. Default is False.
        model (str): The name of the model to use for semantic search. Default is "none".
        excluded_fields (list): A list of fields to drop from the DataFrame. Default is ['_id', '_index', 'text_synonym'].
        client (Elasticsearch): The Elasticsearch client to use for the query.

    Returns:
        list: A list of Elasticsearch hits.
        query_body (dict): The query body used in the Elasticsearch query.
        st.session_state.df_hits: A dataframe with all the hits 
        st.session_state.hits: An HTML representation of the dataframe

    """

    if search_type in ["semantic", "text_expansion", "vector"]:
        search_type = "semantic"
        highlight = False

    query_body = {"query": {}}

    if search_type == "match":
        query_body["query"]["match"] = {
            field_name : {
                "query": searchterm
            }
        }
    elif search_type == "fuzzy":
        query_body["query"]["fuzzy"] = {
            field_name : {
                "value": searchterm,
                "fuzziness": fuzziness if fuzziness else "AUTO"
            }
        }

    elif search_type == "semantic":

        query_body["query"]["semantic"] = {
            "field": field_name,
            "query": searchterm
        }

    if 'highlight' not in query_body:
        query_body['highlight'] = {}

    if 'fields' not in query_body['highlight']:
        query_body['highlight']['fields'] = {}

    if highlight:
        query_body["highlight"]["fields"][field_name] = {}

    response = client.search(index=index_name, body=query_body)
    hits = response['hits']['hits']

    return hits, query_body

def query_elastic_by_multiple_fields(searchterm: str, 
                  index_name: str = None, 
                  field_names = None, 
                  search_type="match",
                  fuzziness: str = None,
                  client= None) -> List[Any]:
    """
    Query Elasticsearch by multiple fields.

    Args:
        searchterm (str): The search term to query.
        index_name (str): The name of the Elasticsearch index to search in.
        field_names (list): A list of field names to search in.
        search_type (str): The type of search to perform. Options: "match" (default), "fuzzy".
        fuzziness (str): The fuzziness parameter for fuzzy search. Default is None.
        client (Elasticsearch): The Elasticsearch client to use for the query.

    Returns:
        hits: A list of Elasticsearch hits.
        query_body (dict): The query body used in the Elasticsearch query.

    """

    if search_type in ["semantic", "text_expansion", "vector"]:
        search_type = "semantic"
        highlight = False

    query_body = {"query": {}}

    if search_type == "match":
        # Use multi_match query to search in multiple fields
        query_body["query"]["multi_match"] = {
            "query": searchterm,
            "fields": field_names
        }
    elif search_type == "fuzzy":
        # You need to write a loop for fuzzy search in multiple fields
        query_body["query"]["bool"] = {
            "should": [
                {
                    "fuzzy": {
                        field_name: {
                            "value": searchterm,
                            "fuzziness": fuzziness if fuzziness else "AUTO"
                        }
                    }
                }
                for field_name in field_names
            ]
        }

    if 'highlight' not in query_body:
        query_body['highlight'] = {}

    if 'fields' not in query_body['highlight']:
        query_body['highlight']['fields'] = {}


    response = client.search(index=index_name, body=query_body)
    hits = response['hits']['hits']

    return hits, query_body



import pandas as pd


def df_to_html(df, 
               remove_highlights=True,
               remove_fields=[]) -> str:
    """
    Convert a pandas DataFrame to an HTML table.

    Args:
        df (pandas.DataFrame): The DataFrame to convert.
        description (str): The description to display above the table. Default is "Search Details".
        remove_fields (list): A list of fields to remove from the DataFrame. Default is [].

    Returns:
        str: The HTML representation of the DataFrame as a table.
    """

    if remove_highlights:
        if 'highlight' in df.columns:
            df = df.drop('highlight', axis=1)

    df = df.drop(remove_fields, axis=1)

    html = df.to_html(index=False, escape=False)
    html = f'''
            <style>
                table {{
                    width: 100%;
                }}
                th {{
                    text-align: center;
                }}
                td, th {{
                    padding: 10px;
                    border-bottom: 1px solid #ddd;
                }}
                em {{
                    background-color: #ff0; /* bright yellow background */
                    color: #000; /* black text */
                    font-weight: bold; /* bold text */
                }}
            </style>
            {html}
        '''
    return html
