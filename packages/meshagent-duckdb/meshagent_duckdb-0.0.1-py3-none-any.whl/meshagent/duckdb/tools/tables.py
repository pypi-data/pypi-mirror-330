import duckdb
import pyarrow as pa
import pyarrow.parquet as pq
import io
import logging
from typing import Optional, Dict

from meshagent.tools import Tool, Toolkit, JsonResponse, ToolContext
from meshagent.api import RoomException

logger = logging.getLogger("duckdb_parquet_tools")
logger.setLevel(logging.INFO)


class ListOpenDatabasesTool(Tool):
    """
    list the currently open databases'.
    """
    def __init__(self, open_databases: Dict[str, Dict]):
        self.open_databases = open_databases
        super().__init__(
            name="duckdb_list_databases",
            title="List DuckDB databases",
            description=(
                "List the currently open databases"
            ),
            input_schema={
                "type": "object",
                "required": [],
                "additionalProperties" : False,
                "properties": {
                  
                }
            }
        )

    async def execute(self, *, context: ToolContext):
        try:
            return JsonResponse(json={"databases" :  list(map(lambda x: [ { "name": x } ], self.open_databases.keys())) })
        except duckdb.Error as err:
                raise RoomException(str(err))


class OpenDatabaseTool(Tool):
    """
    Opens an empty database with an in-memory DuckDB connection'.
    """
    def __init__(self, open_databases: Dict[str, Dict]):
        self.open_databases = open_databases
        super().__init__(
            name="duckdb_open_database",
            title="New DuckDB database",
            description=(
                "Open a DuckDB in-memory database in the room. The database will be empty. Will return an error if the database is already open."
            ),
            input_schema={
                "type": "object",
                "required": ["database"],
                "additionalProperties" : False,
                "properties": {
                    "database": {
                        "type": "string",
                        "description": "Identifier for this 'database'"
                    }
                }
            }
        )

    async def execute(self, *, context: ToolContext, database: str):
        try:
            # Access the toolkit
            if database in self.open_databases:
                # Already open
                raise RoomException("The a database with the same name is already open")

         
            # Create an in-memory connection
            conn = duckdb.connect(database=':memory:')

            # Store in the open_databases dictionary
            self.open_databases[database] = {
                "connection": conn,
            }

            return JsonResponse({"status": "opened", "database": database})
        except duckdb.Error as err:
                raise RoomException(str(err))


class EnsureDatabaseOpenTool(Tool):
    """
    Open a database if it is not open, and loads it into an in-memory DuckDB connection'.
    """
    def __init__(self, open_databases: Dict[str, Dict]):
        self.open_databases = open_databases
        super().__init__(
            name="duckdb_ensure_database_open",
            title="Ensure DuckDB database open",
            description=(
                "Open a DuckDB in-memory database in the room if it is not open. The database will be empty."
            ),
            input_schema={
                "type": "object",
                "required": ["database"],
                "additionalProperties" : False,
                "properties": {
                    "database": {
                        "type": "string",
                        "description": "Identifier for this 'database'"
                    },
                }
            }
        )

    async def execute(self, *, context: ToolContext, database: str):
        try:
            # Access the toolkit
            if database in self.open_databases:
                # Already open
                return {"status": "opened", "database": database}

         
            # Create an in-memory connection
            conn = duckdb.connect(database=':memory:')

            # Store in the open_databases dictionary
            self.open_databases[database] = {
                "connection": conn,
            }

            return JsonResponse({"status": "opened", "database": database})
        except duckdb.Error as err:
                raise RoomException(str(err))

class ImportParquetTableTool(Tool):
    """
    Reads a Parquet file from room storage and loads it into an in-memory DuckDB connection as a view.
    """
    def __init__(self, open_databases: Dict[str, Dict]):
        self.open_databases = open_databases
        super().__init__(
            name="duckdb_import_parquet_table",
            title="Import a DuckDB Parquet-based database",
            description="import a Parquet file in room storage at the desired path into a table with the specified name",
            input_schema={
                "type": "object",
                "required": ["database","path", "table"],
                "additionalProperties" : False,
                "properties": {
                    "database": {
                        "type": "string",
                        "description": "Identifier for this 'database' (one Parquet file)."
                    },
                    "path": {
                        "type": "string",
                        "description": "the full path to the parquet file"
                    },
                    "table": {
                        "type": "string",
                        "description": "the name of the table to load the data into"
                    }
                }
            }
        )

    async def execute(self, *, context: ToolContext, database: str, path: str, table: str):
        try:
            # Access the toolkit
            if database not in self.open_databases:

                raise RoomException(f"The a database with the name {database} is not open")
          
            # Create an in-memory connection
            conn : duckdb.DuckDBPyConnection = self.open_databases[database]["connection"]

            # Attempt to download Parquet file from storage
            parquet_bytes = (await context.room.storage.download(path=path)).data
            arrow_table = pq.read_table(io.BytesIO(parquet_bytes))

            view_name = f"__import_{database}"
            conn.register(view_name, arrow_table)
            try:
                conn.execute(f"""
                    CREATE TABLE {table} AS
                        SELECT * 
                        FROM {view_name};             
                """)
            finally:
                conn.unregister(view_name)
            

            logger.info(f"Loaded {database} from {path} into {table}.")


            return JsonResponse({"status": "imported", "database": database, "table" : table, "path" : path})
        except duckdb.Error as err:
            raise RoomException(str(err))

