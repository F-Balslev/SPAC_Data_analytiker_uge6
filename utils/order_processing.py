import pandas as pd


def process_single_restock(shipment, inventory: dict) -> dict:
    product, amount = shipment["product_id"], shipment["amount"]

    if product not in inventory:
        raise KeyError(f"Couldn't find {product} in inventory.")

    inventory[product] += amount
    inventory["total"] += amount

    return inventory


def process_restocks(
    restocks: pd.DataFrame, inventory: dict, date: pd.Timestamp
) -> dict:
    daily_restocks = restocks[restocks["delivery_date"] == date]

    for _, shipment in daily_restocks.iterrows():
        inventory = process_single_restock(shipment, inventory)

    return inventory


def process_single_order(order, inventory: dict) -> dict:
    products, status = order["products"], order["status"]

    if status != "Accepted":
        return inventory

    # Consider checking if valid product structure

    for product in products.split(", ")[:-1]:
        if product not in inventory:
            raise KeyError(f"Couldn't find {product} in inventory.")

        if inventory[product] < 1:
            raise ValueError(f"Product {product} was not in stock.")

        inventory[product] -= 1
        inventory["total"] -= 1

    return inventory


def process_orders(orders: pd.DataFrame, inventory: dict, date: pd.Timestamp) -> dict:
    daily_orders = orders[orders["date"] == date]

    for _, order in daily_orders.iterrows():
        inventory = process_single_order(order, inventory)

    return inventory
