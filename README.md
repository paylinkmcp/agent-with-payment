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

Before getting started, ensure you have:

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager (recommended)
- OpenAI API key
- A PayLink account — [Create one here](https://paylink-platform.vercel.app/)

For detailed prerequisites, see the [PayLink Prerequisites Guide](https://docs.paylink.dev/agent-to-human/prerequisites).

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

3. **Install the PayLink SDK:**

   ```bash
   pip install paylink
   ```

   For more installation options, see the [Install Guide](https://docs.paylink.dev/get-started/install).

4. **Set up environment variables:**

   Create a `.env` file in the project root:

   ```env
   OPENAI_API_KEY=your_openai_api_key
   PAYLINK_API_KEY=your_paylink_api_key
   ```

   Learn how to get your API key in the [API Key documentation](https://docs.paylink.dev/resources/api-key).

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

## Quick Start

### 1. Build the Agent

This example follows the [Build Agent](https://docs.paylink.dev/agent-to-human/build-agent) guide. The agent is configured in `src/agent.py`:

```python
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from paylink.integrations.langchain_tools import PayLinkTools

# Initialize PayLink tools
paylink_client = PayLinkTools()
payment_tools = paylink_client.list_tools()

# Combine with custom tools
tools = [get_orders] + payment_tools

# Create the agent
agent = create_agent(
    model=init_chat_model(model="gpt-4o-mini"),
    tools=tools,
)
```

### 2. Run the Agent

**Using LangGraph CLI:**

```bash
langgraph dev
```

**Using LangGraph Studio:**

```bash
langgraph studio
```

### 3. Test Payments

Before processing real payments, test your integration using the [Test Payment Provider](https://docs.paylink.dev/agent-to-human/test-payment-provider).

## Agent to Human Flow

This example implements the **Agent to Human** payment pattern, where AI agents request payments that humans approve. The complete flow includes:

1. **[Prerequisites](https://docs.paylink.dev/agent-to-human/prerequisites)** — Set up your environment
2. **[Test Payment Provider](https://docs.paylink.dev/agent-to-human/test-payment-provider)** — Validate your integration
3. **[Build Agent](https://docs.paylink.dev/agent-to-human/build-agent)** — Create your AI agent (this example)
4. **[Human in the Loop](https://docs.paylink.dev/agent-to-human/human-in-the-loop)** — Add approval workflows
5. **[Handle Webhooks](https://docs.paylink.dev/agent-to-human/handle-webhooks)** — Process payment callbacks
6. **[Full Integration](https://docs.paylink.dev/agent-to-human/setup)** — Complete setup guide

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
- Initiating payments (M-Pesa, Card, etc.)
- Checking payment status
- Processing refunds

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

### Customizing PayLink

```python
from paylink.integrations.langchain_tools import PayLinkTools

paylink_client = PayLinkTools(
    api_key="your_api_key",              # Your PayLink API key
    tracing="your_project_id",           # Enable tracing (optional)
    payment_provider=["mpesa", "card"],  # Filter available providers
)
```

Learn more about [Tracing](https://docs.paylink.dev/resources/tracing) and [Projects](https://docs.paylink.dev/resources/project).

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

## Resources

### PayLink Documentation
- [About PayLink](https://docs.paylink.dev/overview/about)
- [Install Guide](https://docs.paylink.dev/get-started/install)
- [Create an Account](https://docs.paylink.dev/get-started/create-an-account)
- [API Key](https://docs.paylink.dev/resources/api-key)
- [Wallet](https://docs.paylink.dev/resources/wallet)
- [PayLink Agent](https://docs.paylink.dev/resources/agent)

### Community
- [Website](https://paylink-platform.vercel.app/)
- [Discord](https://discord.gg/bhs62pADCe)
- [GitHub](https://github.com/paylinkmcp/paylink)
- [Support](mailto:paylinkmcp@gmail.com)

### Framework Documentation
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://python.langchain.com/)

## License

MIT
