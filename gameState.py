class GameState:
    def __init__(self):
        self.screen_width = 650
        self.screen_height = 650
        self.sfx_volume = 0.6
        self.bgm_volume = 0.6
        self.bg_music = None  # Loaded later
        self.coin_sound = None  # Loaded later
        self.jump_sound = None  # Loaded later
