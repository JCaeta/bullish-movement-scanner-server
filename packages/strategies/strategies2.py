import pandas as pd

class Strategy1: 
    def on_price_event(self, data):
        """
        Data is a pandas array
        format:
            time     1.635549e+09
            open     1.155160e+00
            high     1.155310e+00
            low      1.155110e+00
            close    1.155260e+00

        Example of how to get the time
        time = data[time]
        """

        # self.candlesticks.append(data)
        # return { 'time': data['time'], 'open': data['open'], 'high': data['high'], 'low': data['low'], 'close': data['close'] }
        return data

class StrategyPriceTrigger:
    def __init__(self, entry_price: float, 
                 upper_price: float, 
                 lower_price: float, 
                 func_lower_close, 
                 func_upper_close):
        self.candlesticks = []
        self.upper_price = upper_price
        self.lower_price = lower_price
        self.entry_price = entry_price
        self.close_price = None
        self.func_lower_close = func_lower_close
        self.func_upper_close = func_upper_close

    def on_price_event(self, data):
        """
        Data is a pandas array
        format:
            time     1.635549e+09
            open     1.155160e+00
            high     1.155310e+00
            low      1.155110e+00
            close    1.155260e+00

        Example of how to get the time
        time = data[time]
        """

        self.candlesticks.append(data)

        if((data["open"] or data["high"] or data["low"] or data["close"]) >= self.upper_price):
            self.upper_price_event()
        elif((data["open"] or data["high"] or data["low"] or data["close"]) <= self.lower_price):
            self.lower_price_event()
    
    def upper_price_event(self):
        self.close(self.upper_price)
        self.func_upper_close()

    def lower_price_event(self):
        self.close(self.lower_price)
        self.func_lower_close()

    def close(self, price):
        self.close_price = price

    def set_lower_price(self, lower_price):
        self.lower_price = lower_price

class Movement:
    def __init__(self, entry_price, close_price, candlesticks):
        self.candlesticks = candlesticks
        self.entry_price = entry_price
        self.close_price = close_price
    
    def set_candlesticks(self, candlesticks):
        self.candlesticks = candlesticks

class StrategyMovementTracker:
    def __init__(self):
        self.entry_price = None
        self.long_percentage = None
        self.short_percentage = None
        self.upper_price = None
        self.lower_price = None
        self.movements = []
        self.max_price = None

    def clear(self):
        self.entry_price = None
        self.long_percentage = None
        self.short_percentage = None
        self.upper_price = None
        self.lower_price = None
        self.movements = []

    def start_tracking(self, entry_price: float, long_percentage: float, max_correction_percentage: float):
        self.entry_price = entry_price
        self.long_percentage = long_percentage
        self.max_correction_percentage = max_correction_percentage
        self.max_price = self.entry_price

        upper_price = self.entry_price + (self.entry_price*self.long_percentage)
        lower_price = self.entry_price - (self.entry_price*self.max_correction_percentage)

        self.price_trigger = StrategyPriceTrigger(self.entry_price, 
                                                  upper_price, lower_price, 
                                                  self.func_lower_close,
                                                  self.func_upper_close)

    def set_max_correction(self, max_price):
        self.price_trigger.set_lower_price(max_price - (max_price*self.max_correction_percentage))

    def set_current_data(self, data):
        """
        data: DataFrame.series
        """
        # 1) If there is not open operation, open one
        if self.entry_price == None:
            self.start_tracking(data['open'], 0.1, 0.07)

        # 2) Check and set max price
        max_value = max([data["open"], data["high"], data["low"], data["close"]])
        if (max_value > self.max_price):
            self.max_price = max_value
            self.set_max_correction(self.max_price)

        # 3) Send data to price trigger
        self.price_trigger.on_price_event(data)
        
    def func_upper_close(self):
        move = Movement(self.entry_price, self.price_trigger.close_price, self.price_trigger.candlesticks)
        self.movements.append(move)

        self.entry_price = None
        self.long_percentage = None
        self.short_percentage = None
        self.upper_price = None
        self.lower_price = None

    def func_lower_close(self):
        self.entry_price = None
        self.long_percentage = None
        self.short_percentage = None
        self.upper_price = None
        self.lower_price = None
