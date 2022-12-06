import pygame
from sitepackge import config

unit = 68
image_unit = 64


# 载入敌方坦克贴图
def load_tank_image(sc):
    print("正在加载敌方坦克图标......")
    for o in range(4):
        tank_dict = {}
        for y in range(4):  # 每种坦克四个等级  config.image_dict['tank0'][0][0][0] 表示第1种坦克第1个等级朝上方向的第1张图片
            tank_lst = []
            for x in range(4):  # 每个等级的坦克四个方向
                tank_lst.append([sc.subsurface((x * 2 * unit + o * 8 * unit + 2, y * unit + 2,
                                                image_unit, image_unit)),
                                 sc.subsurface(((x * 2 + 1) * unit + o * 8 * unit + 2, y * unit + 2,
                                                image_unit, image_unit))])
            tank_dict[y] = tank_lst
        config.image_dict['tank' + str(o)] = tank_dict
    print('我方坦克图标加载成功')


# 载入玩家坦克贴图
def load_player_tank_image(sc):
    print("正在加载我方坦克图标......")
    player1 = []
    player2 = []
    for o in range(4):
        level = []
        for x in range(4):
            level.append([
                sc.subsurface((x * 2 * unit + o * 8 * unit + 2, 11 * unit + 2, image_unit, image_unit)),
                sc.subsurface(((x * 2 + 1) * unit + o * 8 * unit + 2, 11 * unit + 2, image_unit, image_unit))
            ])
        player1.append(level)
    for o in range(4):
        level = []
        for x in range(4):
            level.append([
                sc.subsurface((x * 2 * unit + o * 8 * unit + 2, 12 * unit + 2, image_unit, image_unit)),
                sc.subsurface(((x * 2 + 1) * unit + o * 8 * unit + 2, 12 * unit + 2, image_unit, image_unit))
            ])
        player2.append(level)
    config.image_dict['player1'] = player1
    config.image_dict['player2'] = player2
    print('敌方坦克图标加载成功')


# 载入小坦克贴图
def load_mini_tank_image(sc):
    print("正在加载迷你坦克图标......")
    mini_tank = []
    for x in range(4):
        mini_tank.append([
            pygame.transform.scale(sc.subsurface((x * 2 * unit + 2, 8 * unit + 2, image_unit, image_unit)),
                                   (32, 32)),
            pygame.transform.scale(sc.subsurface(((x * 2 + 1) * unit + 2, 8 * unit + 2, image_unit, image_unit)),
                                   (32, 32))
        ])
    config.image_dict['mini_tank'] = mini_tank
    print('迷你坦克图标加载成功')


# 载入河流/砖块/铁块/冰块/树丛/史莱姆贴纸
def load_wall_image(sc):
    print("正在加载墙体图标......")
    river1 = sc.subsurface((0 * unit + 2, 7 * unit + 2, image_unit, image_unit))
    river2 = sc.subsurface((1 * unit + 2, 7 * unit + 2, image_unit, image_unit))
    config.image_dict['river'] = [river1, river2]
    brick = sc.subsurface((18 * unit + 2, 5 * unit + 2, image_unit / 2, image_unit / 2))
    config.image_dict['brick'] = [brick]
    iron = sc.subsurface((0 * unit + 2, 6 * unit + 2, image_unit / 2, image_unit / 2))
    config.image_dict['iron'] = [iron]
    ice = sc.subsurface((9 * unit + 2, 7 * unit + 2, image_unit, image_unit))
    ice.set_alpha(200)
    for x in range(64):
        for y in range(64):
            if ice.get_at((x, y)) == (188, 188, 188):
                ice.set_at((x, y), (133, 242, 255))
            elif ice.get_at((x, y)) == (127, 127, 127):
                ice.set_at((x, y), (28, 129, 255))
    config.image_dict['ice'] = [ice]
    tree = sc.subsurface((4 * unit + 2, 7 * unit + 2, image_unit, image_unit))
    config.image_dict['tree'] = [tree]
    slime = pygame.image.load("./image/slime.png")
    slime = pygame.transform.scale(slime, (64, 64))
    config.image_dict['slime'] = [slime]
    print('墙体图标加载成功')


