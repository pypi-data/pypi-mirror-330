# postgres_server.py
import asyncpg
from mcp.server.fastmcp import FastMCP, Context
from contextlib import asynccontextmanager
from typing import AsyncIterator, List, Dict, Any, Optional

# Create an MCP server
mcp = FastMCP("PostgreSQL")

# Database connection class
class PostgresDB:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.conn = None
    
    async def connect(self):
        self.conn = await asyncpg.connect(self.connection_string)
    
    async def disconnect(self):
        if self.conn:
            await self.conn.close()
    
    async def execute_query(self, query: str, params: Optional[List[Any]] = None) -> List[Dict[str, Any]]:
        if not self.conn:
            raise ValueError("Database not connected")
        
        params = params or []
        try:
            # For SELECT queries that return data
            if query.strip().upper().startswith("SELECT"):
                rows = await self.conn.fetch(query, *params)
                return [dict(row) for row in rows]
            # For INSERT/UPDATE/DELETE queries that return affected row count
            else:
                result = await self.conn.execute(query, *params)
                return [{"result": result}]
        except Exception as e:
            return [{"error": str(e)}]
    
    async def list_tables(self) -> List[Dict[str, Any]]:
        query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
        """
        return await self.execute_query(query)
    
    async def describe_table(self, table_name: str) -> List[Dict[str, Any]]:
        query = """
        SELECT 
            column_name, 
            data_type, 
            is_nullable,
            column_default
        FROM 
            information_schema.columns
        WHERE 
            table_schema = 'public' AND 
            table_name = $1
        ORDER BY 
            ordinal_position;
        """
        return await self.execute_query(query, [table_name])

# Server lifespan for database connection management
@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[Dict[str, Any]]:
    # Get connection string from environment or use default
    connection_string = server.env.get("DATABASE_URL", "")
    
    if not connection_string:
        server.logger.warning("No DATABASE_URL provided. Please set it when installing the server.")
        yield {"db": None}
        return
    
    # Initialize database connection
    db = PostgresDB(connection_string)
    try:
        await db.connect()
        server.logger.info("Connected to PostgreSQL database")
        yield {"db": db}
    finally:
        await db.disconnect()
        server.logger.info("Disconnected from PostgreSQL database")

# Set up the server with the lifespan
mcp = FastMCP("PostgreSQL", lifespan=lifespan)

@mcp.resource("postgres://info")
def get_postgres_info() -> str:
    """Get information about the PostgreSQL server"""
    return """
    PostgreSQL MCP Server
    
    This server provides tools to interact with a PostgreSQL database.
    
    Available tools:
    - query: Execute SQL queries
    - list_tables: List all tables in the database
    - describe_table: Get column information for a specific table
    
    To use this server, you need to provide a DATABASE_URL when installing:
    mcp install postgres_server.py -v DATABASE_URL=postgresql://user:password@host:port/dbname
    """

@mcp.tool()
async def query(sql: str, ctx: Context) -> str:
    """
    Execute a SQL query on the PostgreSQL database.
    
    Parameters:
    - sql: SQL query to execute
    
    Returns the query results or error message.
    """
    db = ctx.request_context.lifespan_context.get("db")
    if not db:
        return "Error: Database connection not available. Please check your DATABASE_URL."
    
    ctx.info(f"Executing query: {sql}")
    results = await db.execute_query(sql)
    
    # Format the results as a string
    if not results:
        return "Query executed successfully. No results returned."
    
    if "error" in results[0]:
        return f"Error executing query: {results[0]['error']}"
    
    # Format as table for SELECT queries
    if "result" in results[0]:  # This is an INSERT/UPDATE/DELETE result
        return results[0]["result"]
    
    # Format SELECT results as a table
    headers = results[0].keys()
    header_row = " | ".join(str(h) for h in headers)
    separator = "-" * len(header_row)
    rows = [header_row, separator]
    
    for row in results:
        rows.append(" | ".join(str(row.get(h, "")) for h in headers))
    
    return "\n".join(rows)

@mcp.tool()
async def list_tables(ctx: Context) -> str:
    """
    List all tables in the PostgreSQL database.
    
    Returns a list of table names.
    """
    db = ctx.request_context.lifespan_context.get("db")
    if not db:
        return "Error: Database connection not available. Please check your DATABASE_URL."
    
    ctx.info("Listing database tables")
    results = await db.list_tables()
    
    if not results:
        return "No tables found in the database."
    
    return "Tables in database:\n" + "\n".join(f"- {row['table_name']}" for row in results)

@mcp.tool()
async def describe_table(table_name: str, ctx: Context) -> str:
    """
    Describe the structure of a table.
    
    Parameters:
    - table_name: Name of the table to describe
    
    Returns column information for the specified table.
    """
    db = ctx.request_context.lifespan_context.get("db")
    if not db:
        return "Error: Database connection not available. Please check your DATABASE_URL."
    
    ctx.info(f"Describing table: {table_name}")
    results = await db.describe_table(table_name)
    
    if not results:
        return f"Table '{table_name}' not found or has no columns."
    
    # Format as table
    headers = ["column_name", "data_type", "is_nullable", "column_default"]
    header_row = " | ".join(headers)
    separator = "-" * len(header_row)
    rows = [header_row, separator]
    
    for row in results:
        rows.append(" | ".join(str(row.get(h, "")) for h in headers))
    
    return f"Structure of table '{table_name}':\n" + "\n".join(rows)

if __name__ == "__main__":
    mcp.run()