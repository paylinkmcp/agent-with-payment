from langchain.tools import tool
from typing import Literal


TOOL_DESCRIPTION = """
This tool returns orders from the database

Args:
- payment_status: The payment status of the orders. Can be "paid", "pending", or "failed". If not provided, all orders are returned.

Returns:
- A list of orders with the following fields:
    - name: The name of the order
    - price: The price of the order
    - quantity: The quantity of the order
    - payment_status: The payment status of the order

"""


@tool("get_orders", description=TOOL_DESCRIPTION)
def get_orders(
    payment_status: Literal["paid", "pending", "failed"] | None = None,
) -> list[dict]:
    """Return orders in the cart, optionally filtered by payment status."""

    orders = [
        {
            "name": "Item 1",
            "price": 100,
            "currency": "Ksh",
            "quantity": 1,
            "payment_status": "paid",
        },
        {
            "name": "Item 2",
            "price": 200,
            "currency": "Ksh",
            "quantity": 2,
            "payment_status": "pending",
        },
    ]

    if payment_status is None:
        return orders

    normalized_status = payment_status.lower()
    return [
        item for item in orders if item["payment_status"].lower() == normalized_status
    ]
