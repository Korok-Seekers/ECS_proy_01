class CEnemy:
    def __init__(self, score:int, cooldown:int, probability:float) -> None:
        self.score = score
        self.cooldown = cooldown
        self.probability = probability
        self.timer = 0
