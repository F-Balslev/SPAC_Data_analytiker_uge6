import numpy as np
import pandas as pd

from experiments.restocking_product_frequency import (
    SimulateRestocBasedOnProductFrequency,
)
from experiments.restocking_strategy_experiments import SimulateRestockWhenNLeft
from utils.dataloader import FilePaths
from utils.inventory_simulation import InventorySimulation


def save_stuffs(ting, name):
    np.save(f"debug_{name}.npy", ting.debug_total_inventory_over_time)
    ting.orders.to_pickle(f"orders_{name}")
    ting.restocks.to_pickle(f"restocks_{name}")


def main():
    paths = FilePaths(
        base_path="data/",
        inventory="start_inventory.csv",
        orders="orders.csv",
        restocks="restocks.csv",
        products="products.csv",
    )

    """
    original_simulation = InventorySimulation(paths)
    original_simulation.process_all()

    simulation_n = SimulateRestockWhenNLeft(paths, min_inventory=0)
    simulation_n.process_all()


    simulation_n1 = SimulateRestockWhenNLeft(paths, min_inventory=1)
    simulation_n1.process_all()
    save_stuffs(simulation_n1, "n1")

    simulation_n2 = SimulateRestockWhenNLeft(paths, min_inventory=2)
    simulation_n2.process_all()
    save_stuffs(simulation_n2, "n2")

    simulation_n3 = SimulateRestockWhenNLeft(paths, min_inventory=3)
    simulation_n3.process_all()
    save_stuffs(simulation_n3, "n3")

    simulation_n4 = SimulateRestockWhenNLeft(paths, min_inventory=4)
    simulation_n4.process_all()
    save_stuffs(simulation_n4, "n4")

    simulation_n5 = SimulateRestockWhenNLeft(paths, min_inventory=5)
    simulation_n5.process_all()
    save_stuffs(simulation_n5, "n5")

    simulation_n6 = SimulateRestockWhenNLeft(paths, min_inventory=6)
    simulation_n6.process_all()
    save_stuffs(simulation_n6, "n6")

    simulation_n7 = SimulateRestockWhenNLeft(paths, min_inventory=7)
    simulation_n7.process_all()
    save_stuffs(simulation_n7, "n7")

    simulation_n8 = SimulateRestockWhenNLeft(paths, min_inventory=8)
    simulation_n8.process_all()
    save_stuffs(simulation_n8, "n8")

    simulation_n9 = SimulateRestockWhenNLeft(paths, min_inventory=9)
    simulation_n9.process_all()
    save_stuffs(simulation_n9, "n9")
        filepaths: FilePaths,
        sample_until: pd.Timestamp,
        shpping_time: int = 9,
        end_idx: int = -1,
    """

    simulation_f = SimulateRestocBasedOnProductFrequency(
        paths,
        sample_until=pd.Timestamp("2012-01-01"),
        shpping_time=9,
        end_idx=-1,
    )
    simulation_f.process_all()
    save_stuffs(simulation_f, "f")

    breakpoint()


if __name__ == "__main__":
    main()
