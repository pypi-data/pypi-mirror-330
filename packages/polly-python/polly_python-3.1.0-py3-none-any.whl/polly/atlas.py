from polly.auth import Polly
from polly.session import PollySession
from polly.errors import (
    RequestException,
    ResourceNotFoundError,
    BadRequestError,
    UnauthorizedException,
    ValidationError,
)
from typing import Callable, List, Optional, Dict, Any, Iterator, Union
from requests import Response
import pandas as pd
import json


class Column:
    """
    Attributes:
        name: The name of the column
        col_type: The type of the column
        constraint: The constraint on the column (optional). Can be one of ["PRIMARY KEY", None].
    """

    def __init__(self, name: str, col_type: str, constraint: Optional[str] = None):
        """
        Initializes a Column instance with a given name, type, and optional constraint.

        Args:
            name: The name of the column
            col_type: The type of the column
            constraint: The constraint on the column. If not provided, it will be set to None.

        Examples:
            >>> column = Column(name='patient_id', col_type='string', constraint='PRIMARY_KEY')
        """

        self.name = name
        self.col_type = col_type
        self.constraint = constraint if constraint == "PRIMARY KEY" else None

    def __repr__(self):
        return f"Column(name='{self.name}', col_type='{self.col_type}', constraint='{self.constraint}')"


