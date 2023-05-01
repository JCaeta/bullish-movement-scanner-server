# from csv_utils.controller_csv import ControllerCSV
# from backtesting_utils.backtesting_utils import Backtest
# import pandas as pd
# from strategies.strategies1 import Strategy1, StrategyMovementTracker
# from charts.tradingview_utils import create_rect

# path_btc_usd = "D:\\documents storage\\repositories\\sandboxes\\financials\\data\\BTC_USD.csv"
# path_eur_usd = "D:\\documents storage\\repositories\\sandboxes\\financials\\data\\EURUSD_M5_2021-10-27_2023-02-27.csv"
# path_eur_usd_small = "D:\\documents storage\\repositories\\sandboxes\\financials\\data\\EURUSD_M5_2021-10-27_2023-02-27 - Small.csv"

# controller_csv = ControllerCSV()
# eur_usd_data = controller_csv.get_metatrader_data(path_eur_usd)

# strategy = StrategyMovementTracker()
# backtest = Backtest(eur_usd_data, strategy)
# backtest.run()

# ----------------------------------------------------------------------------------------------------------
import pandas as pd
data_dir = "D:\\documents storage\\repositories\\Reusables\\financials_visualization_reusables\\Data\\"
path_ggal = data_dir + "GGAL.csv"
data = pd.read_csv(path_ggal)
print(data) 