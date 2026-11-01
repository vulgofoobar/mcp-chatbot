import os
import json
from anthropic import Anthropic
from anthropic.types import Message


class Claude:
    def __init__(self, model: str):
        api_endpoint = os.getenv("API_ENDPOINT")
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if api_endpoint:
            self.client = Anthropic(base_url=api_endpoint, api_key=api_key)
        else:
            self.client = Anthropic()
        self.model = model

    def add_user_message(self, messages: list, message):
        user_message = {
            "role": "user",
            "content": message.content
            if isinstance(message, Message)
            else message,
        }
        messages.append(user_message)

    def add_assistant_message(self, messages: list, message):
        assistant_message = {
            "role": "assistant",
            "content": message.content
            if isinstance(message, Message)
            else message,
        }
        messages.append(assistant_message)

    def text_from_message(self, message: Message):
        if message.content:
            texts = []
            for block in message.content:
                block_type = block.get('type') if isinstance(block, dict) else getattr(block, 'type', None)
                if block_type == "text":
                    text = block.get('text') if isinstance(block, dict) else getattr(block, 'text', None)
                    if text:
                        texts.append(text)
            if texts:
                return "\n".join(texts)
        
        if hasattr(message, 'choices') and message.choices:
            content = message.choices[0]['message']['content']
            return content if content else ""
        
        return ""

    def normalize_response(self, message: Message) -> Message:
        if message.content is not None:
            return message
        
        if hasattr(message, 'choices') and message.choices:
            choice = message.choices[0]['message']
            
            if 'tool_calls' in choice and choice['tool_calls']:
                content = []
                for tool_call in choice['tool_calls']:
                    args = tool_call['function'].get('arguments', '{}')
                    if isinstance(args, str):
                        args = json.loads(args)
                    content.append({
                        "type": "tool_use",
                        "id": tool_call['id'],
                        "name": tool_call['function']['name'],
                        "input": args,
                    })
                message.content = content
                message.stop_reason = "tool_use"
            elif choice.get('content'):
                message.content = [{
                    "type": "text",
                    "text": choice['content']
                }]
                message.stop_reason = "end_turn"
        
        return message

    def chat(
        self,
        messages,
        system=None,
        temperature=1.0,
        stop_sequences=[],
        tools=None,
        thinking=False,
        thinking_budget=1024,
    ) -> Message:
        params = {
            "model": self.model,
            "max_tokens": 8000,
            "messages": messages,
        }

        if temperature != 1.0:
            params["temperature"] = temperature

        if stop_sequences:
            params["stop_sequences"] = stop_sequences

        if thinking:
            params["thinking"] = {
                "type": "enabled",
                "budget_tokens": thinking_budget,
            }

        if tools:
            params["tools"] = tools

        if system:
            params["system"] = system

        message = self.client.messages.create(**params)
        return self.normalize_response(message)
