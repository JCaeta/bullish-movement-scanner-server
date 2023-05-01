from csv_utils.controller_csv import ControllerCSV

data_dir = "D:\\documents storage\\repositories\\Reusables\\financials_visualization_reusables\\Data\\"
path_ggal = data_dir + "GGAL.csv"

controller = ControllerCSV()
data = controller.get_investing_data(path_ggal)
data.to_csv(data_dir + "GGAL_norm.csv", index=False)
print(data)



