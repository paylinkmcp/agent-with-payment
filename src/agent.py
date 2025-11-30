from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from paylink.integrations.langchain_tools import PayLinkTools

from src.tools.get_orders import get_orders


paylink_client = PayLinkTools()

payment_tools = paylink_client.list_tools()


tools = [get_orders] + payment_tools


agent = create_agent(
    model=init_chat_model(model="gpt-4o-mini"),
    tools=tools,

)