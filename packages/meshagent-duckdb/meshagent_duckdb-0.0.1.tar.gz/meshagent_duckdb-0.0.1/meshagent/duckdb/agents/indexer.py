from meshagent.agents import TaskRunner, RequiredToolkit

class DuckDbIndexer(TaskRunner):

    
    def __init__(self,
         *, 
        name,
        title=None,
        description=None,
        requires=None,
        supports_tools = None,
    ):
        super().__init__(
            name=name,
            title=title,
            description=description,
            requires=[
                RequiredToolkit(
                    name="meshagent.duckdb",
                    tools=[
                        "duckdb_open_database",
                        "duckdb_query",
                        "duckdb_prepared_query"
                    ]
                ),
            ],
            supports_tools=supports_tools,
            input_schema={
                "type" : "object",
                "required" : [
                    "queue", "database", "table"
                ],
                "additionalProperties" : False,
                "properties" : {
                    "queue" : {
                        "type" : "string",
                        "description" : "default: firecrawl"
                    },
                    "database" : {
                        "type" : "string",
                        "description" : "default: indexes"
                    },
                    "table" : {
                        "type" : "string",
                        "description" : "default: index"
                    }
                }
            },
            output_schema={
                "type" : "object",
                "required" : [],
                "additionalProperties" : False,
                "properties" : {},
            }
        )

    async def ask(self, *, context, arguments):
        
        queue = arguments["queue"]
        database = arguments["database"]
        table = arguments["table"]

        await context.room.agents.invoke_tool(
            toolkit="meshagent.duckdb",
            tool="duckdb_ensure_database_open",
            arguments={
                "database": database
            })

        await context.room.agents.invoke_tool(
            toolkit="meshagent.duckdb",
            tool="duckdb_query",
            arguments={
                "database": database,
                "query" : f"create table if not exists {table} (url text unique, markdown text)" 
            })

        while True:
            message = await context.room.queues.receive(name=queue, create=True, wait=True)
            if message == None:
                break

            print(message)
            await context.room.agents.invoke_tool(
                toolkit="meshagent.duckdb",
                tool="duckdb_prepared_query",
                arguments={
                    "database": database,
                    "query" : f"insert into {table} (url, markdown) values ($url, $markdown) on conflict (url) DO UPDATE SET markdown = $markdown",
                    "parameters" : [ 
                        {
                            "name" : "url",
                            "value" : message["data"]["metadata"]["url"],
                        },
                        {
                            "name" : "markdown",
                            "value" : message["data"]["markdown"]
                        }  
                    ]
                })
            
        return {}

    

    