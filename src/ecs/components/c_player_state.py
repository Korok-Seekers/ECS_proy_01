from enum import Enum


class CPlayerState:
    def __init__(self):
        self.state = PlayerState.IDLE


class PlayerState(Enum):
    IDLE = 0
    MOVE = 1
