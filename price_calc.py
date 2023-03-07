price_in = 1000000000000000000000000000000000000000000000000000000000
price_out = 1232179226069246418772385351098853723957544392402548031488


def get_final_price(initial_price: float):
    return round(initial_price * (price_out / price_in), 2)


def get_initial_price(final_price: float):
    if get_final_price(round(final_price / (price_out / price_in), 2)) == final_price:
        return round(final_price / (price_out / price_in), 2)
    elif get_final_price(round(final_price / (price_out / price_in), 3)) == final_price:
        return round(final_price / (price_out / price_in), 3)
    else:
        return round(final_price / (price_out / price_in), 4)
