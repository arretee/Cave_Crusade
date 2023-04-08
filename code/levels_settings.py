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


levels = {
    1: level1,
    2: level2
}
