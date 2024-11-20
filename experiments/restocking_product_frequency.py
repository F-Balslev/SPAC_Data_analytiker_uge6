from collections import defaultdict

import numpy as np
import pandas as pd
import tqdm

from utils.dataloader import FilePaths
from utils.inventory_simulation import InventorySimulation

#
#
# order quantity: int(resstock_limit) + 1
#
#


class SimulateRestocBasedOnProductFrequency(InventorySimulation):
    """
    Triggers a restock for each product when
        items in inventory is less than 'products_sold_per_day' * 'shipping_time'


    """

    def __init__(
        self,
        filepaths: FilePaths,
        sample_until: pd.Timestamp,
        shpping_time: int = 9,
        end_idx: int = -1,
    ):
        # def __init__(self, inventory, num_workers):
        InventorySimulation.__init__(self, filepaths)
        self.end_date: pd.Timestamp = self.orders.iloc[end_idx]["date"]
        self.shipping_time = shpping_time
        self.start_date = sample_until

        # Consider getting rid of this and only use start_date
        self.sample_until = sample_until

        # Split orders into a sampling dataframe and a dataframe for evaluation
        self.samples, self.orders = self.sampling_split()

        # Get limits for when to restock based on the sampling data
        self.restock_limits = self.get_restock_limit()

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

    def get_restock_limit(self):
        """
        Calculates average number of products ordered in the time it takes for more products to be restsocked
        """
        product_count = defaultdict(lambda: 0)

        print("Pre-processing")
        for _, order in tqdm.tqdm(self.samples.iterrows()):
            products = order["products"].split(", ")[:-1]

            for product in products:
                product_count[product] += 1

        start_time: pd.Timestamp = self.samples.iloc[0]["date"]
        end_date: pd.Timestamp = self.samples.iloc[-1]["date"]

        n_days = (end_date - start_time).days

        for key in product_count.keys():
            product_count[key] *= self.shipping_time / n_days

        return product_count

    def process_single_restock(self, shipment: pd.DataFrame):
        product = shipment["product_id"]
        amount = int(self.restock_limits[product]) + 1

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
            if stock <= self.restock_limits[product]
            and not self.pending_restock[product]
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