class ExportParquetTableTool(Tool):
    """
    Saves the table content (in memory) to a Parquet file.
    The database remains open afterward.
    """
    def __init__(self, open_databases: Dict[str, Dict]):
        self.open_databases = open_databases
        super().__init__(
            name="duckdb_export_parquet_table",
            title="Export DuckDB Table",
            description="Saves the table to Parquet in room storage, overwriting the existing file.",
            input_schema={
                "type": "object",
                "required": ["database","path", "table"],
                "additionalProperties" : False,
                "properties": {
                    "database": {
                        "type": "string",
                        "description": "The database to save."
                    },
                    "path": {
                        "type": "string",
                        "description": "The path to save the database to (should end with .parquet)"
                    },
                    "table": {
                        "type": "string",
                        "description": "The table to save."
                    }
                }
            }
        )

    async def execute(self, *, context: ToolContext, database: str, table: str, path: str):
        try:
            if database not in self.open_databases:
                raise RoomException(f"Database '{database}' is not open.")

            db_info = self.open_databases[database]
            conn : duckdb.DuckDBPyConnection = db_info["connection"]
         
            # Fetch the entire dbtable as Arrow
            arrow_table = conn.table(table).arrow()

            # Convert to parquet bytes in-memory
            buf = pa.BufferOutputStream()
            pq.write_table(arrow_table, buf)
            parquet_bytes = buf.getvalue().to_pybytes()

            # Write to storage
            handle = await context.room.storage.open(path=path, overwrite=True)
            try:
                await context.room.storage.write(handle=handle, data=parquet_bytes)
            finally:
                await context.room.storage.close(handle=handle)

            logger.info(f"Saved {database}.{table} to {path}")
            return JsonResponse({"status": "exported", "database": database, "table" : table, "path" : path})
        except duckdb.Error as err:
            raise RoomException(str(err))


class CloseParquetTableTool(Tool):
    """
    Closes the DuckDB in-memory connection for the specified database
    """
    def __init__(self, open_databases: Dict[str, Dict]):
        self.open_databases = open_databases
        super().__init__(
            name="duckdb_close_database",
            title="Close a DuckDB database",
            description="Remove the in-memory DuckDB connection.",
            input_schema={
                "type": "object",
                "additionalProperties" : False,
                "required": ["database"],
                "properties": {
                    "database": {
                        "type": "string",
                        "description": "The database to close."
                    },
                }
            }
        )

    async def execute(self, *, context: ToolContext, database: str):

        try:
            if database not in self.open_databases:
                raise RoomException(f"Database '{database}' is not open.")

            db_info = self.open_databases[database]
            conn : duckdb.DuckDBPyConnection  = db_info["connection"]

            # Now close the connection and remove from dictionary
            conn.close()
            del self.open_databases[database]

            logger.info(f"Closed database '{database}'.")
            return JsonResponse({"status": "closed", "database": database})
        
        except duckdb.Error as err:
                raise RoomException(str(err))


class ExecuteQueryTool(Tool):
    """
    Executes a SQL query against the open in-memory DuckDB database.
    Returns the results as JSON with a "rows" property (list of dicts).
    For non-SELECT queries, "rows" will be empty.
    """
    def __init__(self, open_databases: Dict[str, Dict]):
        self.open_databases = open_databases
        super().__init__(
            name="duckdb_query",
            title="Execute DuckDB SQL query",
            description="Execute a SQL query against an in-memory DuckDB database. Returns rows as JSON.",
            input_schema={
                "type": "object",
                "required": ["database", "query"],
                "additionalProperties" : False,
                "properties": {
                    "database": {
                        "type": "string",
                        "description": "The database name to query (must already be open)."
                    },
                    "query": {
                        "type": "string",
                        "description": "The SQL statement to execute."
                    }
                }
            }
        )

    async def execute(self, *, context: ToolContext, database: str, query: str):
        try:

            close = False
            try:
                if database not in self.open_databases:
                    
                    raise RoomException(f"The database {database} is not open.")
                    close = True
                    # Build the storage path
                    storage_path = f".databases/{database}.parquet"

                    # Create an in-memory connection
                    conn = duckdb.connect(database=':memory:')

                    # Attempt to download Parquet file from storage
                    parquet_bytes = (await context.room.storage.download(path=storage_path)).data
                    arrow_table = pq.read_table(io.BytesIO(parquet_bytes))

                    conn.register("dbtable", arrow_table)

                else:
                    conn : duckdb.DuckDBPyConnection = self.open_databases[database]["connection"]

                # Execute the query
                cursor = conn.execute(query)
                description = cursor.description

                rows_data = []
                if description is not None:
                    # SELECT-like queries
                    all_rows = cursor.fetchall()
                    columns = [desc[0] for desc in description]
                    for row in all_rows:
                        row_dict = {}
                        for idx, col_name in enumerate(columns):
                            row_dict[col_name] = row[idx]
                        rows_data.append(row_dict)
            
            except Exception as e:
                if close:
                    conn.close()
                raise

        except duckdb.Error as err:
            raise RoomException(str(err))

        return JsonResponse({"rows": rows_data, "columns" : columns })


