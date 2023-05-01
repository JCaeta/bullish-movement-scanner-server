
class Operator:
    __stop_loss_perc = None  
    __take_profit_perc = None
    __stop_loss_price = None
    __take_profit_price = None
    __markers = []
    __position_is_open = False
    __buy_position_open = False
    __sell_position_open = False
    __time_bars = []

    def __init__(self, stop_loss_perc, take_profit_perc):
        self.__stop_loss_perc = stop_loss_perc
        self.__take_profit_perc = take_profit_perc

    def set_stop_loss_percentage(self, percentage):
        self.__stop_loss_perc = percentage
    
    def set_take_profit_percentaje(self, percentage):
        self.__take_profit_perc = percentage

    def open_buy_position(self, time):
        self.__markers.append({
            'time': time,
            'position': 'belowBar',
            'color': 'green',
            'shape': 'arrowUp',
            'text': 'buy'
        })
        self.__position_is_open = True
        self.__buy_position_open = True
        # print("buy | ", {
        #     'time': time,
        #     'position': 'belowBar',
        #     'color': 'green',
        #     'shape': 'arrowUp',
        #     'text': 'buy'
        # })

    def open_sell_position(self, time):
        self.__markers.append({
            'time': time,
            'position': 'aboveBar',
            'color': 'red',
            'shape': 'arrowDown',
            'text': 'sell'
        })
        self.__position_is_open = True
        self.__sell_position_open = True
        # print("sell | ", {
        #     'time': time,
        #     'position': 'aboveBar',
        #     'color': 'red',
        #     'shape': 'arrowDown',
        #     'text': 'sell'
        # })

    def set_current_price(self, price, time):
        if self.__position_is_open:
            self.__time_bars.append(time)
            if self.__buy_position_open:
                if price < self.__st

    def get_markers(self):
        return self.__markers

    def position_is_open(self):
        return self.__position_is_open
    