import abc
import pandas as pd
from ..pandas_utils.pandas_utils import PandasFormatter
import datetime as dt

class JsonInvestingAdapter():
    __data = None
    __data_base_format = None

    def set_data(self, data):
        self.__data = data

    def convert_to_base_format(self):
        # 0) Instanciate elements
        formatter = PandasFormatter()

        # 1) Get the columns we need
        self.__data_base_format = self.__data[['Date', 'Price', 'Open', 'High', 'Low']]

        # 2) Rename columns
        self.__data_base_format = self.__data_base_format[['Date', 'Price', 'Open', 'High', 'Low']]
        self.__data_base_format = self.__data_base_format.rename(columns={'Date': 'time', 
                                    'Price': 'close', 
                                    'Open': 'open', 
                                    'High': 'high', 
                                    'Low': 'low'})
        
        # 3) Remove commas
        if formatter.has_commas(self.__data_base_format):
            self.__data_base_format = formatter.remove_commas(self.__data_base_format)

        # 4) Convert to numeric
        self.__data_base_format[['close', 'open', 'high', 'low']] = self.__data_base_format[['close', 'open', 'high', 'low']].apply(pd.to_numeric)

        # 5) Convert string date to date
        self.__data_base_format['time'] = formatter.change_date_format(self.__data_base_format['time'], '%Y-%m-%d' )

        # 6) Revert dataframe
        self.__data_base_format = formatter.reverse_dataframe(self.__data_base_format)

    def get_data_base_format(self) -> pd.DataFrame:
        return self.__data_base_format