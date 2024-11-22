from collections import defaultdict

import numpy as np
import pandas as pd

from utils.dataloader import FilePaths
from utils.inventory_simulation import InventorySimulation


class SimulateRestockWhenNLeftSplit(InventorySimulation):
    """
    Triggers a restock when 'min_inventory' items in inventory instead of 0
    split dataset
    """

    def __init__(
        self,
        filepaths: FilePaths,
        min_inventory: int,
        sample_until: pd.Timestamp,
        end_idx: int = -1,
    ):
        # def __init__(self, inventory, num_workers):
        InventorySimulation.__init__(self, filepaths)
        self.min_inventory: int = min_inventory
        self.end_date: pd.Timestamp = self.orders.iloc[end_idx]["date"]

        self.start_date = sample_until
        self.sample_until = sample_until

        _, self.orders = self.sampling_split()

        # Manually set status
        self.orders["status"] = "Unknown"

        # Create empty restocks from old restocks
        self.restocks = pd.DataFrame(columns=self.restocks.columns)

        # Create dict for products that have been ordered for restocking but not yet arrived
        self.pending_restock = defaultdict(lambda: False)

        self.debug_total_inventory_over_time = np.zeros(
            (self.end_date - self.start_date).days + 1
        )

    def sampling_split(self):
        first_indexs = self.orders["date"] < self.sample_until

        return self.orders[first_indexs].copy(), self.orders[~first_indexs].copy()

    def process_single_restock(self, shipment: pd.DataFrame):
        product, amount = shipment["product_id"], shipment["amount"]

        if product not in self.inventory:
            raise KeyError(f"Couldn't find {product} in inventory.")

        # Add to inventory
        self.inventory[product] += amount
        self.inventory["total"] += amount

        # Remove from pending restocks
        self.pending_restock[product] = False

    def process_single_order(self, order: pd.DataFrame, index):
        products = order["products"].split(", ")[:-1]

        # Check if the order is valid
        for product in products:
            if product not in self.inventory:
                raise KeyError(f"Couldn't find {product} in inventory.")

            if self.inventory[product] < 1:
                # Product was not in stock, reject order
                self.orders.loc[index, "status"] = "Rejected"
                return

        # Accept the order and update inventory
        self.orders.loc[index, "status"] = "Accepted"

        for product in products:
            self.inventory[product] -= 1
            self.inventory["total"] -= 1

    def process_daily_orders(self, date: pd.Timestamp):
        daily_orders = self.orders[self.orders["date"] == date]

        for index, order in daily_orders.iterrows():
            self.process_single_order(order, index)

    def get_supplier(self, product_id):
        # This is suuuuper slow :(
        return self.products.loc[self.products["id"] == product_id, "brand"].item()

    def generate_delivery_date(self, date):
        return date + pd.Timedelta(9, "days")

    def add_new_restocks(self, date):
        # Get all products that need to be restocked
        products_to_restock = [
            product
            for product, stock in self.inventory.items()
            if stock <= self.min_inventory and not self.pending_restock[product]
        ]

        # Add to pending restocks
        for product in products_to_restock:
            self.pending_restock[product] = True

        # Store in dataframe
        restock_data = [
            {
                "order_date": date,
                "delivery_date": self.generate_delivery_date(date),
                "product_id": product,
                "amount": 10,
                "supplier": None,  # self.get_supplier(product),
            }
            for product in products_to_restock
        ]

        restock_data_df = pd.DataFrame(restock_data, columns=self.restocks.columns)

        if self.restocks.empty:
            self.restocks = restock_data_df
        else:
            self.restocks = pd.concat(
                [self.restocks, restock_data_df],
                ignore_index=True,
            )

    def process_day(self, date: pd.Timestamp):
        self.process_daily_restocks(date)
        self.process_daily_orders(date)
        self.add_new_restocks(date)
        self.debug_total_inventory_over_time[(date - self.start_date).days] = (
            self.inventory["total"]
        )