class Table:
    """
    Attributes:
        atlas_id: The unique identifier for the Atlas
        name: The name of the table
        columns: List of columns in the table
    """

    atlas_id: str
    name: str
    columns: List[Column]

    def __init__(self, atlas_id: str, name: str, columns: List[Column] = None):
        """
        Initializes an instance of a Table with the unique identifier atlas_id, table_name and optional list of columns

        Args:
            atlas_id: The unique identifier for the Atlas.
            name: The name of the table to be initialized.
            columns: List of column objects representing the columns in the table.

        Examples:
            >>> table = Table(atlas_id='1234', name='my_table')
        """
        self.atlas_id = atlas_id
        self._get_session: Callable[[], PollySession] = lambda: Polly.default_session
        self._get_session().headers["Accept"] = "application/vnd.api+json"
        self._get_session().headers["Accept-Encoding"] = "gzip"
        self.name = name
        self.columns = columns if columns else self.list_columns()

    @classmethod
    def from_kwargs(cls, atlas_id: str, **kwargs):
        name: str = kwargs.get("name")
        col_dict = kwargs.get("columns")
        columns: List[Column] = [Column(**column) for column in col_dict]
        return cls(atlas_id, name, columns)

    def __repr__(self):
        return f"Table(name='{self.name}', columns={self.columns})"

    def list_columns(self) -> List[Column]:
        """
        Retrieve the list of columns associated with the table.

        Returns:
            A list of Column objects representing the columns in the table.

        Examples:
            >>> patient_table = Table(atlas_id='atlas_1', name='patient')
            >>> columns = patient_table.list_columns()
        """
        url = f"{self._get_session().atlas_domain_url}/atlas/{self.atlas_id}/tables/{self.name}"
        response = self._get_session().get(url=url)
        validated_response = handle_success_and_error_response(response=response)
        all_columns = []
        if validated_response:
            for column in validated_response["data"]["attributes"]["columns"]:
                all_columns.append(
                    Column(column["name"], column["col_type"], column["constraint"])
                )
        return all_columns

    def get_column(self, column_name: str) -> Column:
        """
        Retrieves a specific column from the table based on its name.

        Args:
            column_name: The name of the column to retrieve.

        Returns:
            The Column object representing the specified column.

        Raises:
            ValueError: If no column with the specified name is found in the table.

        Examples:
            >>> patient_table = Table(atlas_id='atlas_1', name='patient')
            >>> column = table.get_column(column_name='patient_id')
        """
        url = f"{self._get_session().atlas_domain_url}/atlas/{self.atlas_id}/tables/{self.name}/columns/{column_name}"
        response = self._get_session().get(url=url)
        validated_response = handle_success_and_error_response(response=response)
        if validated_response:
            return Column(
                validated_response["data"]["attributes"]["name"],
                validated_response["data"]["attributes"]["col_type"],
                validated_response["data"]["attributes"]["constraint"],
            )

    def add_column(self, column: Column) -> Column:
        """
        Adds a new column to the table.

        Args:
            column: The Column object representing the column to add.

        Returns:
            The Column object that was added to the table.

        Examples:
            >>> patient_table = Table(atlas_id='atlas_1', name='patient')
            >>> new_column = Column(name='patient_age', col_type='int', constraint="PRIMARY KEY")
            >>> added_column = patient_table.add_column(column=new_column)
        """
        url = f"{self._get_session().atlas_domain_url}/atlas/{self.atlas_id}/tables/{self.name}/columns"
        payload = {
            "data": {
                "type": "column",
                "id": column.name,
                "attributes": {
                    "name": column.name,
                    "col_type": column.col_type,
                    "constraint": column.constraint,
                },
            }
        }
        response = self._get_session().post(url=url, json=payload)
        validated_response = handle_success_and_error_response(response=response)
        if validated_response:
            column = Column(
                validated_response["data"]["attributes"]["name"],
                validated_response["data"]["attributes"]["col_type"],
                validated_response["data"]["attributes"]["constraint"],
            )
            self.columns.append(column)
            return column

    def delete_column(self, column_name: str) -> None:
        """
        Deletes a column from the table based on its name.

        Args:
            column_name: The name of the column to be deleted

        Examples:
            >>> patient_table = Table(atlas_id='atlas_1', name='patient')
            >>> patient_table.delete_column(column_name='patient_age')
        """
        url = f"{self._get_session().atlas_domain_url}/atlas/{self.atlas_id}/tables/{self.name}/columns/{column_name}"
        response = self._get_session().delete(url=url)
        validated_response = handle_success_and_error_response(response=response)
        if validated_response:
            self.columns = [
                column for column in self.columns if column.name != column_name
            ]

    def add_rows(self, rows: List[dict]):
        """
        Adds new rows to the tabl

        Args:
            rows: A list of key-value pairs representing rows to be added.

        Examples:
            >>> patient_table = Table(atlas_id='atlas_1', name='patient')
            >>> rows = [
            >>>     {"patient_id": "P0311", "patient_age": 23},
            >>>     {"patient_id": "P0312", "patient_age": 24},
            >>> ]
            >>> patient_table.add_rows(rows)
        """
        url = f"{self._get_session().atlas_domain_url}/atlas/{self.atlas_id}/tables/{self.name}/rows"
        payload = {
            "data": {
                "type": "rows",
                "attributes": {"operation": "add", "rows": rows},
            }
        }
        response = self._get_session().post(url=url, json=payload)
        validated_response = handle_success_and_error_response(response=response)
        if validated_response:
            print(validated_response["data"])

    def delete_rows(self, rows: List[dict]):
        """
        Deletes rows from the table based on the column value

        Args:
            rows: A list of key-value pairs representing rows to delete,
                where the key is the primary key column name and value is the corresponding entry.

        Examples:
            >>> patient_table = Table(atlas_id='atlas_1', name='patient')
            >>> rows = [
            >>>     {'patient_id': 'P0311'},
            >>>     {'patient_id': 'P0322'}
            >>> ]
            >>> patient_table.delete_rows(rows=rows)
        """
        url = f"{self._get_session().atlas_domain_url}/atlas/{self.atlas_id}/tables/{self.name}/rows"
        payload = {
            "data": {
                "type": "rows",
                "attributes": {"operation": "delete", "rows": rows},
            }
        }
        response = self._get_session().post(url=url, json=payload)
        validated_response = handle_success_and_error_response(response=response)
        if validated_response:
            print(validated_response["data"])

    def update_rows(self, rows: List[dict]):
        """
        Updates rows in the table based on provided row data.

        Args:
            rows: A list of dictionaries representing the rows to update.

        Examples:
            >>> patient_table = Table(atlas_id='atlas_1', name='patient')
            >>> rows = [
            >>>    {"patient_id": "P0311", "patient_age": 23},
            >>>    {"patient_id": "P0322", "patient_age": 24},
            >>> ]
            >>> patient_table.update_rows(rows=rows)
        """
        url = f"{self._get_session().atlas_domain_url}/atlas/{self.atlas_id}/tables/{self.name}/rows"
        payload = {
            "data": {
                "type": "rows",
                "attributes": {"operation": "update", "rows": rows},
            }
        }
        response = self._get_session().post(url=url, json=payload)
        validated_response = handle_success_and_error_response(response=response)
        if validated_response:
            print(validated_response["data"])

    def head(self) -> pd.DataFrame:
        """
        Retrieves the first five rows of the table as a Pandas DataFrame.

        Returns:
            A Pandas DataFrame containing the first five rows of the table.

        Examples:
            >>> patient_table = Table(atlas_id='atlas_1', name='patient')
            >>> head_df = patient_table.head()
        """
        url = f"{self._get_session().atlas_domain_url}/atlas/{self.atlas_id}/tables/{self.name}/rows"
        index = ""
        for column in self.columns:
            if column.constraint == "PRIMARY KEY":
                index = column.name
                break
        response = self._get_session().get(url=url)
        validated_response = handle_success_and_error_response(response=response)
        if validated_response:
            rows = validated_response["data"]["rows"]
            return (
                pd.DataFrame(rows, columns=rows[0].keys()).set_index(index)
                if rows
                else pd.DataFrame()
            )

    def iter_rows(self) -> Iterator[List[Dict[str, Any]]]:
        """
        Iterates over the rows of the table in a paginated manner.

        Yields:
            A list of dictionaries representing rows of the table, with column names as keys and corresponding values.

        Examples:
            >>> patient_table = Table(atlas_id='atlas_1', name='patient')
            >>> for page_rows in patient_table.iter_rows():
            >>>     for row in page_rows:
        """
        next = f"/sarovar/atlas/{self.atlas_id}/tables/{self.name}/rows?page[size]=5000&page[number]=1"
        while next:
            url = (
                f"{self._get_session().atlas_domain_url.replace('/sarovar', '')}{next}"
            )
            response = self._get_session().get(url=url)
            validated_response = handle_success_and_error_response(response=response)
            yield validated_response["data"]["rows"]
            next = validated_response["links"]["next"]

    def to_df(self) -> pd.DataFrame:
        """
        Returns the complete table as a Pandas DataFrame.

        Returns:
            A Pandas DataFrame containing the data from the table.

        Examples:
            >>> patient_table = Table(atlas_id='atlas_1', name='patient')
            >>> df = patient_table.to_df()
        """
        index = ""
        for column in self.columns:
            if column.constraint == "PRIMARY KEY":
                index = column.name
                break
        next = f"/sarovar/atlas/{self.atlas_id}/tables/{self.name}/rows?page[size]=5000&page[number]=1"
        all_rows = []
        while next:
            url = (
                f"{self._get_session().atlas_domain_url.replace('/sarovar', '')}{next}"
            )
            response = self._get_session().get(url=url)
            validated_response = handle_success_and_error_response(response=response)
            rows = validated_response["data"]["rows"]
            all_rows.extend(rows)
            next = validated_response["links"]["next"]
        return (
            pd.DataFrame(all_rows, columns=all_rows[0].keys()).set_index(index)
            if all_rows
            else pd.DataFrame()
        )


