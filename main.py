import numpy as np
import pandas as pd
import tqdm

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

    # Total inventory at the end of each day (eod)
    eod_total_inventory = np.zeros((end_date - start_date).days + 1)

    for current_date in tqdm.tqdm(pd.date_range(start_date, end_date)):
        # Start by processing restocks for the day
        inventory = process_restocks(restocks, inventory, current_date)

        # Then process orders for the day
        inventory = process_orders(orders, inventory, current_date)

        # Update the end of day inventory
        current_date_index = (start_date - current_date).days
        eod_total_inventory[current_date_index] = inventory["total"]

    breakpoint()


if __name__ == "__main__":
    main()
