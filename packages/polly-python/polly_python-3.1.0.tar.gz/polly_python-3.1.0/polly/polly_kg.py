from polly.auth import Polly
from polly.errors import (
    InvalidParameterException,
    error_handler,
    AccessDeniedError,
    RequestFailureException,
    QueryFailedException,
    ResourceNotFoundError,
)
from polly import helpers
from polly import constants as const
from polly.tracking import Track

import requests
import json
import logging


class PollyKG:
    """The PollyKG class provides an interface to interact with the Polly Knowledge Graph (KG) API.\
     It enables users to execute and manage Gremlin and OpenCypher queries, retrieve node and relationship data,\
     and analyze graph structures efficiently. This class simplifies access to the KG engine, allowing seamless\
     querying and data exploration. It is designed for users who need to extract insights from complex graph-based datasets.

    Args:
        token (str): Authentication token from polly

    Usage:
        from polly.polly_kg import PollyKG

        kg = PollyKG(token)
    """

    def __init__(self, token=None, env="", default_env="polly") -> None:
        # Initialize a PollyKG instance.

        # Args:
        #     token (str, optional): Authentication token. Defaults to None.
        #     env (str, optional): Environment override. Defaults to "".
        #     default_env (str, optional): Default environment if not specified. Defaults to "polly".

        env = helpers.get_platform_value_from_env(
            const.COMPUTE_ENV_VARIABLE, default_env, env
        )
        self.session = Polly.get_session(token, env=env)
        self.polly_kg_endpoint = (
            f"https://apis.{self.session.env}.elucidata.io/polly-kg"
        )
        if self.session.env == "polly":
            self.env_string = "prod"
        elif self.session.env == "testpolly":
            self.env_string = "test"
        else:
            self.env_string = "devenv"

    @Track.track_decorator
    def get_engine_status(self) -> dict:
        """Retrieve a status of the Polly Knowledge Graph.

        Returns:
            dict: A dictionary containing status information about the engine,
                 such as gremlin, opencypher.

        Raises:
            ResourceNotFoundError: Raised when the specified graph does not exist.
            AccessDeniedError: Raised when the user does not have permission to access the graph status.
            RequestFailureException: Raised when the request fails due to an unexpected error.

        Examples:
            >>> kg = PollyKG()
            >>> status = kg.get_engine_status()
        """
        try:
            response = self.session.get(f"{self.polly_kg_endpoint}/status")
            response.raise_for_status()
            print(response.json())
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            if http_err.response.status_code == 404:
                raise ResourceNotFoundError("Graph not found.")
            elif http_err.response.status_code == 403:
                raise AccessDeniedError("Access denied to graph status.")
            logging.error(f"HTTP error occurred: {http_err}")
            raise RequestFailureException()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error retrieving graph status: {e}")
            raise RequestFailureException()

    @Track.track_decorator
    def get_graph_summary(self) -> dict:
        """Retrieve a summary of the Polly Knowledge Graph.

        Returns:
            dict: A dictionary containing summary information about the graph,
                 such as node counts, edge counts, and other metadata.

        Raises:
            ResourceNotFoundError: Raised when the specified graph summary does not exist.
            AccessDeniedError: Raised when the user does not have permission to access the graph summary.
            RequestFailureException: Raised when the request fails due to an unexpected error.

        Examples:
            >>> kg = PollyKG()
            >>> summary = kg.get_graph_summary()
        """
        try:
            response = self.session.get(f"{self.polly_kg_endpoint}/summary")
            error_handler(response)
            print(response.json())
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            if http_err.response.status_code == 404:
                raise ResourceNotFoundError("Graph summary not found.")
            elif http_err.response.status_code == 403:
                raise AccessDeniedError("Access denied to graph summary.")
            logging.error(f"HTTP error occurred: {http_err}")
            raise RequestFailureException()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error retrieving graph summary: {e}")
            raise RequestFailureException()

    @Track.track_decorator
    def run_opencypher_query(self, query: str) -> dict:
        """Execute a opencypher query against the Polly KG endpoint.

        Args:
            query (str): The opencypher query to execute.

        Returns:
            dict: The query execution results.

        Raises:
            InvalidParameterException: Raised when the query is empty or None.
            RequestFailureException: Raised when the request fails due to an unexpected error.
            QueryFailedException: Raised when the query execution fails due to a timeout.

        Examples:
            >>> kg = PollyKG()
            >>> query = "your query"
            >>> summary = kg.run_opencypher_query(query)
        """
        if not query or query == "":
            raise InvalidParameterException("query")

        payload = {"query_content": query}

        try:
            response = self.session.post(
                f"{self.polly_kg_endpoint}/opencypher/query", data=json.dumps(payload)
            )
            error_handler(response)
            return response.json()["results"]
        except requests.exceptions.HTTPError as http_err:
            if (
                http_err.response.status_code == 408
                or "timeout" in str(http_err).lower()
            ):
                logging.error("Query execution timed out")
                raise QueryFailedException(
                    "Time limit exceeded, please optimize the query or contact polly.support@elucidata.io"
                )
            logging.error(f"HTTP error occurred: {http_err}")
            raise RequestFailureException()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error executing query: {e}")
            raise RequestFailureException()

    @Track.track_decorator
    def run_gremlin_query(self, query: str) -> dict:
        """Execute a Gremlin query against the Polly KG endpoint.

        Args:
            query (str): The Gremlin query to execute.

        Returns:
            dict: The query execution results.

        Raises:
            InvalidParameterException: Raised when the query is empty or None.
            RequestFailureException: Raised when the request fails due to an unexpected error.
            QueryFailedException: Raised when the query execution fails due to a timeout.

        Examples:
            >>> kg = PollyKG()
            >>> query = "your query"
            >>> summary = kg.run_gremlin_query(query)
        """
        if not query or query == "":
            raise InvalidParameterException("query")

        payload = {"query_content": query}

        try:
            response = self.session.post(
                f"{self.polly_kg_endpoint}/gremlin/query", data=json.dumps(payload)
            )
            error_handler(response)
            return response.json()["result"]
        except requests.exceptions.HTTPError as http_err:
            if (
                http_err.response.status_code == 408
                or "timeout" in str(http_err).lower()
            ):
                logging.error("Query execution timed out")
                raise QueryFailedException(
                    "Time limit exceeded, please optimize the query or contact polly.support@elucidata.io"
                )
            logging.error(f"HTTP error occurred: {http_err}")
            raise RequestFailureException()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error executing query: {e}")
            raise RequestFailureException()
