import twstock

twstock.realtime.mock = False
unit = twstock.realtime.get("2330")
str = "\n".join(map(str, unit["realtime"]["best_bid_price"]))
print(str)
