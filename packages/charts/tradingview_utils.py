def create_rect(start_price, end_price, candlesticks):
    rect_coordinates = []
    n = len(candlesticks)
    # Slope
    m = (end_price - start_price)/(n - 1) 
    for i, cs in enumerate(candlesticks):
        y = m*i + start_price
        rect_coordinates.append({'time': cs['time'], 'value': y})
    return rect_coordinates