class Atlas:
    """

    Attributes:
        atlas_id: Atlas ID
    """

    atlas_id: str

    def __init__(self, atlas_id: str):
        """
        Initializes the internal data Atlas with a given Atlas ID

        Args:
            atlas_id: The identifier for the Atlas

        Examples:
            >>> atlas = Atlas(atlas_id='atlas_1')
        """
        self.atlas_id = atlas_id
        self._get_session: Callable[[], PollySession] = lambda: Polly.default_session
        self._get_session().headers["Accept"] = "application/vnd.api+json"
        self._get_session().headers["Accept-Encoding"] = "gzip"

    @classmethod
    def create_atlas(cls, atlas_id: str, atlas_name: str):
        session = Polly.default_session
        session.headers["Accept"] = "application/vnd.api+json"
        session.headers["Accept-Encoding"] = "gzip"
        url = f"{session.atlas_domain_url}/atlas"
        payload = {
            "data": {
                "type": "atlas",
                "attributes": {"id": f"{atlas_id}", "name": f"{atlas_name}"},
            }
        }
        response = session.post(url=url, json=payload)
        handle_success_and_error_response(response=response)

        return cls(atlas_id=atlas_id)

    @classmethod
    def delete_atlas(cls, atlas_id: str):
        session = Polly.default_session
        session.headers["Accept"] = "application/vnd.api+json"
        session.headers["Accept-Encoding"] = "gzip"
        url = f"{session.atlas_domain_url}/atlas/{atlas_id}"
        response = session.delete(url=url)
        handle_success_and_error_response(response=response)

    @classmethod
    def list_atlases(cls):
        session = Polly.default_session
        session.headers["Accept"] = "application/vnd.api+json"
        session.headers["Accept-Encoding"] = "gzip"
        url = f"{session.atlas_domain_url}/atlas"
        response = session.get(url=url)
        validated_response = handle_success_and_error_response(response=response)
        all_atlases = []
        for atlas in validated_response["data"]:
            all_atlases.append(cls(atlas_id=atlas["id"]))

        return all_atlases

    def __repr__(self):
        return f"Atlas(atlas_id={self.atlas_id})"

    def get_name(self) -> str:
        """
        Retrieves the name of the Atlas using the Atlas ID

        Returns:
            The name of the Atlas as a string

        Examples:
            >>> atlas = Atlas(atlas_id='atlas_1')
            >>> atlas.get_name()
            'My Atlas'
        """
        url = f"{self._get_session().atlas_domain_url}/atlas/{self.atlas_id}"
        response = self._get_session().get(url=url)
        validated_response = handle_success_and_error_response(response=response)
        if validated_response:
            return validated_response["data"]["attributes"]["name"]

    def list_tables(self) -> List[Table]:
        """
        Retrieves the list of tables associated with an Atlas.

        Returns:
            A list of Table objects representing the tables associated with an Atlas.

        Examples:
            >>> atlas = Atlas(atlas_id='atlas_1')
            >>> tables = atlas.list_tables()
        """
        url = f"{self._get_session().atlas_domain_url}/atlas/{self.atlas_id}/tables"
        response = self._get_session().get(url=url)
        validated_response = handle_success_and_error_response(response=response)
        all_tables = []
        if validated_response:
            for table_data in validated_response["data"]:
                all_tables.append(
                    Table.from_kwargs(self.atlas_id, **table_data["attributes"])
                )
        return all_tables

    def get_table(self, table_name: str) -> Table:
        """
        Retrieves a specific table object by name.

        Args:
            table_name: The name of the table to retrieve.

        Returns:
            The Table object representing the specified table.

        Notes:
            It loads the table object and not the table data. Use to_df() function to do so.

        Examples:
            >>> atlas = Atlas(atlas_id='1234')
            >>> table = atlas.get_table(table_name='my_table')
        """
        url = f"{self._get_session().atlas_domain_url}/atlas/{self.atlas_id}/tables/{table_name}"
        response = self._get_session().get(url=url)
        validated_response = handle_success_and_error_response(response=response)
        if validated_response:
            return Table.from_kwargs(
                atlas_id=self.atlas_id, **validated_response["data"]["attributes"]
            )

    def create_table(
        self, table_name: str, columns: List[Column], rows: Optional[List[dict]] = None
    ) -> Table:
        """
        Creates a new table with the specified name and columns.

        Args:
            table_name: The name of the new table to create.
            columns: A list of Column objects representing the columns of the new table.
            rows (list, optional): A list of key-value pairs representing the table data.

        Returns:
            The newly created Table object.

        Examples:
            >>> atlas = Atlas(atlas_id='my_atlas')
            >>> columns = [
            >>>    Column(name='patient_id', col_type='integer', constraint='PRIMARY KEY'),
            >>>    Column(name='patient_ name', col_type='string')
            >>> ]
            >>> patient_table = atlas.create_table(table_name='patient', columns=columns)
        """
        url = f"{self._get_session().atlas_domain_url}/atlas/{self.atlas_id}/tables/"
        all_columns = []
        for item in columns:
            column = {
                "name": item.name,
                "col_type": item.col_type,
                "constraint": item.constraint,
            }
            all_columns.append(column)
        payload = {
            "data": {
                "id": table_name,
                "type": "table",
                "attributes": {
                    "name": table_name,
                    "columns": all_columns,
                    "rows": rows,
                },
            }
        }
        response = self._get_session().post(url=url, json=payload)
        validated_response = handle_success_and_error_response(response=response)
        if validated_response:
            return Table.from_kwargs(
                atlas_id=self.atlas_id, **validated_response["data"]["attributes"]
            )

    def create_table_from_df(self, table_name: str, df: pd.DataFrame) -> Table:
        """
        Creates a new table with the specified table name and schema derived from the Pandas DataFrame.

        Optionally loads the data into the table.

        Raises Validation error if the datatype is not supported.

        Supported column types are [int, float, bool, object]

        Args:
            table_name: The name of the new table to create.
            df: A Pandas DataFrame representing the data and schema for the new table

        Returns:
            The newly created table object showing first 5 rows from the table.

        Examples:
            >>> atlas = Atlas(atlas_id='my_atlas')
            >>> data = {'patient_id': ["P0031", "P0032"], 'patient_age': ['Sam', 'Ron']}
            >>> df = pd.DataFrame(data)
            >>> df.set_index('patient_id', inplace=True)
            >>> new_table = atlas.create_table_from_df(table_name='patient', df=df)
        """
        primary_key_name = df.index.name
        primary_key_dtype = df.index.dtype
        if primary_key_name is None:
            raise ValidationError(
                "The dataframe index should have a name. You can set it using df.index.name = '<index_name>'"
            )

        column_datatype_map = {
            str(col_name): str(dtype) for col_name, dtype in df.dtypes.to_dict().items()
        }
        column_datatype_map[str(primary_key_name)] = str(primary_key_dtype)

        for column, column_type in column_datatype_map.items():
            if column_type in ["int64", "int32"]:
                column_datatype_map[column] = "integer"
            elif column_type in ["float64", "float32"]:
                column_datatype_map[column] = "float"
            elif column_type == "bool":
                column_datatype_map[column] = "boolean"
            elif column_type == "object":
                column_datatype_map[column] = "string"
            else:
                pass

        all_columns = []
        for column_name, column_type in column_datatype_map.items():
            constraint = None
            if column_name == primary_key_name:
                constraint = "PRIMARY KEY"  # Adding column with constraint PRIMARY_KEY when column is the dataframe index
            all_columns.append(
                Column(name=column_name, col_type=column_type, constraint=constraint)
            )

        df[str(primary_key_name)] = df.index

        return self.create_table(
            table_name=table_name,
            columns=all_columns,
            rows=json.loads(df.to_json(orient="records")),
        )

    def delete_table(self, table_name: str) -> None:
        """
        Deletes the table from the atlas.

        Args:
            table_name: The name of the table to delete.

        Examples:
            >>> atlas = Atlas(atlas_id='atlas_1')
            >>> atlas.delete_table(table_name='patient')
        """
        url = f"{self._get_session().atlas_domain_url}/atlas/{self.atlas_id}/tables/{table_name}"
        response = self._get_session().delete(url=url)
        handle_success_and_error_response(response=response)

    def query(
        self, query: str, format: Optional[str] = None
    ) -> Union[pd.DataFrame, List[Dict]]:
        """
        Executes a query on the Atlas tables.

        Args:
            query: The SQL query to execute.

        Returns:
            The result of the query execution.

        Examples:
            >>> atlas = Atlas(atlas_id='atlas_1')
            >>> result = atlas.query(query='SELECT * FROM patient;')
        """
        url = f"{self._get_session().atlas_domain_url}/atlas/{self.atlas_id}/queries"
        payload = {
            "data": {
                "id": self.atlas_id,
                "type": "query",
                "attributes": {"id": self.atlas_id, "query": query},
            }
        }
        response = self._get_session().post(url=url, json=payload)
        validated_response = handle_success_and_error_response(response=response)
        if validated_response:
            if format == "json":
                return validated_response["data"]["results"]

        return pd.DataFrame(validated_response["data"]["results"])


def handle_success_and_error_response(response: Response):
    if response.status_code in [200, 201]:
        return response.json()
    if response.status_code == 204:
        return None
    if response.status_code == 401:
        raise UnauthorizedException()
    if (
        response.status_code in [400, 401, 402, 403, 404]
        and "errors" in response.json()
    ):
        if isinstance(response.json()["errors"], list):
            error_message = response.json()["errors"][0]["detail"]
        else:
            error_message = response.json()["errors"]
    if response.status_code == 400:
        raise BadRequestError(detail=error_message)
    if response.status_code == 404:
        raise ResourceNotFoundError(detail=error_message)
    if response.status_code == 413:
        raise RequestException(title="Payload Too Large")
    if response.status_code >= 500:
        response.raise_for_status()
    response.raise_for_status()
