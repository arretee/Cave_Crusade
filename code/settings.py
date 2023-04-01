screen_resolutions = [[1280, 720], [1600, 900], [1920, 1080]]

pathes = {
    "character": {
        "axe": {
            "attack": "../graphics/characters/basic/axe/attack",
            "idle": "../graphics/characters/basic/axe/idle",
            "run": "../graphics/characters/basic/axe/run",
        },
        "basic": {
            "climb": "../graphics/characters/basic/basic/climb",
            "idle": "../graphics/characters/basic/basic/idle",
            "jump": "../graphics/characters/basic/basic/jump",
            "run": "../graphics/characters/basic/basic/run",
        },
        "bow": {
            "attack": "../graphics/characters/basic/bow/attack",
            "idle": "../graphics/characters/basic/bow/idle",
            "run": "../graphics/characters/basic/bow/run",
        },
        "sword": {
            "attack": "../graphics/characters/basic/sword/attack",
            "idle": "../graphics/characters/basic/sword/idle",
            "run": "../graphics/characters/basic/sword/run",
        },
    },
    "enemy": {
        "barbarian": {
            "attack": "../graphics/characters/barbarian/attack",
            "idle": "../graphics/characters/barbarian/idle",
            "run": "../graphics/characters/barbarian/run"
        },
        "dwarf": {
            "attack": "../graphics/characters/dwarf/attack",
            "idle": "../graphics/characters/dwarf/idle",
            "run": "../graphics/characters/dwarf/run"
        },
        "guard": {
            "attack": "../graphics/characters/guard/attack",
            "idle": "../graphics/characters/guard/idle",
            "run": "../graphics/characters/guard/run"
        },
        "knight_blue": {
            "attack": "../graphics/characters/knight_blue/attack",
            "idle": "../graphics/characters/knight_blue/idle",
            "run": "../graphics/characters/knight_blue/run"
        },
        "knight_green": {
            "attack": "../graphics/characters/knight_green/attack",
            "idle": "../graphics/characters/knight_green/idle",
            "run": "../graphics/characters/knight_green/run"
        },
        "knight_red": {
            "attack": "../graphics/characters/knight_red/attack",
            "idle": "../graphics/characters/knight_red/idle",
            "run": "../graphics/characters/knight_red/run"
        },
        "knight_yellow": {
            "attack": "../graphics/characters/knight_yellow/attack",
            "idle": "../graphics/characters/knight_yellow/idle",
            "run": "../graphics/characters/knight_yellow/run"
        },
        "lizard": {
            "attack": "../graphics/characters/lizard/attack",
            "idle": "../graphics/characters/lizard/idle",
            "run": "../graphics/characters/lizard/run"
        },
        "mooseman": {
            "attack": "../graphics/characters/mooseman/attack",
            "idle": "../graphics/characters/mooseman/idle",
            "run": "../graphics/characters/mooseman/run"
        },
        "rhino": {
            "attack": "../graphics/characters/rhino/attack",
            "idle": "../graphics/characters/rhino/idle",
            "run": "../graphics/characters/rhino/run"
        },
        "troll": {
            "attack": "../graphics/characters/troll/attack",
            "idle": "../graphics/characters/troll/idle",
            "run": "../graphics/characters/troll/run"
        },

    },
    "items": {},
}


characters_data = {
    "player": {
        # Health / Attack params
        "health": 100,
        "axe_damage": 50,
        "sword_damage": 35,
        "bow_damage": 75,


        # basic parms - game scale / value
        "speed" : 2,
        "gravity_speed": 75,
        "jump_speed": -1,
        "sword_kd": 2000,
        "axe_kd": 1000,
        "bow_kd": 4000,

        # animation value
        "animation_speed": 0.07,

        # Hit box - game scale * value
        "x_inflate": -8,
        "y_inflate": -6,


        # Hits KD - parms
        "HitBounceX": 6,  # Scale / value
        "HitBounceY": 3,  # Scale / value
        "MoveAfterHit_kd": 500,
    },

    # -------------------------------------------- Easy Enemies --------------------------------------------
    "blue_knigt": {
        "health": 50,
        "damage": 15,


        # basic parms - game scale / value
        "speed": 4,
        "gravity_speed": 75,
        "jump_speed": -1,

        # animation value
        "animation_speed": 0.07,

        # Hit box - game scale * value
        "x_inflate": -10,
        "y_inflate": -10,

        # Hits KD - parms
        "MoveAfterHit_kd": 400,
        "HitBounceX": 6,  # Scale / value
        "HitBounceY": 3,  # Scale / value


        # X Change - Scale * Value
        "idle": True,
        "x_idle": 0,
        "y_idle": -4,
        "run": True,
        "x_run": 0,
        "y_run": -4,
        "attack": True,
        "x_attack": 0,
        "y_attack": -4,
    },
    # -------------------------------------------- Normal Enemies --------------------------------------------
    # -------------------------------------------- Hard Enemies --------------------------------------------

}
