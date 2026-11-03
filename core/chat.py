from core.claude import Claude
from mcp_client import MCPClient
from core.tools import ToolManager
from anthropic.types import MessageParam


class Chat:
    def __init__(self, claude_service: Claude, clients: dict[str, MCPClient]):
        self.claude_service: Claude = claude_service
        self.clients: dict[str, MCPClient] = clients
        self.messages: list[MessageParam] = []

    async def _process_query(self, query: str):
        self.messages.append({"role": "user", "content": query})

    async def run(
        self,
        query: str,
    ) -> str:
        final_text_response = ""

        await self._process_query(query)

        system_prompt = "You are a helpful assistant with access to tools for reading and editing documents. Use the available tools to answer questions about document contents. When a user asks about a document, use the read_doc tool to fetch its contents."

        while True:
            response = self.claude_service.chat(
                messages=self.messages,
                tools=await ToolManager.get_all_tools(self.clients),
                system=system_prompt,
            )

            self.claude_service.add_assistant_message(self.messages, response)

            if response.stop_reason == "tool_use":
                print(self.claude_service.text_from_message(response))
                tool_result_parts = await ToolManager.execute_tool_requests(
                    self.clients, response
                )

                self.messages.append({
                    "role": "user",
                    "content": tool_result_parts,
                })
            else:
                final_text_response = self.claude_service.text_from_message(
                    response
                )
                break

        return final_text_response
