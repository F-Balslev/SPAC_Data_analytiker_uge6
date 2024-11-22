import numpy as np
import pandas as pd

from experiments.frequency_multiplier import SimulateRestocksFrequencyMultiplier
from experiments.restocking_n_left_split import SimulateRestockWhenNLeftSplit
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

    """
    """
    simulation_n0 = SimulateRestockWhenNLeft(paths, min_inventory=0)
    simulation_n0.process_all()
    save_stuffs(simulation_n0, "n0")

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


    simulation_f_base = SimulateRestocBasedOnProductFrequency(
        paths,
        sample_until=pd.Timestamp("2012-01-01"),
        shpping_time=9,
        end_idx=-1,
    )
    simulation_f_base.process_all()
    save_stuffs(simulation_f_base, "f_base")



    simulation_f075 = SimulateRestocksFrequencyMultiplier(
        paths,
        sample_until=pd.Timestamp("2012-01-01"),
        shpping_time=9,
        end_idx=-1,
        restock_multiplier=0.75,
    )
    simulation_f075.process_all()
    save_stuffs(simulation_f075, "f075")

    simulation_f125 = SimulateRestocksFrequencyMultiplier(
        paths,
        sample_until=pd.Timestamp("2012-01-01"),
        shpping_time=9,
        end_idx=-1,
        restock_multiplier=1.25,
    )
    simulation_f125.process_all()
    save_stuffs(simulation_f125, "f125")

    simulation_f150 = SimulateRestocksFrequencyMultiplier(
        paths,
        sample_until=pd.Timestamp("2012-01-01"),
        shpping_time=9,
        end_idx=-1,
        restock_multiplier=1.5,
    )
    simulation_f150.process_all()
    save_stuffs(simulation_f150, "f150")

    simulation_f175 = SimulateRestocksFrequencyMultiplier(
        paths,
        sample_until=pd.Timestamp("2012-01-01"),
        shpping_time=9,
        end_idx=-1,
        restock_multiplier=1.75,
    )
    simulation_f175.process_all()
    save_stuffs(simulation_f175, "f175")

    simulation_f200 = SimulateRestocksFrequencyMultiplier(
        paths,
        sample_until=pd.Timestamp("2012-01-01"),
        shpping_time=9,
        end_idx=-1,
        restock_multiplier=2,
    )
    simulation_f200.process_all()
    save_stuffs(simulation_f200, "f200")

    """
    simulation_f050 = SimulateRestocksFrequencyMultiplier(
        paths,
        sample_until=pd.Timestamp("2012-01-01"),
        shpping_time=9,
        end_idx=-1,
        restock_multiplier=0.5,
    )
    simulation_f050.process_all()
    save_stuffs(simulation_f050, "f050")

    simulation_f750 = SimulateRestocksFrequencyMultiplier(
        paths,
        sample_until=pd.Timestamp("2012-01-01"),
        shpping_time=9,
        end_idx=-1,
        restock_multiplier=7.5,
    )
    simulation_f750.process_all()
    save_stuffs(simulation_f750, "f750")

    simulation_f1000 = SimulateRestocksFrequencyMultiplier(
        paths,
        sample_until=pd.Timestamp("2012-01-01"),
        shpping_time=9,
        end_idx=-1,
        restock_multiplier=10,
    )
    simulation_f1000.process_all()
    save_stuffs(simulation_f1000, "f1000")

    """
    simulation_ns0 = SimulateRestockWhenNLeftSplit(
        paths, min_inventory=0, sample_until=pd.Timestamp("2012-01-01")
    )
    simulation_ns0.process_all()
    save_stuffs(simulation_ns0, "ns0")

    simulation_ns1 = SimulateRestockWhenNLeftSplit(
        paths, min_inventory=1, sample_until=pd.Timestamp("2012-01-01")
    )
    simulation_ns1.process_all()
    save_stuffs(simulation_ns1, "ns1")

    simulation_ns2 = SimulateRestockWhenNLeftSplit(
        paths, min_inventory=2, sample_until=pd.Timestamp("2012-01-01")
    )
    simulation_ns2.process_all()
    save_stuffs(simulation_ns2, "ns2")

    simulation_ns3 = SimulateRestockWhenNLeftSplit(
        paths, min_inventory=3, sample_until=pd.Timestamp("2012-01-01")
    )
    simulation_ns3.process_all()
    save_stuffs(simulation_ns3, "ns3")

    simulation_ns4 = SimulateRestockWhenNLeftSplit(
        paths, min_inventory=4, sample_until=pd.Timestamp("2012-01-01")
    )
    simulation_ns4.process_all()
    save_stuffs(simulation_ns4, "ns4")

    simulation_ns5 = SimulateRestockWhenNLeftSplit(
        paths, min_inventory=5, sample_until=pd.Timestamp("2012-01-01")
    )
    simulation_ns5.process_all()
    save_stuffs(simulation_ns5, "ns5")

    simulation_ns6 = SimulateRestockWhenNLeftSplit(
        paths, min_inventory=6, sample_until=pd.Timestamp("2012-01-01")
    )
    simulation_ns6.process_all()
    save_stuffs(simulation_ns6, "ns6")

    simulation_ns7 = SimulateRestockWhenNLeftSplit(
        paths, min_inventory=7, sample_until=pd.Timestamp("2012-01-01")
    )
    simulation_ns7.process_all()
    save_stuffs(simulation_ns7, "ns7")

    simulation_ns8 = SimulateRestockWhenNLeftSplit(
        paths, min_inventory=8, sample_until=pd.Timestamp("2012-01-01")
    )
    simulation_ns8.process_all()
    save_stuffs(simulation_ns8, "ns8")

    simulation_ns9 = SimulateRestockWhenNLeftSplit(
        paths, min_inventory=9, sample_until=pd.Timestamp("2012-01-01")
    )
    simulation_ns9.process_all()
    save_stuffs(simulation_ns9, "ns9")

    """
    breakpoint()


if __name__ == "__main__":
    main()
