# Sample
# level_name = {
#     "enemies": {
#              pos , enemy_type, start_facing , moving or stay
#         1: [(5, 7), "blue_knigt", "left", "moving"]
#     },
# }



level1 = {
    "tmx_path": "../map/levels/level1.tmx",
    "enemies": {
        1: [(7, 7), "knight_blue", "left", "moving"],
        2: [(10, 13), "knight_blue", "left", "staying"],
        3: [(36, 8), "lizard", "left", "staying"],
        4: [(43, 8), "knight_blue", "left", "moving"],
        5: [(72, 8), "guard", "left", "moving"],
        6: [(80, 5), "lizard", "left", "moving"],
        7: [(39, 13), "guard", "left", "moving"],
        8: [(66, 13), "dwarf", "left", "moving"],
        9: [(83, 13), "guard", "left", "staying"],
        10: [(52, 7), "guard", "left", "staying"],

    },
}

level2 = {
    "tmx_path": "../map/levels/level2.tmx",
    "enemies": {
        1: [(18, 6), "knight_blue", "left", "staying"],
        2: [(24, 6), "knight_blue", "right", "staying"],
        3: [(20, 6), "lizard", "left", "moving"],

        5: [(54, 8), "knight_blue", "left", "staying"],
        6: [(66, 8), "knight_blue", "right", "staying"],

        7: [(66, 8), "mooseman", "right", "moving"],

        8: [(72, 6), "knight_blue", "left", "staying"],
        9: [(82, 6), "knight_blue", "right", "staying"],
        10: [(77, 6), "knight_yellow", "right", "moving"],

    },
}

level3 = {
    "tmx_path": "../map/levels/level3.tmx",
    "enemies": {
        1: [(17, 15), "knight_blue", "left", "staying"],
        2: [(23, 15), "knight_yellow", "left", "moving"],
        3: [(29, 15), "knight_blue", "right", "staying"],

        4: [(58, 14), "knight_red", "right", "moving"],

        5: [(38, 9), "knight_blue", "right", "staying"],
        7: [(32, 9), "rhino", "right", "moving"],
        8: [(26, 9), "knight_blue", "left", "staying"],

        9: [(14, 10), "lizard", "left", "moving"],
        10: [(7, 9), "rhino", "left", "moving"],

        11: [(53, 5), "knight_blue", "left", "moving"],
        12: [(59, 5), "knight_blue", "right", "moving"],

        13: [(43, 3), "guard", "right", "moving"],

        14: [(33, 2), "knight_yellow", "right", "moving"],
        15: [(12, 3), "knight_blue", "right", "moving"],

        16: [(69, 3), "knight_blue", "right", "moving"],
        17: [(84, 2), "lizard", "right", "moving"],
        18: [(98, 3), "knight_yellow", "right", "moving"],

        19: [(79, 8), "knight_blue", "right", "moving"],
        20: [(92, 9), "guard", "right", "moving"],
        21: [(106, 9), "lizard", "right", "moving"],

        22: [(78, 15), "guard", "right", "moving"],
        23: [(96, 15), "knight_blue", "right", "moving"],
        24: [(106, 14), "knight_yellow", "right", "moving"],
    },
}



levels = {
    1: level1,
    2: level2,
    3: level3,
}