# 载入游戏结束贴图
def load_gameover_image(sc):
    print("正在加载游戏失败图标......")
    gameover = sc.subsurface((4 * unit + 2, 4 * unit + 2, image_unit * 2, image_unit))
    for x in range(image_unit * 2):
        for y in range(image_unit):
            if gameover.get_at((x, y)) == (244, 80, 1):
                gameover.set_at((x, y), (255, 255, 255))
    config.image_dict['gameover'] = [gameover]
    print('游戏结束图标加载成功')


# 载入食物贴图
def load_food_image(sc):
    print("正在加载食物图标......")
    food1 = sc.subsurface((12 * unit + 2, 6 * unit + 2, image_unit, image_unit))
    food2 = sc.subsurface((13 * unit + 2, 6 * unit + 2, image_unit, image_unit))
    food3 = sc.subsurface((14 * unit + 2, 6 * unit + 2, image_unit, image_unit))
    food4 = sc.subsurface((15 * unit + 2, 6 * unit + 2, image_unit, image_unit))
    food5 = sc.subsurface((16 * unit + 2, 6 * unit + 2, image_unit, image_unit))
    food6 = sc.subsurface((18 * unit + 2, 6 * unit + 2, image_unit, image_unit))
    food7 = sc.subsurface((20 * unit + 2, 6 * unit + 2, image_unit, image_unit))
    food8 = sc.subsurface((22 * unit + 2, 6 * unit + 2, image_unit, image_unit))
    food9 = sc.subsurface((24 * unit + 2, 6 * unit + 2, image_unit, image_unit))
    food10 = sc.subsurface((27 * unit + 2, 4 * unit + 2, image_unit, image_unit))
    config.image_dict['food'] = [food1, food2, food3, food4, food5, food6, food7, food8, food9, food10]
    print('食物图标加载成功')


# 载入敌人出生点贴图
def load_start_point_image(sc):
    print("正在加载敌方坦克出生点图标......")
    point_lst = []
    for i in range(16, 20):
        point_lst.append(sc.subsurface((i * unit + 2, 4 * unit + 2, image_unit, image_unit)))
    config.image_dict['start_point'] = point_lst[::-1]
    print('敌方坦克出生点图标加载成功')


# 载入爆炸效果贴图
def load_boom_image(sc):
    print("正在加载爆炸效果图标......")
    boom1 = sc.subsurface((20 * unit + 2, 4 * unit + 2, image_unit, image_unit))
    boom2 = sc.subsurface((21 * unit + 2, 4 * unit + 2, image_unit, image_unit))
    boom3 = sc.subsurface((22 * unit + 2, 4 * unit + 2, image_unit, image_unit))
    boom4 = sc.subsurface((23 * unit + 2, 4 * unit + 2, image_unit * 2, image_unit * 2))
    boom5 = sc.subsurface((25 * unit + 2, 4 * unit + 2, image_unit * 2, image_unit * 2))
    config.image_dict['boom'] = [boom1, boom2, boom3, boom4, boom5]
    print('爆炸效果图标加载成功')


# 载入空白贴图
def load_blank_image(sc):
    print("正在加载空白格图标......")
    blank = sc.subsurface((0 * unit + 2, 4 * unit + 2, image_unit, image_unit))
    blank_bullet1 = sc.subsurface((0 * unit + 2, 4 * unit + 2, 16, 20))
    blank_bullet2 = sc.subsurface((0 * unit + 2, 4 * unit + 2, 20, 16))
    blank_boom = sc.subsurface((16 * unit + 2, 9 * unit + 2, image_unit * 2, image_unit * 2))
    blank_mini_tank = sc.subsurface((0 * unit + 2, 4 * unit + 2, image_unit / 2, image_unit / 2))
    config.image_dict['blank'] = [blank, blank_bullet1, blank_bullet2, blank_boom, blank_mini_tank]
    print('空白格图标加载成功')


# 载入子弹贴图
def load_bullet_image(sc):
    print("正在加载子弹图标......")
    bullet1 = sc.subsurface((0 * unit, 5 * unit, 16, 20))
    bullet2 = sc.subsurface((10 / 34 * unit, 5 * unit, 16, 20))
    bullet3 = sc.subsurface((0 * unit, 5 * unit + 10 / 34 * unit, 20, 16))
    bullet4 = sc.subsurface((10 / 34 * unit, 5 * unit + 10 / 34 * unit, 20, 16))
    tracking_bomb = bullet4.copy()
    for x in range(20):
        for y in range(16):
            if tracking_bomb.get_at((x, y)) == (188, 188, 188):
                tracking_bomb.set_at((x, y), (255, 0, 0))
    tracking_bomb = pygame.transform.scale(tracking_bomb, (40, 32))

    config.image_dict['bullet'] = [bullet1, bullet4, bullet2, bullet3]
    config.image_dict['tracking_bomb'] = [tracking_bomb]
    print('子弹图标加载成功')


