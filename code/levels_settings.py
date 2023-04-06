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
        1: [(5, 7), "knight_blue", "left", "moving"],
        2: [(10, 13), "knight_blue", "right", "moving"],
        3: [(46, 8), "knight_yellow", "left", "moving"],
        4: [(43, 13), "knight_blue", "right", "moving"],
        5: [(58, 13), "knight_red", "right", "moving"],
    },

}


levels = {
    1: test_level
}
