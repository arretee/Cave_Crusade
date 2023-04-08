# Sample
# level_name = {
#     "enemies": {
#              pos , enemy_type, start_facing , moving or stay
#         1: [(5, 7), "blue_knigt", "left", "moving"]
#     },
# }



test_level = {
    "tmx_path": "../map/levels/level_test1.tmx",
    "enemies": {
        1: [(7, 7), "knight_blue", "left", "moving"],
        2: [(10, 13), "troll", "left", "staying"],
        3: [(46, 8), "knight_red", "left", "moving"],
        4: [(43, 13), "barbarian", "right", "moving"],
        5: [(58, 13), "knight_yellow", "right", "moving"],
    },
}

level_1 = {
    "tmx_path": "../map/levels/level_1.tmx",
    "enemies": {
    },
}


levels = {
    1: test_level,
    2: level_1
}
