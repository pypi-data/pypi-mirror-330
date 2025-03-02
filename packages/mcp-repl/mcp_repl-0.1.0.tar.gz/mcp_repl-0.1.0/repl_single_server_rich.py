import asyncio
from typing import Optional, List, Dict, Any
from contextlib import AsyncExitStack
import sys
import json
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding import KeyBindings
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich.console import Group
from rich.syntax import Syntax
from rich.prompt import Confirm

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

# Define styles for the prompt
style = Style.from_dict({
    'prompt': 'ansicyan bold',
    'user-input': 'ansigreen',
})

# Create key bindings
kb = KeyBindings()

class LLMClient:
    """Handles interactions with the LLM and tools"""
    def __init__(self):
        self.anthropic = Anthropic()
        self.chat_history = []
        self.tools = []
        self.available_tools = []
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.stdio = None
        self.write = None

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
        self.tools = response.tools

        self.available_tools = [{
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
        } for tool in self.tools]
        
        return [tool.name for tool in response.tools]

    async def add_user_message(self, query: str):
        """Add a user message to the chat history"""
        self.chat_history.append({
            "role": "user",
            "content": query
        })
    
    async def get_llm_response(self):
        """Get a response from the LLM based on the current chat history"""
        system_prompt = """You are Claude, an AI assistant by Anthropic. You can help with a wide range of tasks including:
1. Writing and explaining code in various programming languages
2. Answering general knowledge questions
3. Providing creative content like stories or poems
4. Using the available tools when appropriate

When asked to write code or perform general tasks unrelated to the available tools, you should do so directly. Only use the provided tools when they are specifically relevant to the user's request."""

        response = self.anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            system=system_prompt,
            messages=self.chat_history,
            tools=self.available_tools,
            max_tokens=1000
        )
        
        return response
    
    async def call_tool(self, tool_name: str, tool_args: Dict[str, Any]):
        """Call a tool and return the result"""
        return await self.session.call_tool(tool_name, tool_args)
    
    async def add_assistant_message(self, content):
        """Add an assistant message to the chat history"""
        assistant_message = {"role": "assistant", "content": content}
        self.chat_history.append(assistant_message)
        return assistant_message
    
    async def add_tool_result(self, tool_use_id, result):
        """Add a tool result to the chat history"""
        tool_result_message = {
            "role": "user",
            "content": [{
                "type": "tool_result",
                "tool_use_id": tool_use_id,
                "content": result.content
            }]
        }
        self.chat_history.append(tool_result_message)
    
    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()


class RichUI:
    """Handles the Rich UI components and user interaction"""
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        self.console = Console()
    
    def print_welcome(self):
        """Print welcome message"""
        self.console.print("[bold blue]MCP Client Started![/bold blue]")
        self.console.print("Type your queries, [bold red]quit[/bold red] to exit, or press [bold red]q[/bold red] to exit directly.")
    
    def print_connected_tools(self, tool_names):
        """Print connected tools"""
        self.console.print("\nConnected to server with tools:", tool_names)
    
    def print_markdown(self, text):
        """Print markdown text"""
        self.console.print(Markdown(text))
    
    def print_tool_call(self, tool_name):
        """Print tool call information"""
        self.console.print(f"\n[Tool call: {tool_name}]\n")
    
    def confirm_tool_execution(self, tool_name, tool_args):
        """Ask for confirmation to execute a tool"""
        tool_args_str = str(tool_args)
        confirmation_text = Group(
            Text("🛠️  Tool Execution Request", style="bold white"),
            Text(""),
            Text("Tool: ", style="bold cyan") + Text(tool_name, style="bold yellow"),
            Text("Arguments: ", style="bold cyan") + Text(tool_args_str, style="italic"),
            Text(""),
            Text("Proceed with execution? (Y/n): ", style="bold green")
        )
        
        self.console.print(Panel(confirmation_text, border_style="yellow", title="Confirmation Required", subtitle="Press Enter to approve"))
        
        # Get user confirmation
        confirm = input()
        self.console.print()  # Add a blank line after input
        
        return confirm.lower() != 'n'
    
    def display_tool_result(self, tool_name, tool_args, result):
        """Display tool execution result"""
        # Extract the result text
        result_text = result.content
        formatted_result = ""
        
        if isinstance(result_text, list) and len(result_text) > 0:
            try:
                # Try to parse as JSON
                json_data = json.loads(result_text[0].text)
                formatted_result = json.dumps(json_data, indent=2)
            except (json.JSONDecodeError, AttributeError):
                # If not JSON, use the raw text
                if hasattr(result_text[0], 'text'):
                    formatted_result = result_text[0].text
                else:
                    formatted_result = str(result_text)
        else:
            formatted_result = str(result_text)
        
        header = Group(
            Text("🔧 Tool Call: ", style="bold cyan") + Text(tool_name, style="bold yellow"),
            Text("📥 Arguments: ", style="bold cyan") + Text(str(tool_args), style="italic"),
            Text("📤 Raw Result:", style="bold cyan"),
            Text("")  # Empty line for spacing
        )
        
        # Format the result content based on tool and content type
        if len(formatted_result) > 500:
            # For long outputs, truncate and offer to show full content
            preview_length = 500
            truncated = len(formatted_result) > preview_length
            preview = formatted_result[:preview_length] + ("..." if truncated else "")
            
            # Display truncated content in panel
            panel_content = Group(
                header,
                Text(preview)
            )
            
            if truncated:
                panel_content.renderables.append(Text("\n[Output truncated. Full length: " + 
                                                     str(len(formatted_result)) + " characters]", 
                                                     style="italic yellow"))
            
            self.console.print(Panel(panel_content, title="Tool Result", border_style="cyan"))
            
            # Offer to show full content
            if truncated:
                show_full = input("\nShow full output? (y/n): ")
                if show_full.lower() == 'y':
                    self.console.print("\nFull output:")
                    self.console.print(formatted_result)
        else:
            # For other results, just use the formatted text in a standard panel
            panel_content = Group(header, Text(formatted_result))
            self.console.print(Panel(panel_content, title="Tool Result", border_style="cyan"))
        
        self.console.print()
    
    def print_error(self, error):
        """Print error message"""
        self.console.print(f"\n[bold red]Error:[/bold red] {str(error)}")
        import traceback
        self.console.print(traceback.format_exc())
    
    def print_interrupted(self):
        """Print interrupted message"""
        self.console.print("\n[bold yellow]Interrupted. Type 'quit' to exit.[/bold yellow]")
    
    def print_tool_cancelled(self):
        """Print tool cancelled message"""
        self.console.print("[bold red]Tool call cancelled by user[/bold red]")


