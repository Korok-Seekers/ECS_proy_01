
from src.engine.service_locator import ServiceLocator


class CPlayerWeapon:
    def __init__(self, weapon: str, player_info: dict):
        self.weapon = weapon
        self.cooldown = player_info["triple_shot_cooldown"]
        self.player_info = player_info
        self.sprite = self.player_info["image"]
        self.number_of_bullets = 0
        self.max_number_of_bullets = player_info["max_number_of_bullets"]
    
    def set_weapon(self):
        if self.sprite is None:
            self.sprite = self.player_info["image"]
            self.weapon = "basic"
            self.reset_cooldown()
        
        elif self.sprite == self.player_info["alternate_image"]:
            self.sprite = self.player_info["image"]
            self.weapon = "basic"
            self.reset_cooldown()
        
        elif self.sprite == self.player_info["image"] and self.cooldown <= 0.0:
            self.sprite = self.player_info["alternate_image"]
            self.weapon = "multiple"
            self.reset_cooldown()

    def reset_cooldown(self):
        self.cooldown = self.player_info["triple_shot_cooldown"]