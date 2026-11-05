# MCP Chatbot

MCP Chat is a command-line interface application that enables interactive chat capabilities with AI models through the Anthropic API. The application supports document retrieval, command-based prompts, and extensible tool integrations via the MCP (Model Control Protocol) architecture.

## Prerequisites

- Python 3.9+
- Anthropic API Key

## Setup

### Step 1: Configure the environment variables

1. Create or edit the `.env` file in the project root and verify that the following variables are set correctly:

```
ANTHROPIC_API_KEY=""  # Enter your Anthropic API secret key
```

**Optional: Use external AI models**

To use an external AI model provider, add these variables:

```
API_ENDPOINT=""       # Base URL of your external AI model endpoint (e.g., http://localhost:8000/v1)
CLAUDE_MODEL=""       # Model identifier to use (e.g., claude-3-5-sonnet, local-model)
```

If these are not set, the application will use the Anthropic API with your `ANTHROPIC_API_KEY`.

### Step 2: Install dependencies

#### Option 1: Setup with uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

1. Install uv, if not already installed:

```bash
pip install uv
```

2. Create and activate a virtual environment:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
uv pip install -e .
```

4. Run the project

```bash
uv run main.py
```

#### Option 2: Setup without uv

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install anthropic python-dotenv prompt-toolkit "mcp[cli]==1.8.0"
```

3. Run the project

```bash
python main.py
```

## Usage

### Basic Interaction

Simply type your message and press Enter to chat with the model.

### Document Retrieval

Use the @ symbol followed by a document ID to include document content in your query:

```
> Tell me about @deposition.md
```

### Commands

Use the / prefix to execute commands defined in the MCP server:

```
> /summarize deposition.md
> /format spec.txt
```

Commands will auto-complete when you press Tab.

## Development

### MCP Development Inspector

Test and debug the MCP server using the browser-based inspector:

```bash
mcp dev mcp_server.py
```

This launches an interactive development server. Open your browser to `http://127.0.0.1:6274/` to:
- Quickly iterate on tool implementations
- Test edge cases and error conditions
- Verify tool interactions and state management
- Debug issues in real-time

### Adding New Documents

Edit the `mcp_server.py` file to add new documents to the `docs` dictionary.

### Implementing MCP Features

To fully implement the MCP features:

1. Complete the TODOs in `mcp_server.py`
2. Implement the missing functionality in `mcp_client.py`

### Linting and Typing Check

There are no lint or type checks implemented.

## Tangent discoveries

see [what's mcp and what it stands for?](./docs/whats-mcp-and-what-it-stands-for.md)

see [why does mcp matters?](./docs/why-does-mcp-matters.md)

see [what problem mcp solves?](./docs/what-problem-mcp-solves.md)

see [what's mcp server?](./docs/whats-mcp-server.md)

see [how mcp client and mcp server communicates? what's the most common?](./docs/how-mcp-client-and-mcp-server-communicates.md)

see [what's python mcp sdk?](./docs/whats-python-mcp-sdk.md)

see [what python mcp sdk does?](./docs/what-python-mcp-sdk-does.md)

see [how does python mcp sdk make it easy to expose tools to claude?](./docs/how-does-python-mcp-sdk-make-it-easy.md)

see [what's the code to create an mcp server w mcp sdk?](./docs/code-to-create-mcp-server.md)

see [what's the code to define a tool w mcp sdk?](./docs/code-to-define-tool.md)

see [what's the key benefits of the mcp server sdk?](./docs/key-benefits-mcp-server-sdk.md)

see [what's a mcp client session? where it belongs?](./docs/what-is-mcp-client-session.md)

see [what's a mcp client?](./docs/what-is-mcp-client.md)

see [what are resources in mcp?](./docs/what-are-resources-in-mcp.md)

see [what's the purpose of mime_type in mcp responses? give two examples](./docs/mime-type-purpose.md)

see [what's the diff between binary and text files?](./docs/binary-vs-text-files.md)

see [what's the diff between resources and tools?](./docs/resources-vs-tools.md)

see [what's mcp server prompts?](./docs/what-are-mcp-server-prompts.md)

see [why mcp server prompts?](./docs/why-mcp-server-prompts.md)

see [what are mcp server prompt key benefits?](./docs/mcp-server-prompt-benefits.md)

see [what are mcp server primitives?](./docs/mcp-server-primitives.md)

## Reference

- [introduction to model context protocol](https://anthropic.skilljar.com/introduction-to-model-context-protocol)
