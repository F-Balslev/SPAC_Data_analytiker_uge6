import pandas as pd

from utils.dataloader import FilePaths, load_all
from utils.order_processing import process_orders, process_restocks


def main():
    paths = FilePaths(
        base_path="data/",
        inventory="start_inventory.csv",
        orders="orders.csv",
        restocks="restocks.csv",
        products="products.csv",
    )

    inventory, orders, restocks, products = load_all(paths)

    start_date = orders["date"].iloc[0]
    end_date = orders["date"].iloc[-1]

    for current_date in pd.date_range(start_date, end_date, inclusive="both"):
        # Start by processing restocks for the day
        inventory = process_restocks(restocks, inventory, current_date)

        # Then process orders for the day
        inventory = process_orders(orders, inventory, current_date)

    breakpoint()


if __name__ == "__main__":
    main()
