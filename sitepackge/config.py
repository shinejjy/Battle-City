import pygame

fps = 45  # 帧频
image_dict = {}  # 存放所有素材图片的字典
Maps: None  # Map类实例
width, height = 13 * 64, 13 * 64  # 地图尺寸
size = 17 * 64, 13 * 64
bullet_speed = 18  # 子弹速度
player_control = [[pygame.K_w, pygame.K_d, pygame.K_s, pygame.K_a, pygame.K_j, pygame.K_q],
                  [pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT, pygame.K_BACKSLASH, pygame.K_KP_ENTER]]

# 不同敌方坦克类型标签
enemy_label = {
    'tank0': {  # normal
        'level0': {'move_speed': 2, 'fire_speed': 0.8, 'HP': 1},
        'level1': {'move_speed': 2, 'fire_speed': 0.8, 'HP': 2},
        'level2': {'move_speed': 2, 'fire_speed': 0.8, 'HP': 3},
        'level3': {'move_speed': 2, 'fire_speed': 0.8, 'HP': 4},
    },
    'tank1': {  # high-fire-speed/high-move-speed/low-hp
        'level0': {'move_speed': 2, 'fire_speed': 0.5, 'HP': 1},
        'level1': {'move_speed': 3, 'fire_speed': 0.5, 'HP': 1},
        'level2': {'move_speed': 3, 'fire_speed': 0.4, 'HP': 1},
        'level3': {'move_speed': 4, 'fire_speed': 0.5, 'HP': 1},
    },
    'tank2': {  # better
        'level0': {'move_speed': 2, 'fire_speed': 0.7, 'HP': 2},
        'level1': {'move_speed': 2, 'fire_speed': 0.7, 'HP': 3},
        'level2': {'move_speed': 2, 'fire_speed': 0.7, 'HP': 4},
        'level3': {'move_speed': 2, 'fire_speed': 0.7, 'HP': 5},
    },
    'tank3': {  # normal-fire-speed/low-move-speed/high-hp
        'level0': {'move_speed': 1, 'fire_speed': 0.8, 'HP': 5},
        'level1': {'move_speed': 1, 'fire_speed': 0.8, 'HP': 6},
        'level2': {'move_speed': 1, 'fire_speed': 0.8, 'HP': 7},
        'level3': {'move_speed': 1, 'fire_speed': 0.8, 'HP': 8},
    }
}

# 我方坦克标签
player_label = {
    0: {'move_speed': 3, 'fire_speed': 0.7, 'HP': 3},
    1: {'move_speed': 3, 'fire_speed': 0.6, 'HP': 4},
    2: {'move_speed': 5, 'fire_speed': 0.5, 'HP': 4},
    3: {'move_speed': 5, 'fire_speed': 0.4, 'HP': 7},
}

