class Player:
    name: str
    money: int

    def __init__(self, name: str, money: float = 0):
        self.name = name
        self.money = money

    def __str__(self):
        return f"{self.name:<10}: ${self.money:>3}"