class ExecutePreparedQueryTool(Tool):
    """
    Executes a SQL query against the open in-memory DuckDB database.
    Returns the results as JSON with a "rows" property (list of dicts).
    For non-SELECT queries, "rows" will be empty.
    """
    def __init__(self, open_databases: Dict[str, Dict]):
        self.open_databases = open_databases
        super().__init__(
            name="duckdb_prepared_query",
            title="Execute DuckDB prepared query",
            description="Execute a SQL query against an in-memory DuckDB database. Returns rows as JSON.",
            input_schema={
                "type": "object",
                "required": ["database", "query", "parameters"],
                "additionalProperties" : False,
                "properties": {
                    "database": {
                        "type": "string",
                        "description": "The database name to query (must already be open)."
                    },
                    "query": {
                        "type": "string",
                        "description": "The SQL statement to execute."
                    },
                    "parameters": {
                        "type": "array",
                        "items" : {
                            "anyOf" : [ 
                                {
                                    "type" : "object",
                                    "required" : [ "string" ],
                                    "additionalProperties" : False,
                                    "properties" : {
                                        "string" :  {
                                            "type" : "string"
                                        },
                                    }
                                },
                                {
                                    "type" : "object",
                                    "required" : [ "number" ],
                                    "additionalProperties" : False,
                                    "properties" : {
                                        "number" :  {
                                            "type" : "number"
                                        },
                                    }
                                },
                                {
                                    "type" : "object",
                                    "required" : [ "boolean" ],
                                    "additionalProperties" : False,
                                    "properties" : {
                                        "boolean" :  {
                                            "type" : "boolean"
                                        },
                                    }
                                },
                                {
                                    "type" : "object",
                                    "required" : [ "null" ],
                                    "additionalProperties" : False,
                                    "properties" : {
                                        "null" : {
                                            "type" : "null",
                                        },
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        )

    async def execute(self, *, context: ToolContext, database: str, query: str, parameters: list):
        try:

            close = False
            try:
                if database not in self.open_databases:
                    
                    raise RoomException(f"The database {database} is not open.")
                    close = True
                    # Build the storage path
                    storage_path = f".databases/{database}.parquet"

                    # Create an in-memory connection
                    conn = duckdb.connect(database=':memory:')

                    # Attempt to download Parquet file from storage
                    parquet_bytes = (await context.room.storage.download(path=storage_path)).data
                    arrow_table = pq.read_table(io.BytesIO(parquet_bytes))

                    conn.register("dbtable", arrow_table)

                else:
                    conn : duckdb.DuckDBPyConnection = self.open_databases[database]["connection"]
                
                parameters_dict = dict()

                parameter : dict
                for parameter in parameters:
                    parameters_dict[parameter["name"]] = parameter[list(parameter.items())[0]["key"]]["value"]

                # Execute the query
                cursor = conn.execute(query, parameters_dict)
                description = cursor.description

                rows_data = []
                if description is not None:
                    # SELECT-like queries
                    all_rows = cursor.fetchall()
                    columns = [desc[0] for desc in description]
                    for row in all_rows:
                        row_dict = {}
                        for idx, col_name in enumerate(columns):
                            row_dict[col_name] = row[idx]
                        rows_data.append(row_dict)
            
            except Exception as e:
                if close:
                    conn.close()
                raise

        except duckdb.Error as err:
            raise RoomException(str(err))

        return JsonResponse({"rows": rows_data, "columns" : columns })


class DuckDbToolkit(Toolkit):
    """
    A Toolkit providing tools to open, save, close, and query
    Each database is purely in-memory and must be saved
    """
    def __init__(self):
        open_databases: Dict[str, Dict] = {}
        super().__init__(
            name="meshagent.duckdb",
            title="duckdb",
            thumbnail_url="https://storage.googleapis.com/meshagent-assets/duckdb.jpeg",
            description=(
                "Tools for interacting with an in-memory DuckDB instance."
            ),
            tools=[
                ListOpenDatabasesTool(open_databases=open_databases),
                EnsureDatabaseOpenTool(open_databases=open_databases),
                OpenDatabaseTool(open_databases=open_databases),
                ImportParquetTableTool(open_databases=open_databases),
                ExportParquetTableTool(open_databases=open_databases),
                CloseParquetTableTool(open_databases=open_databases),
                ExecuteQueryTool(open_databases=open_databases),
                ExecutePreparedQueryTool(open_databases=open_databases)
            ],
        )
        