pre_enemy = [  # 出生点产生的敌人标签
    [
        [{'enemy_type': 'tank0', 'level': 0}, {'enemy_type': 'tank0', 'level': 0}, {'enemy_type': 'tank2', 'level': 0},
         {'enemy_type': 'tank0', 'level': 0}],
        [{'enemy_type': 'tank1', 'level': 3}, {'enemy_type': 'tank3', 'level': 3}, {'enemy_type': 'tank0', 'level': 1},
         {'enemy_type': 'tank0', 'level': 0}],
        [{'enemy_type': 'tank2', 'level': 2}, {'enemy_type': 'tank0', 'level': 2}, {'enemy_type': 'tank2', 'level': 3},
         {'enemy_type': 'tank0', 'level': 0}]
    ],
    [
        [{'enemy_type': 'tank0', 'level': 0}, {'enemy_type': 'tank0', 'level': 0}, {'enemy_type': 'tank2', 'level': 0}],
        [{'enemy_type': 'tank1', 'level': 3}, {'enemy_type': 'tank3', 'level': 3}, {'enemy_type': 'tank0', 'level': 1}],
        [{'enemy_type': 'tank2', 'level': 2}, {'enemy_type': 'tank0', 'level': 2}, {'enemy_type': 'tank2', 'level': 3}]
    ],
    [
        [{'enemy_type': 'tank0', 'level': 0}, {'enemy_type': 'tank0', 'level': 0}, {'enemy_type': 'tank2', 'level': 0}],
        [{'enemy_type': 'tank1', 'level': 3}, {'enemy_type': 'tank3', 'level': 3}, {'enemy_type': 'tank0', 'level': 1}],
        [{'enemy_type': 'tank2', 'level': 2}, {'enemy_type': 'tank0', 'level': 2}, {'enemy_type': 'tank2', 'level': 3}]
    ],
    [
        [{'enemy_type': 'tank0', 'level': 0}, {'enemy_type': 'tank0', 'level': 0}, {'enemy_type': 'tank2', 'level': 0},
         {'enemy_type': 'tank0', 'level': 0}],
        [{'enemy_type': 'tank1', 'level': 3}, {'enemy_type': 'tank3', 'level': 3}, {'enemy_type': 'tank0', 'level': 1},
         {'enemy_type': 'tank0', 'level': 0}],
        [{'enemy_type': 'tank2', 'level': 2}, {'enemy_type': 'tank0', 'level': 2}, {'enemy_type': 'tank2', 'level': 3},
         {'enemy_type': 'tank0', 'level': 0}]
    ],
    [
        [{'enemy_type': 'tank1', 'level': 0}, {'enemy_type': 'tank1', 'level': 0}, {'enemy_type': 'tank2', 'level': 0}],
        [{'enemy_type': 'tank3', 'level': 3}, {'enemy_type': 'tank2', 'level': 3}, {'enemy_type': 'tank0', 'level': 1}],
        [{'enemy_type': 'tank1', 'level': 2}, {'enemy_type': 'tank0', 'level': 2}, {'enemy_type': 'tank2', 'level': 3}]
    ],
    [
        [{'enemy_type': 'tank0', 'level': 0}, {'enemy_type': 'tank0', 'level': 0}, {'enemy_type': 'tank2', 'level': 0}],
        [{'enemy_type': 'tank1', 'level': 3}, {'enemy_type': 'tank3', 'level': 3}, {'enemy_type': 'tank0', 'level': 1}],
        [{'enemy_type': 'tank2', 'level': 0}, {'enemy_type': 'tank0', 'level': 2}, {'enemy_type': 'tank2', 'level': 3}]
    ],
    [
        [{'enemy_type': 'tank3', 'level': 3}, {'enemy_type': 'tank0', 'level': 0}, {'enemy_type': 'tank2', 'level': 0}],
        [{'enemy_type': 'tank1', 'level': 3}, {'enemy_type': 'tank1', 'level': 3}, {'enemy_type': 'tank0', 'level': 1}],
        [{'enemy_type': 'tank2', 'level': 2}, {'enemy_type': 'tank2', 'level': 2}, {'enemy_type': 'tank2', 'level': 3}]
    ],
    [
        [{'enemy_type': 'tank0', 'level': 0}, {'enemy_type': 'tank2', 'level': 3}, {'enemy_type': 'tank2', 'level': 0}],
        [{'enemy_type': 'tank1', 'level': 3}, {'enemy_type': 'tank3', 'level': 3}, {'enemy_type': 'tank0', 'level': 1}],
        [{'enemy_type': 'tank2', 'level': 2}, {'enemy_type': 'tank0', 'level': 2}, {'enemy_type': 'tank2', 'level': 3}]
    ]
]

oooo = [20, 20, 20, 20]

ooox = [20, 20, 20, 0]
ooxo = [20, 20, 0, 20]
oxoo = [20, 0, 20, 20]
xooo = [0, 20, 20, 20]

ooxx = [20, 20, 0, 0]
oxxo = [20, 0, 0, 20]
xxoo = [0, 0, 20, 20]
oxox = [20, 0, 20, 0]
xoxo = [0, 20, 0, 20]
xoox = [0, 20, 20, 0]

oxxx = [20, 0, 0, 0]
xoxx = [0, 20, 0, 0]
xxox = [0, 0, 20, 0]
xxxo = [0, 0, 0, 20]

xxxx = [24, 24, 24, 24]

