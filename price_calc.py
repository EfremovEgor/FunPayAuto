price_in = 1000000000000000000000000000000000000000000000000000000000
price_out = 1232179226069246418772385351098853723957544392402548031488


def get_final_price(initial_price: float):
    return round(initial_price * (price_out / price_in), 3)


def get_initial_price(final_price: float):
    return round(final_price / (price_out / price_in), 3)
