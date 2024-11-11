import pandas as pd


def process_restocks(restocks: pd.DataFrame, inventory: dict, date: str) -> dict:
    daily_restocks = restocks[restocks["delivery_date"] == date]

    for _, row in daily_restocks.iterrows():
        product, amount = row["product_id"], row["amount"]

        if product not in inventory:
            raise KeyError(f"Couldn't find {product} in inventory on {date}.")

        inventory[product] += amount

    return inventory


def process_orders(orders: pd.DataFrame, inventory: dict, date: str) -> dict:
    daily_orders = orders[orders["date"] == date]

    for _, order in daily_orders.iterrows():
        products, status = order["products"], order["status"]

        if status != "Accepted":
            continue

        # Consider checking if valid product structure

        for product in products.split(", ")[:-1]:
            if product not in inventory:
                raise KeyError(f"Couldn't find {product} in inventory on {date}.")

            if inventory[product] < 1:
                raise ValueError(f"Product {product} was not in stock on {date}")

            inventory[product] -= 1

    return inventory
