# from polly import polly_kg
from polly.polly_kg import PollyKG
import pytest

# import os
from polly.errors import InvalidParameterException, RequestException

# import polly
import test_constants as test_const

key = "POLLY_API_KEY"
token = "Zjc2ZGM2YmVjNzo6ZmY2OTk0ZGVhZWQ3YWE3ZGU2OTExMTZlYTE0ZDgxMGVkZGEzYmNlZA=="
response_json = test_const.WORKSPACE_RESPONSE_JSON


def test_obj_initialised():
    assert PollyKG(token, env="testpolly") is not None


def test_get_engine_status():
    obj = PollyKG(token, env="testpolly")
    assert dict(obj.get_engine_status()) is not None


def test_get_graph_summary():
    obj = PollyKG(token, env="testpolly")
    response = obj.get_graph_summary()

    assert response is not None
    assert isinstance(response, dict)
    assert response["numNodes"] is not None
    assert response["numEdges"] is not None


def test_run_gremlin_query_success(mocker):
    # Mocked response from API
    mocked_response = {
        "requestId": "ab81155d-9f64-4717-a1e3-4e70bf5e6dff",
        "status": {
            "message": "",
            "code": 200,
            "attributes": {"@type": "g:Map", "@value": []},
        },
        "result": {
            "data": {
                "@type": "g:List",
                "@value": [
                    {
                        "@type": "g:Map",
                        "@value": [
                            "id",
                            "9796",
                            "properties",
                            {
                                "@type": "g:Map",
                                "@value": [
                                    "name",
                                    {"@type": "g:List", "@value": ["PHYHIP"]},
                                ],
                            },
                        ],
                    },
                    {
                        "@type": "g:Map",
                        "@value": [
                            "id",
                            "5297",
                            "properties",
                            {
                                "@type": "g:Map",
                                "@value": [
                                    "name",
                                    {"@type": "g:List", "@value": ["PI4KA"]},
                                ],
                            },
                        ],
                    },
                ],
            },
            "meta": {"@type": "g:Map", "@value": []},
        },
    }

    obj = PollyKG(token, env="testpolly")

    # Test invalid query (empty query should raise an exception)
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.run_gremlin_query("")

    # Test invalid query (wrong query should raise an exception)
    with pytest.raises(RequestException):
        obj.run_gremlin_query("g.V().liit(5).project('id').by(id).by(valueMap())")

    # Mock the post request in session
    response_post = mocker.patch.object(obj.session, "post")
    response_post.return_value.status_code = 200
    response_post.return_value.json.return_value = mocked_response

    # Test valid query
    query = "g.V().count()"
    result = obj.run_gremlin_query(query)

    # Expected result from mocked response
    expected_result = {
        "data": {
            "@type": "g:List",
            "@value": [
                {
                    "@type": "g:Map",
                    "@value": [
                        "id",
                        "9796",
                        "properties",
                        {
                            "@type": "g:Map",
                            "@value": [
                                "name",
                                {"@type": "g:List", "@value": ["PHYHIP"]},
                            ],
                        },
                    ],
                },
                {
                    "@type": "g:Map",
                    "@value": [
                        "id",
                        "5297",
                        "properties",
                        {
                            "@type": "g:Map",
                            "@value": [
                                "name",
                                {"@type": "g:List", "@value": ["PI4KA"]},
                            ],
                        },
                    ],
                },
            ],
        },
        "meta": {"@type": "g:Map", "@value": []},
    }

    assert result == expected_result


def test_run_opencypher_query_success(mocker):
    # Mocked response from API
    mocked_response = {
        "ResponseMetadata": {
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "transfer-encoding": "chunked",
                "content-type": "application/json;charset=UTF-8",
            },
            "RetryAttempts": 0,
        },
        "results": [
            {
                "node": {
                    "~id": "5555",
                    "~entityType": "node",
                    "~labels": ["Gene"],
                    "~properties": {
                        "EnsemblGeneID": "EEEEEEEEEEEEEEEE",
                        "Symbol": "PPPPPPPPP",
                        "LocusTag": "-",
                        "Synonyms": "CCCCCCCCC",
                    },
                }
            }
        ],
    }

    obj = PollyKG(token, env="testpolly")

    # Test invalid query (empty query should raise an exception)
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.run_opencypher_query("")

    with pytest.raises(RequestException):
        obj.run_opencypher_query("abcd")

    # Mock the post request in session
    response_post = mocker.patch.object(obj.session, "post")
    response_post.return_value.status_code = 200
    response_post.return_value.json.return_value = mocked_response

    # Test valid query
    query = "MATCH (node) RETURN node LIMIT 1"
    result = obj.run_opencypher_query(query)

    # Expected result from mocked response
    expected_result = mocked_response["results"]

    assert result == expected_result
