from enum import Enum


class AssetsIMG(str, Enum):
    # Images
    EXPLOSION_IMG = "assets/sprites/Explosion.png"
    SHIP_IMG = "assets/sprites/vaisseau.png"
    MISSILE_IMG = "assets/sprites/missile.png"
    BACKGROUND_IMG = "assets/sprites/fond.png"
    METEOR_IMG = "assets/sprites/meteor.png"


class AssetsMUSIC(str, Enum):
    # Music
    MUSIC = "assets/musics/stranger-things-124008.mp3"
