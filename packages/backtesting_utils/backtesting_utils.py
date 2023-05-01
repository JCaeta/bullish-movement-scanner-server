import pandas as pd

class Data:
    # Iterable data object

    def __init__(self, data: pd.DataFrame):
        if data.empty:
            raise ValueError("Empty data passed to backtest.")
        self._data = data
        self._data_len = len(data)
    
    def add_column(self, name: str, column: pd.Series):
        self._data[name] = column
    
    def data(self, lookback:int=-1):
        '''
        data()

        Returns the data UP TO self._data_len
        lookback is set to a positive integer to view the previous 'lookback' rows up to self._data_len
        '''
        start:int = 0
        end:int = self._data_len
        if lookback < -1:
            raise ValueError("Lookback cannot be less than zero.")
        else:
            start = self._data_len - lookback

        return self._data.iloc[ start:end ]
    
    def _init(self):
        self._data_len = 0
    
    def _next(self):
        if self._data_len > len(self._data):
            raise IndexError("Last data row reached. Run _init to start over.")

        self._data_len += 1
        return self._data.iloc[self._data_len-1]
    
    def _has_next(self):
        return (self._data_len) < len(self._data)
        
    def __len__(self):
        return self._data_len
    
class Backtest:
    # def __init__(self, data, strategy:Type[Strategy]):
    def __init__(self, data, strategy):
        self.strategy = strategy

        # Create iterable data object containing dataframe
        self._data_test = Data(data)

    def clear(self):
        self.strategy.clear()
    
    def run(self):
        # Iterate through the data one at a time.
        self._data_test._init()
        
        while(self._data_test._has_next()):
            # Obtain the current data value
            current_data = self._data_test._next()
            self.strategy.set_current_data(current_data)
            
            """
            current_data example

            time     1.635549e+09
            open     1.155160e+00
            high     1.155310e+00
            low      1.155110e+00
            close    1.155260e+00
            """
    
    def next(self):
        if self._data_test._has_next():
            return self.strategy.on_price_event(self._data_test._next())
            
    
            
