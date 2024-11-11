import csv
from dataclasses import dataclass

import pandas as pd


@dataclass
class FilePaths:
    base_path: str
    inventory: str
    orders: str
    restocks: str
    products: str

    def inventory_path(self) -> str:
        return f"{self.base_path}{self.inventory}"

    def orders_path(self) -> str:
        return f"{self.base_path}{self.orders}"

    def restocks_path(self) -> str:
        return f"{self.base_path}{self.restocks}"

    def products_path(self) -> str:
        return f"{self.base_path}{self.products}"


def load_inventory_to_dict(filepath: str) -> dict:
    inventory = {}

    with open(filepath) as file:
        reader = csv.DictReader(file)

        for row in reader:
            inventory[row["product_id"]] = int(row["quantity"])

    return inventory


def load_dataframe(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath)


def load_restocks(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath, parse_dates=["order_date", "delivery_date"])


def load_orders(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath, parse_dates=["date"])


def load_all(filepaths: FilePaths):
    inventory = load_inventory_to_dict(filepaths.inventory_path)
    orders = load_orders(filepaths.orders_path)
    restocks = load_restocks(filepaths.restocks_path)
    products = load_dataframe(filepaths.products_path)

    return inventory, orders, restocks, products
