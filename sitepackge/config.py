import pygame

command = False
multiplayer = 2
font = None
fps = 60  # 帧频
image_dict = {}  # 存放所有素材图片的字典
audio_dict = {}  # 存放所有音效的字典
Maps: None  # Map类实例
width, height = 13 * 64, 13 * 64  # 地图尺寸
size = 17 * 64, 13 * 64
bullet_speed = 18  # 子弹速度
player_control = [[pygame.K_w, pygame.K_d, pygame.K_s, pygame.K_a, pygame.K_j, pygame.K_q],
                  [pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RETURN, pygame.K_p]]
enemy_menu, food_menu, help_menu, esc_menu, lose_stage_menu, player_menu, main_menu, select_level_menu = \
    None, None, None, None, None, None, None, None
# 不同敌方坦克类型标签
enemy_label = {
    'tank0': {  # normal
        'level0': {'move_speed': 2, 'fire_speed': 0.8, 'HP': 1, 'score': 100},
        'level1': {'move_speed': 2, 'fire_speed': 0.8, 'HP': 2, 'score': 200},
        'level2': {'move_speed': 2, 'fire_speed': 0.8, 'HP': 3, 'score': 300},
        'level3': {'move_speed': 2, 'fire_speed': 0.8, 'HP': 4, 'score': 400},
    },
    'tank1': {  # high-fire-speed/high-move-speed/low-hp
        'level0': {'move_speed': 2, 'fire_speed': 0.5, 'HP': 1, 'score': 100},
        'level1': {'move_speed': 3, 'fire_speed': 0.5, 'HP': 1, 'score': 200},
        'level2': {'move_speed': 3, 'fire_speed': 0.4, 'HP': 1, 'score': 400},
        'level3': {'move_speed': 4, 'fire_speed': 0.5, 'HP': 1, 'score': 500},
    },
    'tank2': {  # better
        'level0': {'move_speed': 2, 'fire_speed': 0.7, 'HP': 2, 'score': 200},
        'level1': {'move_speed': 2, 'fire_speed': 0.7, 'HP': 3, 'score': 300},
        'level2': {'move_speed': 2, 'fire_speed': 0.7, 'HP': 4, 'score': 400},
        'level3': {'move_speed': 2, 'fire_speed': 0.7, 'HP': 5, 'score': 500},
    },
    'tank3': {  # normal-fire-speed/low-move-speed/high-hp
        'level0': {'move_speed': 1, 'fire_speed': 0.8, 'HP': 5, 'score': 200},
        'level1': {'move_speed': 1, 'fire_speed': 0.8, 'HP': 6, 'score': 300},
        'level2': {'move_speed': 1, 'fire_speed': 0.8, 'HP': 7, 'score': 400},
        'level3': {'move_speed': 1, 'fire_speed': 0.8, 'HP': 8, 'score': 500},
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
        [{'enemy_type': 'tank0', 'level': 0}, {'enemy_type': 'tank0', 'level': 0}, {'enemy_type': 'tank0', 'level': 0},
         {'enemy_type': 'tank0', 'level': 0}],
    ]
    ,
    [
        [{'enemy_type': 'tank0', 'level': 0}, {'enemy_type': 'tank0', 'level': 0}, {'enemy_type': 'tank2', 'level': 0}],
        [{'enemy_type': 'tank1', 'level': 3}, {'enemy_type': 'tank3', 'level': 3}, {'enemy_type': 'tank0', 'level': 1}],
        [{'enemy_type': 'tank2', 'level': 2}, {'enemy_type': 'tank0', 'level': 2}, {'enemy_type': 'tank2', 'level': 3}]
    ],
    [
        [{'enemy_type': 'tank0', 'level': 0}, {'enemy_type': 'tank0', 'level': 0}, {'enemy_type': 'tank0', 'level': 0},
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
    ],
    [
        [{'enemy_type': 'tank0', 'level': 0}, {'enemy_type': 'tank2', 'level': 3}, {'enemy_type': 'tank2', 'level': 0}],
        [{'enemy_type': 'tank1', 'level': 3}, {'enemy_type': 'tank3', 'level': 3}, {'enemy_type': 'tank0', 'level': 1}],
        [{'enemy_type': 'tank2', 'level': 2}, {'enemy_type': 'tank0', 'level': 2}, {'enemy_type': 'tank2', 'level': 3}]
    ]
]

Map_data = None
