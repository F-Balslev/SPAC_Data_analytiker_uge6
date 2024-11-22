import pandas as pd

from experiments.restocking_product_frequency import (
    SimulateRestocBasedOnProductFrequency,
)
from utils.dataloader import FilePaths


class SimulateRestocksFrequencyMultiplier(SimulateRestocBasedOnProductFrequency):
    def __init__(
        self,
        filepaths: FilePaths,
        sample_until: pd.Timestamp,
        shpping_time: int = 9,
        end_idx: int = -1,
        restock_multiplier=1,
    ):
        # def __init__(self, inventory, num_workers):
        SimulateRestocBasedOnProductFrequency.__init__(
            self,
            filepaths,
            sample_until,
            shpping_time,
            end_idx,
        )
        self.restock_multiplier = restock_multiplier

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
                "amount": int(self.restock_limits[product] * self.restock_multiplier)
                + 1,
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
