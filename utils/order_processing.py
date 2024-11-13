import pandas as pd
import tqdm

from utils.dataloader import DataLoader, FilePaths


class OrderProcessing:
    def __init__(self, filepaths: FilePaths):
        self.filepaths: FilePaths = filepaths
        self.dataloader: DataLoader = DataLoader(self.filepaths)
        self.inventory: dict
        self.orders: pd.DataFrame
        self.restocks: pd.DataFrame
        self.products: pd.DataFrame

        self.load_csv()

        self.start_date: pd.Timestamp = self.orders["date"].iloc[0]
        self.end_date: pd.Timestamp = self.orders["date"].iloc[-1]

    def load_csv(self):
        self.inventory = self.dataloader.load_inventory_to_dict()
        self.orders = self.dataloader.load_orders()
        self.restocks = self.dataloader.load_restocks()
        self.products = self.dataloader.load_dataframe()

    def process_single_restock(self, shipment: pd.DataFrame):
        product, amount = shipment["product_id"], shipment["amount"]

        if product not in self.inventory:
            raise KeyError(f"Couldn't find {product} in inventory.")

        self.inventory[product] += amount
        self.inventory["total"] += amount

    def process_daily_restocks(self, date: pd.Timestamp):
        daily_restocks = self.restocks[self.restocks["delivery_date"] == date]

        for _, shipment in daily_restocks.iterrows():
            self.process_single_restock(shipment)

    def process_single_order(self, order: pd.DataFrame):
        products, status = order["products"], order["status"]

        if status != "Accepted":
            return

        # Consider checking if valid product structure

        for product in products.split(", ")[:-1]:
            if product not in self.inventory:
                raise KeyError(f"Couldn't find {product} in inventory.")

            if self.inventory[product] < 1:
                raise ValueError(f"Product {product} was not in stock.")

            self.inventory[product] -= 1
            self.inventory["total"] -= 1

    def process_daily_orders(self, date: pd.Timestamp):
        daily_orders = self.orders[self.orders["date"] == date]

        for _, order in daily_orders.iterrows():
            self.process_single_order(order)

    def process_day(self, date: pd.Timestamp):
        self.process_daily_restocks(date)
        self.process_daily_orders(date)

    def process_all(self):
        for date in tqdm.tqdm(pd.date_range(self.start_date, self.end_date)):
            self.process_day(date)

    def get_inventory(self) -> dict:
        return self.inventory
