from experiments.restocking_strategy_experiments import SimulateRestockWhenNLeft
from utils.dataloader import FilePaths
from utils.inventory_simulation import InventorySimulation


def main():
    paths = FilePaths(
        base_path="data/",
        inventory="start_inventory.csv",
        orders="orders.csv",
        restocks="restocks.csv",
        products="products.csv",
    )
    # simulation = InventorySimulation(paths)
    simulation = SimulateRestockWhenNLeft(paths, min_inventory=5, end_idx=25000)

    simulation.process_all()

    breakpoint()


if __name__ == "__main__":
    main()
