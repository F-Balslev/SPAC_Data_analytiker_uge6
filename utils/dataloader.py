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


class DataLoader:
    def __init__(self, paths: FilePaths) -> None:
        self.paths = paths

    def load_inventory_to_dict(self) -> dict:
        inventory = {}

        with open(self.paths.inventory_path()) as file:
            reader = csv.DictReader(file)

            for row in reader:
                inventory[row["product_id"]] = int(row["quantity"])

        inventory["total"] = sum(inventory.values())

        return inventory

    def load_dataframe(self) -> pd.DataFrame:
        return pd.read_csv(self.paths.products_path())

    def load_restocks(self) -> pd.DataFrame:
        return pd.read_csv(
            self.paths.restocks_path(), parse_dates=["order_date", "delivery_date"]
        )

    def load_orders(self) -> pd.DataFrame:
        return pd.read_csv(self.paths.orders_path(), parse_dates=["date"])