Map_data = [  # 地图数据
    [
        [31, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 31],
        [0, 0, 0, 0, 25, 25, 25, 25, 25, 0, 0, 0, 0],
        [0, 0, 23, 0, oooo, oooo, oooo, oooo, oooo, 0, oooo, oooo, 0],
        [25, 23, oooo, 0, 0, 0, 0, 0, 0, 0, oooo, oooo, 0],
        [0, 0, 23, 0, 1, 22, 22, 22, 2, 0, 0, 0, 0],
        [25, 23, oooo, 0, oooo, xxxx, 23, xxxx, oooo, 0, oooo, oooo, 0],
        [0, oooo, 23, 0, xxxx, 23, 30, 23, xxxx, 0, oooo, 0, 0],
        [25, 23, 0, 0, oooo, xxxx, 23, xxxx, oooo, 0, 0, 0, 0],
        [0, 0, 23, 0, 0, 0, xxxx, 0, 0, 0, oooo, oooo, 0],
        [0, 0, 22, 22, 22, 22, 22, 22, 22, 22, 22, oooo, 0],
        [0, 0, 22, 21, 21, 21, 21, 21, 21, 21, 22, oooo, 0],
        [0, 0, 22, 21, 21, 21, 21, 21, 21, 21, 22, 0, 0],
        [31, 0, 22, 22, 22, 22, 22, 22, 22, 22, 22, 0, 31]
    ],
    [
        [0, 22, 22, 22, 0, 0, 31, 0, 0, 22, 22, 22, 22],
        [25, 0, 31, 0, 0, 0, 0, 0, 0, 0, 31, 0, 25],
        [25, 0, 0, xxxx, 0, 0, xxxx, 0, 0, xxxx, 0, 0, 25],
        [25, 0, 23, 0, oooo, oooo, oooo, oooo, oooo, 0, 0, 23, 25],
        [25, 0, 23, 0, oooo, oooo, oooo, oooo, oooo, 0, 0, 23, 25],
        [25, 0, 0, 1, oooo, oooo, 30, oooo, oooo, 2, 23, 23, 25],
        [25, 23, 23, 0, oooo, oooo, oooo, oooo, oooo, 0, 0, 0, 25],
        [25, 0, 0, 0, oooo, oooo, oooo, oooo, oooo, 0, 23, 0, 25],
        [25, 0, 23, 0, 0, 0, 0, 23, 0, 0, 0, 0, 25],
        [25, 0, 23, 0, 0, 23, 0, 0, 0, 23, 0, 22, 25],
        [25, 0, 0, 23, 0, 0, 23, 0, 0, 0, 0, 22, 25],
        [25, 0, 0, 21, 21, 21, 21, 21, 0, 23, 0, 22, 25],
        [0, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 0]
    ],
    [
        [23, 23, 31, 0, 0, 0, 31, 0, 0, 0, 31, oooo, oooo],
        [23, 0, 0, 0, 0, 0, 0, 0, 0, 0, 23, 21, oooo],
        [0, 0, 0, 0, 0, oooo, oooo, oooo, 0, 0, oooo, 21, 0],
        [22, 21, 21, oooo, 0, 0, 0, 0, 0, 0, oooo, oooo, 0],
        [22, 23, oooo, oooo, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [22, 0, xxxx, 0, 0, 21, 23, 21, 0, 0, 0, 0, 0],
        [0, 0, 25, 0, 0, 23, xxxx, 23, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 21, 23, 21, 0, 0, xxxx, 0, 22],
        [0, 0, 25, 0, 0, 0, 0, 0, 0, oooo, oooo, 23, 22],
        [0, oooo, oooo, 0, 0, oooo, oooo, oooo, 0, oooo, 21, 21, 22],
        [0, 21, oooo, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [oooo, 21, 23, 25, 0, oooo, oooo, oooo, 0, 0, 0, 0, 23],
        [oooo, oooo, 0, 25, 1, oooo, 30, oooo, 2, 0, 0, 23, 23]
    ],
    [
        [31, xxxx, 23, 23, 25, 25, 25, 25, 25, 0, 23, 23, 31],
        [23, 23, 23, 0, 23, 23, 23, 23, 23, 23, 0, 23, xxxx],
        [23, 0, oooo, oooo, 23, 23, 23, 0, 0, oooo, oooo, 23, 23],
        [0, 23, oooo, xxxx, 21, 21, xxxx, 21, 21, xxxx, oooo, 0, 23],
        [25, 23, 0, 21, 22, 22, 22, 22, 22, 21, 23, 23, 25],
        [25, 23, 23, 21, 22, 1, 22, 22, 22, 21, 23, 23, 25],
        [25, 23, 23, xxxx, 22, 22, 30, 22, 22, xxxx, 0, 23, 25],
        [25, 23, 23, 21, 22, 22, 22, 2, 22, 21, 23, 23, 25],
        [25, 23, 0, 21, 22, 22, 22, 22, 22, 21, 0, 23, 25],
        [0, 23, oooo, xxxx, 21, 21, xxxx, 21, 21, xxxx, oooo, 23, 23],
        [23, 23, oooo, oooo, 0, 23, 23, 23, 0, oooo, oooo, 0, 23],
        [xxxx, 0, 23, 23, 23, 0, 23, 23, 23, 23, 23, 23, 23],
        [31, 23, 23, 23, 25, 25, 25, 25, 25, 0, 23, xxxx, 31]
    ],

    [
        [31, 0, 0, 0, 0, 0, 31, 0, 0, 0, 0, 0, 31],
        [0, oooo, 0, oooo, 0, oooo, 0, oooo, 0, oooo, 0, oooo, 0],
        [0, oooo, 0, oooo, 0, oooo, xxxx, oooo, 0, oooo, 0, oooo, 0],
        [0, oooo, 0, oooo, 0, oooo, 0, oooo, 0, oooo, 0, oooo, 0],
        [0, oooo, 0, oooo, 0, 0, 0, 0, 0, oooo, 0, oooo, 0],
        [0, 0, 0, 0, 0, oooo, 0, oooo, 0, 0, 0, 0, 0],
        [xxxx, 0, oooo, oooo, 0, 0, 0, 0, 0, oooo, oooo, 0, xxxx],
        [0, 0, 0, 0, 0, oooo, 0, oooo, 0, 0, 0, 0, 0],
        [0, oooo, 0, oooo, 0, oooo, oooo, oooo, 0, oooo, 0, oooo, 0],
        [0, oooo, 0, oooo, 0, oooo, 0, oooo, 0, oooo, 0, oooo, 0],
        [0, oooo, 0, oooo, 0, 0, 0, 0, 0, oooo, 0, oooo, 0],
        [0, oooo, 0, oooo, 0, oooo, oooo, oooo, 0, oooo, 0, oooo, 0],
        [0, 0, 0, 0, 1, oooo, 30, oooo, 2, 0, 0, 0, 0]
    ],

    [
        [22, 0, 31, 0, 0, 0, 31, 0, 0, 0, 31, 0, 0],
        [22, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [22, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [22, 0, oooo, oooo, 0, 0, 0, 0, 0, oooo, oooo, 0, 0],
        [22, 0, oooo, oooo, 23, 23, 23, 23, 23, oooo, oooo, 0, 0],
        [22, 0, oooo, oooo, 21, 21, 21, 21, 21, oooo, oooo, 0, 0],
        [22, 0, oooo, oooo, 23, 23, 23, 23, 23, oooo, oooo, 0, 0],
        [22, 0, oooo, oooo, 0, 0, 0, 0, 0, oooo, oooo, 0, 0],
        [22, 0, oooo, oooo, 0, 0, 0, 0, 0, oooo, oooo, 0, 0],
        [22, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [22, 0, 0, 1, xxxx, xxxx, xxxx, xxxx, xxxx, 2, 0, 0, 0],
        [22, 0, 0, 0, xxxx, oooo, oooo, oooo, xxxx, 0, 0, 0, 0],
        [22, 0, 0, 0, xxxx, oooo, 30, oooo, xxxx, 0, 0, 0, 0]
    ],

    [
        [31, 0, 0, 0, 0, 0, 31, 0, 0, 0, 0, 0, 31],
        [0, oooo, 0, oooo, 0, oooo, 0, oooo, 0, oooo, 0, oooo, 0],
        [0, oooo, 0, oooo, 0, oooo, xxxx, oooo, 0, oooo, 0, oooo, 0],
        [0, oooo, 0, oooo, 0, oooo, 0, oooo, 0, oooo, 0, oooo, 0],
        [0, oooo, 0, oooo, 0, 0, 0, 0, 0, oooo, 0, oooo, 0],
        [0, 0, 0, 0, 0, oooo, 0, oooo, 0, 0, 0, 0, 0],
        [xxxx, 0, oooo, oooo, 0, 0, 0, 0, 0, oooo, oooo, 0, xxxx],
        [0, 0, 0, 0, 0, oooo, 0, oooo, 0, 0, 0, 0, 0],
        [0, oooo, 0, oooo, 0, oooo, oooo, oooo, 0, oooo, 0, oooo, 0],
        [0, oooo, 0, oooo, 0, oooo, 0, oooo, 0, oooo, 0, oooo, 0],
        [0, oooo, 0, oooo, 0, 0, 0, 0, 0, oooo, 0, oooo, 0],
        [0, oooo, 0, oooo, 0, oooo, oooo, oooo, 0, oooo, 0, oooo, 0],
        [0, 0, 0, 0, 1, oooo, 30, oooo, 2, 0, 0, 0, 0]
    ],

    [
        [0, 0, 31, 0, 0, 0, 31, 0, 0, 0, 31, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 23, 0, 0, 0, 0],
        [0, 0, 0, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 21, 0, 0, oooo, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, oooo, oooo, oooo, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, oooo, 30, oooo, 0, 0, 0, 0, 0]
    ],

    [
        [0, 23, 31, 31, 31, 23, 23, 23, 23, 23, 23, 23, 23],
        [0, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23],
        [0, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23],
        [0, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23],
        [0, 23, 23, 23, 23, 22, 0, 23, 23, 23, 23, 23, 23],
        [0, 23, 22, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23],
        [0, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23],
        [0, 23, 23, 23, 22, 23, 23, 23, 23, 0, 23, 23, 23],
        [0, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23],
        [0, 23, 23, 22, 23, 0, 22, 23, 23, 23, 23, 23, 23],
        [0, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23],
        [1, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23],
        [2, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23],
    ],
    [

    ]
]
