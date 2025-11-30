# Agent with Payment

An AI-powered agent built with LangGraph that integrates PayLink payment tools, enabling conversational payment processing and order management.

## Overview

This example demonstrates how to build an intelligent agent that can:

- **Query orders** — Retrieve orders from a database, filtered by payment status (paid, pending, failed)
- **Process payments** — Leverage PayLink's payment infrastructure through natural language

The agent combines custom business logic tools with PayLink's payment capabilities, creating a seamless conversational interface for payment operations.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    LangGraph Agent                  │
│                    (GPT-4o-mini)                    │
├─────────────────────────────────────────────────────┤
│                       Tools                         │
│  ┌─────────────────┐    ┌─────────────────────────┐ │
│  │   get_orders    │    │    PayLink Tools        │ │
│  │  (Custom Tool)  │    │  (Payment Processing)   │ │
│  └─────────────────┘    └─────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager (recommended)
- OpenAI API key
- PayLink API key (optional, for production use)

## Installation

1. **Clone the repository and navigate to this example:**

   ```bash
   cd examples/agent_with_payment
   ```

2. **Install dependencies using uv:**

   ```bash
   uv sync
   ```

   Or with pip:

   ```bash
   pip install -e .
   ```

3. **Set up environment variables:**

   Create a `.env` file in the project root:

   ```env
   OPENAI_API_KEY=your_openai_api_key
   PAYLINK_API_KEY=your_paylink_api_key  # Optional
   ```

## Project Structure

```
agent_with_payment/
├── src/
│   ├── agent.py           # Main agent configuration
│   └── tools/
│       └── get_orders.py  # Custom order retrieval tool
├── langgraph.json         # LangGraph deployment config
├── pyproject.toml         # Project dependencies
└── README.md
```

## Usage

### Running with LangGraph CLI

Start the agent server locally:

```bash
langgraph dev
```

This launches an interactive development server where you can test the agent.

### Running in LangGraph Studio

Open the project in [LangGraph Studio](https://github.com/langchain-ai/langgraph-studio) for a visual interface:

```bash
langgraph studio
```

## Tools

### `get_orders`

Retrieves orders from the database with optional filtering by payment status.

**Parameters:**
- `payment_status` (optional): Filter orders by status — `"paid"`, `"pending"`, or `"failed"`

**Returns:** List of orders containing:
- `name`: Order item name
- `price`: Price amount
- `currency`: Currency code (e.g., "Ksh")
- `quantity`: Item quantity
- `payment_status`: Current payment status

**Example Usage (via agent):**
> "Show me all pending orders"
> "What orders have been paid?"

### PayLink Tools

The agent automatically loads all available payment tools from PayLink, enabling operations like:
- Initiating payments
- Checking payment status
- Processing refunds
- And more...

## Configuration

### LangGraph Configuration (`langgraph.json`)

```json
{
  "graphs": {
    "agent_with_payment": "src/agent.py:agent"
  },
  "dependencies": ["."],
  "env": "./.env",
  "python_version": "3.13"
}
```

### Customizing the Agent

Modify `src/agent.py` to:
- Change the LLM model
- Add custom tools
- Configure PayLink options

```python
from paylink.integrations.langchain_tools import PayLinkTools

# Initialize with custom configuration
paylink_client = PayLinkTools(
    api_key="your_api_key",           # Optional API key
    payment_provider=["mpesa", "card"] # Filter available providers
)
```

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| langchain | ≥1.1.0 | Agent framework |
| langchain-openai | ≥1.1.0 | OpenAI integration |
| langgraph | ≥1.0.4 | Graph-based agent orchestration |
| langgraph-cli | ≥0.4.7 | CLI tools & development server |
| paylink | ≥0.4.2 | Payment processing integration |

## Example Conversations

**Querying Orders:**
```
User: What orders do I have?
Agent: You have 2 orders:
       1. Item 1 - Ksh 100 (paid)
       2. Item 2 - Ksh 200 x2 (pending)

User: Show me only the pending ones
Agent: Here's your pending order:
       - Item 2 - Ksh 200 x2 (pending)
```

**Processing Payments:**
```
User: I want to pay for Item 2
Agent: I'll help you process the payment for Item 2 (Ksh 400 total).
       [Initiates PayLink payment flow]
```

## Development

### Adding Custom Tools

Create new tools in `src/tools/`:

```python
from langchain.tools import tool

@tool("my_custom_tool", description="Description of what this tool does")
def my_custom_tool(param: str) -> dict:
    """Implementation details."""
    return {"result": "success"}
```

Then register it in `src/agent.py`:

```python
from src.tools.my_tool import my_custom_tool

tools = [get_orders, my_custom_tool] + payment_tools
```

## License

MIT

## Links

- [PayLink Documentation](https://paylink.dev)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://python.langchain.com/)

