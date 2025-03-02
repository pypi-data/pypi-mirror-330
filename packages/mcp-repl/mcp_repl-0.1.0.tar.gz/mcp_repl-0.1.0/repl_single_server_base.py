import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()
        self.chat_history = []
        self.tools = []
        self.available_tools = []

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server

        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()
        
        print("\nConnected to server with tools:", [tool.name for tool in response.tools])    
        self.tools = response.tools

        available_tools = [{
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
        } for tool in self.tools]
        self.available_tools = available_tools

    async def process_query(self, query: str) -> str:
        """Process a query using Claude and available tools"""
        # Add the new user message to chat history
        self.chat_history.append({
            "role": "user",
            "content": query
        })
        
        # Use the full chat history instead of just the current query
        messages = self.chat_history.copy()

        # Initial Claude API call
        response = self.anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            messages=messages,
            tools=self.available_tools,
            max_tokens=1000
        )

        # Process response and handle tool calls
        tool_results = []
        final_text = []

        assistant_message = {"role": "assistant", "content": []}
        for content in response.content:
            if content.type == 'text':
                final_text.append(content.text)
                assistant_message["content"].append(content)
            elif content.type == 'tool_use':
                tool_name = content.name
                tool_args = content.input

                # Execute tool call
                result = await self.session.call_tool(tool_name, tool_args)
                tool_results.append({"call": tool_name, "result": result})
                final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")

                assistant_message["content"].append(content)
                
        # Add assistant's message to chat history
        self.chat_history.append(assistant_message)
        
        # If there were tool calls, add tool results and get follow-up response
        if tool_results:
            # Add tool results to chat history
            tool_result_message = {
                "role": "user",
                "content": []
            }
            
            for i, result in enumerate(tool_results):
                tool_use_id = assistant_message["content"][i + 1].id if i + 1 < len(assistant_message["content"]) else None
                if tool_use_id:
                    tool_result_message["content"].append({
                        "type": "tool_result",
                        "tool_use_id": tool_use_id,
                        "content": result["result"].content
                    })
            
            self.chat_history.append(tool_result_message)
            
            # Update messages with the latest history
            messages = self.chat_history.copy()
            
            # Get next response from Claude
            follow_up_response = self.anthropic.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=messages,
                tools=self.available_tools
            )
            
            # Add follow-up response to chat history
            follow_up_message = {"role": "assistant", "content": []}
            for content in follow_up_response.content:
                final_text.append(content.text)
                follow_up_message["content"].append(content)
            
            self.chat_history.append(follow_up_message)

        return "\n".join(final_text)    

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == 'quit':
                    break

                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()
    
async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    import sys
    asyncio.run(main())        