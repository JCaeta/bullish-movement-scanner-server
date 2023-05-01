import abc
import pandas as pd
from ..pandas_utils.pandas_utils import PandasFormatter
import datetime as dt

class IDataAdapter(abc.ABC):
    @abc.abstractmethod
    def read_data(self):
        pass

    @abc.abstractmethod
    def get_data_base_format(self) -> pd.DataFrame:
        pass

    @abc.abstractmethod
    def convert_to_base_format(self):
        pass

class CsvInvestingAdapter(IDataAdapter):
    __data = None
    __path = None
    __data_base_format = None

    def read_data(self):
        # Implementation of save_data method
        # 1) Open data.csv
        self.__data = pd.read_csv(self.__path)
        self.convert_to_base_format()

    def set_path(self, path):
        self.__path = path

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

class CsvMetatraderAdapter(IDataAdapter):
    __data = None
    __path = None
    __data_base_format = None

    def read_data(self):
        self.__data = pd.read_csv(self.__path, delimiter="\t")
        print(self.__data)
        self.convert_to_base_format()

    def convert_to_base_format(self):
        # 0) Instanciate elements
        # formatter = PandasFormatter()
        # ui_data = []

        # 1) Get the columns we need
        self.__data_base_format = self.__data[['<DATE>', '<TIME>', '<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>']]

        # 2) Merge <DATE> and <TIME> column
        # - The columns are merged into the <TIME> column with the format "2023-02-27 15:50:00"
        # - The <DATE> column is removed
        self.__data_base_format = self.__merge_date_time_columns(self.__data_base_format)

        # 3) Convert <TIME> format "2023-02-27 15:50:00" to timestamps ()
        # - timestamps are necessary to plot intraday data into the UI
        self.__data_base_format['<TIME>'] = self.__data_base_format['<TIME>'].apply(lambda x: int(dt.datetime.timestamp(x)))

        # 4) Rename columns
        self.__data_base_format = self.__data_base_format.rename(columns={'<TIME>': 'time', 
                                    '<CLOSE>': 'close', 
                                    '<OPEN>': 'open', 
                                    '<HIGH>': 'high', 
                                    '<LOW>': 'low'})
        
        # 5) Convert to numeric
        self.__data_base_format[['close', 'open', 'high', 'low']] = self.__data_base_format[['close', 'open', 'high', 'low']].apply(pd.to_numeric)
    
    def get_data_base_format(self):
        return self.__data_base_format

    # def get_data_ui_format(self) -> list:
    #     ui_data = []
    #     for index, row in self.__data.iterrows():
    #         ui_data.append({'time': row['time'],  'open': row['open'], 'high': row['high'], 'low': row['low'], 'close': row['close']})
    #     return ui_data

    def set_path(self, path):
        self.__path = path

    def __merge_date_time_columns(self, df):
        # Merge the <DATE> and <TIME> columns into a single column
        df['<TIME>'] = pd.to_datetime(df['<DATE>'] + ' ' + df['<TIME>'])

        # Drop the original <DATE> column
        df.drop(['<DATE>'], axis=1, inplace=True)

        return df
    

