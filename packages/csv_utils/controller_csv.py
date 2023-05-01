from .adapters import CsvMetatraderAdapter, CsvInvestingAdapter

class ControllerCSV:
    def get_metatrader_data(self, path):
        data_adapter = CsvMetatraderAdapter()
        data_adapter.set_path(path)
        data_adapter.read_data()
        return data_adapter.get_data_base_format()
    
    def get_investing_data(self, path):
        data_adapter = CsvInvestingAdapter()
        data_adapter.set_path(path)
        data_adapter.read_data()
        return data_adapter.get_data_base_format()