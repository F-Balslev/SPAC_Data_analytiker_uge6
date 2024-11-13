from utils.dataloader import FilePaths
from utils.order_processing import OrderProcessing


def main():
    paths = FilePaths(
        base_path="data/",
        inventory="start_inventory.csv",
        orders="orders.csv",
        restocks="restocks.csv",
        products="products.csv",
    )
    process = OrderProcessing(paths)

    process.process_all()

    breakpoint()


if __name__ == "__main__":
    main()