class MCPClient:
    """Main client that coordinates LLM and UI components"""
    def __init__(self):
        self.llm_client = LLMClient()
        self.ui = RichUI(self.llm_client)

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server"""
        tool_names = await self.llm_client.connect_to_server(server_script_path)
        self.ui.print_connected_tools(tool_names)

    async def process_query(self, query: str):
        """Process a query using Claude and available tools"""
        # Add the new user message to chat history
        await self.llm_client.add_user_message(query)
        
        # Show status indicator only for the initial API call
        with self.ui.console.status("[bold green]Processing query...[/bold green]"):
            response = await self.llm_client.get_llm_response()

        # Process response and handle tool calls
        tool_results = []
        assistant_content = []
        
        # Process and display the initial response
        for content in response.content:
            if content.type == 'text':
                self.ui.print_markdown(content.text)
                assistant_content.append(content)
            elif content.type == 'tool_use':
                tool_name = content.name
                tool_args = content.input

                # Print tool call information
                self.ui.print_tool_call(tool_name)
                
                # Get user confirmation
                if self.ui.confirm_tool_execution(tool_name, tool_args):
                    # Show status indicator for tool execution
                    with self.ui.console.status("[bold green]Executing tool...[/bold green]"):
                        # Execute tool call
                        result = await self.llm_client.call_tool(tool_name, tool_args)
                        tool_results.append({"call": tool_name, "result": result, "tool_use_id": content.id})
                    
                    # Display the tool result
                    self.ui.display_tool_result(tool_name, tool_args, result)
                    assistant_content.append(content)
                else:
                    self.ui.print_tool_cancelled()
        
        # Add assistant's message to chat history
        assistant_message = await self.llm_client.add_assistant_message(assistant_content)
        
        # If there were tool calls, add tool results and get follow-up response
        if tool_results:
            # Add tool results to chat history
            for result in tool_results:
                await self.llm_client.add_tool_result(result["tool_use_id"], result["result"])
            
            # Show status indicator for follow-up response
            with self.ui.console.status("[bold green]Getting follow-up response...[/bold green]"):
                # Get next response from Claude
                follow_up_response = await self.llm_client.get_llm_response()
            
            # Display follow-up response
            follow_up_content = []
            for content in follow_up_response.content:
                if content.type == 'text':
                    self.ui.print_markdown(content.text)
                follow_up_content.append(content)
            
            await self.llm_client.add_assistant_message(follow_up_content)

    async def chat_loop(self):
        """Run an interactive chat loop with improved UI"""
        self.ui.print_welcome()
        
        # Create prompt session with history
        session = PromptSession(
            history=FileHistory('.mcp_chat_history'),
            style=style,
            key_bindings=kb,
            multiline=True,
            prompt_continuation='... '
        )

        while True:
            try:
                # Display a fancy prompt
                query = await session.prompt_async(
                    HTML('<prompt>Query</prompt> <user-input>❯</user-input> '),
                    multiline=False
                )

                # Check for exit commands
                if query.lower() in ('quit', 'exit', 'q'):
                    break
                    
                # Skip empty queries
                if not query.strip():
                    continue

                # Process the query
                await self.process_query(query)
                
            except KeyboardInterrupt:
                self.ui.print_interrupted()
            except Exception as e:
                self.ui.print_error(e)

    async def cleanup(self):
        """Clean up resources"""
        await self.llm_client.cleanup()
    
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
    asyncio.run(main())        