# 载入我方基地贴图
def load_base_image(sc):
    print("正在加载基地图标......")
    base = sc.subsurface((19 * unit + 2, 5 * unit + 2, image_unit, image_unit))
    config.image_dict['base'] = [base]
    print('基地图标加载成功')


# 载入图标贴图
def load_icon_image(sc):
    print("正在加载UI图标......")
    enemy_icon = sc.subsurface((1 * unit + 20, 4 * unit + 20, 28, 28))
    config.image_dict['enemy_icon'] = [enemy_icon]
    ip = sc.subsurface((2 * unit + 2, 4 * unit + 2, image_unit, image_unit))
    iip = sc.subsurface((3 * unit + 2, 4 * unit + 2, image_unit, image_unit))
    config.image_dict['player_icon'] = [ip, iip]
    heart = sc.subsurface((22 * unit + 12, 5 * unit + 16, 44, 36))
    config.image_dict['heart'] = [heart]
    bomb = sc.subsurface((29 * unit + 2, 6 * unit + 2, image_unit, image_unit))
    config.image_dict['bomb'] = [bomb]
    print('UI图标加载成功')


# 载入分数贴图
def load_score_image(sc):
    print("正在加载分数图标......")
    score = []
    for i in range(27, 32):
        score.append(sc.subsurface((i * unit + 2, 5 * unit + 2, image_unit, image_unit)))
    config.image_dict['score'] = score
    print('分数图标加载成功')


# 载入坦克保护罩贴图
def load_cover_image(sc):
    print("正在加载保护罩图标......")
    cover0 = sc.subsurface((10 * unit + 2, 7 * unit + 2, image_unit, image_unit))
    cover1 = sc.subsurface((11 * unit + 2, 7 * unit + 2, image_unit, image_unit))
    cover2 = sc.subsurface((12 * unit + 2, 7 * unit + 2, image_unit, image_unit))
    cover3 = sc.subsurface((13 * unit + 2, 7 * unit + 2, image_unit, image_unit))
    cover4 = sc.subsurface((15 * unit + 2, 7 * unit + 2, image_unit, image_unit))
    config.image_dict['cover'] = [cover0, cover1, cover2, cover3, cover4]
    print('保护罩图标加载成功')


def load_food_gif():
    print("正在加载食物效果动图......")
    food_gif = []
    name_gif = ['save', 'aboard', 'speed', 'fire_speed', 'upgrade', 'cover', 'bomb', 'strong', 'minitank', 'heart']
    n_gif = [16, 94, 76, 109, 151, 28, 94, 205, 46, 19]
    for i in range(10):
        certain_gif = []
        for j in range(0, n_gif[i], 3):
            certain_gif.append(pygame.image.load("./image/food/" + name_gif[i] + f"_gif/{j}.png"))
        food_gif.append(certain_gif)
    config.image_dict['food_gif'] = food_gif
    print('食物效果动图加载成功')


# 载入贴图总函数
def load_image():
    sc = pygame.image.load("./image/tank_elements.png")
    sc = pygame.transform.scale(sc, (2176, 884))
    load_tank_image(sc)
    load_wall_image(sc)
    load_gameover_image(sc)
    load_start_point_image(sc)
    load_food_image(sc)
    load_boom_image(sc)
    load_blank_image(sc)
    load_bullet_image(sc)
    load_base_image(sc)
    load_icon_image(sc)
    load_score_image(sc)
    load_cover_image(sc)
    load_player_tank_image(sc)
    load_mini_tank_image(sc)
    load_food_gif()


def load_audio():
    config.audio_dict['fire'] = './audios/fire.mp3'
    config.audio_dict['boom'] = './audios/boom.mp3'
    config.audio_dict['button'] = './audios/button.mp3'
    config.audio_dict['iron_break'] = './audios/iron_break.mp3'
    config.audio_dict['lose'] = './audios/lose.mp3'
    config.audio_dict['tree'] = './audios/tree.mp3'
    config.audio_dict['win'] = './audios/win.mp3'
