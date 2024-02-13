class PriceOutput:
    def __init__(self, price):
        self.price = price

    def to_json(self):
        return {"price": self.price if self.price else 0}