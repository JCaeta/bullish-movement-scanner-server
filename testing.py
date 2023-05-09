import unittest
from globals import LOMA_PATH, GGAL_PATH
from packages.csv_utils.adapters import CsvInvestingAdapter
import pandas as pd
from controller import ChartsController
from packages.strategies.strategies3 import StrategyMovementTracker
from packages.backtesting_utils.backtesting_utils import Backtest

class TestController(unittest.TestCase):
    
    # @unittest.skip("demonstrating skipping")
    @classmethod
    def setUpClass(cls) -> None:
        # It executes before all the test methods
        print("setUpClass call")

    # @unittest.skip("demonstrating skipping")
    def test_setup_normal_distribution(self):
        # 1) Adapt data file
        adapter = CsvInvestingAdapter()
        # adapter.set_path(GGAL_PATH)
        adapter.set_path(LOMA_PATH)
        adapter.read_data()
        adapter.convert_to_base_format()
        data = adapter.get_data_base_format()

        # 2) Make backtesting
        backtest = None
        strategy = StrategyMovementTracker()
        strategy.short_percentage = 0.05
        backtest = Backtest(data, strategy)
        backtest.run()

        # 3) Use controller
        controller = ChartsController()
        normal_distribution = controller.setup_normal_distribution(strategy.movements)
        print(normal_distribution)


    # @unittest.skip("demonstrating skipping")
    @classmethod
    def tearDownClass(cls) -> None:
        # It executes before all the test methods
        print("tearDown call")

if __name__ == '__main__':
    unittest.main()
