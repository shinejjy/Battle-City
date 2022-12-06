from sitepackge import config
import pygame
from sitepackge.load_game.menu import Image, Text, Gif, DisplayButton, Button, Menu, get_text_surface


def load_enemy_menu(bk):
    width, height = bk.get_size()
    unit = width / 17
    my_font = pygame.font.SysFont(['方正粗黑宋简体', 'microsoftsansserif'], int(unit / 2))
    tanks = []
    for i in range(4):
        tank = []
        for j in range(4):
            tank.append(pygame.transform.scale(config.image_dict['tank' + str(i)][j][0][0], (unit, unit)))
        tanks.append(tank)
    tank_help_surface = []
    for index in range(4):
        surface = pygame.Surface((12 * unit, 6 * unit))
        for j in range(4):
            Image(tanks[index][j], (4.5 * unit + j * unit * 2, 0.5 * unit), 1).draw(surface)
        Text("HP", (255, 255, 255), my_font, (0.5 * unit, 2 * unit), 1).draw(surface)
        Text("move_speed", (255, 255, 255), my_font, (0.5 * unit, 3 * unit), 1).draw(surface)
        Text("fire_speed", (255, 255, 255), my_font, (0.5 * unit, 4 * unit), 1).draw(surface)
        Text("score", (255, 255, 255), my_font, (0.5 * unit, 5 * unit), 1).draw(surface)
        for j in range(4):
            Text(str(config.enemy_label['tank' + str(index)]['level' + str(j)]['HP']),
                 (255, 255, 255), my_font, (4.5 * unit + j * unit * 2, 2 * unit), 1).draw(surface)
            Text(str(config.enemy_label['tank' + str(index)]['level' + str(j)]['move_speed']),
                 (255, 255, 255), my_font, (4.5 * unit + j * unit * 2, 3 * unit), 1).draw(surface)
            Text(str(config.enemy_label['tank' + str(index)]['level' + str(j)]['fire_speed']),
                 (255, 255, 255), my_font, (4.5 * unit + j * unit * 2, 4 * unit), 1).draw(surface)
            Text(str(config.enemy_label['tank' + str(index)]['level' + str(j)]['score']),
                 (255, 255, 255), my_font, (4.5 * unit + j * unit * 2, 5 * unit), 1).draw(surface)
        tank_help_surface.append(surface)
    config.enemy_menu = Menu()
    for index in range(4):
        config.enemy_menu.add_display_button(DisplayButton(
            image=tanks[index][3],
            position=(4.5 * unit + (index % 2) * 6 * unit, 3.5 * unit + (index // 2) * 4 * unit),
            scale=2,
            content=Image(
                image=tank_help_surface[index],
                position=(2.5 * unit, 3.5 * unit),
                scale=1
            )
        ))


def load_food_menu(bk):
    # name_gif = ['save', 'aboard', 'speed', 'fire_speed', 'upgrade', 'cover', 'bomb', 'strong', 'minitank', 'heart']
    text_lst = ["Save for another player", "Move on the river for 10 second", "Movement speed increase for 3 second",
                "Fire speed increase for 10 second", "Upgrade (For further particulars, please HELP->Player)",
                "Gain a cover to withstand an attack", "Get a tracking bomb",
                "Can break the Slim Block and the Iron Block for 10 second", "Summon a mini tank", "Gain a HP"]
    width, height = bk.get_size()
    unit = width / 17
    my_font = pygame.font.SysFont(['方正粗黑宋简体', 'microsoftsansserif'], int(unit / 2))
    config.food_menu = Menu()
    for index, gif in enumerate(config.image_dict['food_gif']):
        new_gif = []
        for png in gif:
            new_gif.append(pygame.transform.scale(png, (unit * 17, unit * 13)))
        config.food_menu.add_display_button(
            DisplayButton(
                image=config.image_dict['food'][index],
                position=(1.5 * unit + (index % 4) * unit * 4, 1.5 * unit + (index // 4) * unit * 4),
                scale=2,
                content=[
                    Gif(
                        images=new_gif,
                        position=(1.5 * unit, 1.5 * unit),
                        scale=0.8,
                        mid_width=width / 2,
                        mid_height=height / 2
                    ),
                    Text(
                        text=text_lst[index],
                        color=(255, 0, 0),
                        font=my_font,
                        position=(0, 11.8 * unit),
                        scale=1,
                        mid_width=width / 2
                    )
                ]
            ))


def load_help_menu(bk):
    width, height = bk.get_size()
    unit = width / 17
    my_font = pygame.font.SysFont(['方正粗黑宋简体', 'microsoftsansserif'], int(unit / 2))
    config.help_menu = Menu()
    config.help_menu.add_button(Button(
        text='Food',
        position=(6 * unit, 3 * unit),
        color=(255, 43, 67),
        font=my_font,
        scale=2,
        event='food',
        mid_width=width / 2
    ))
    config.help_menu.add_button(Button(
        text='Player',
        position=(6 * unit, 6 * unit),
        color=(255, 43, 67),
        font=my_font,
        scale=2,
        event='player',
        mid_width=width / 2
    ))
    config.help_menu.add_button(Button(
        text='Enemy',
        position=(6 * unit, 9 * unit),
        color=(255, 43, 67),
        font=my_font,
        scale=2,
        event='enemy',
        mid_width=width / 2
    ))


def load_player_menu(bk):
    width, height = bk.get_size()
    unit = width / 17
    my_font = pygame.font.SysFont(['方正粗黑宋简体', 'microsoftsansserif'], int(unit / 2))
    config.player_menu = Menu()

    players = []
    for index in range(2):
        player = []
        for level in range(4):
            player.append(
                pygame.transform.scale(config.image_dict['player' + str(index + 1)][level][0][0], (unit, unit)))
        players.append(player)
    player_key = [pygame.Surface((4 * unit, 4 * unit)), pygame.Surface((4 * unit, 4 * unit))]
    Text("Move W A S D", (255, 255, 255), my_font, (0.5 * unit, 1 * unit), scale=0.5).draw(player_key[0])
    Text("Fire    J", (255, 255, 255), my_font, (0.5 * unit, 2 * unit), scale=0.5).draw(player_key[0])
    Text("Bomb    Q", (255, 255, 255), my_font, (0.5 * unit, 3 * unit), scale=0.5).draw(player_key[0])
    Text("Move UP LEFT DOWN RIGHT", (255, 255, 255), my_font, (0.5 * unit, 1 * unit), scale=0.5).draw(player_key[1])
    Text("Fire      Enter", (255, 255, 255), my_font, (0.5 * unit, 2 * unit), scale=0.5).draw(player_key[1])
    Text("Bomb       \\", (255, 255, 255), my_font, (0.5 * unit, 3 * unit), scale=0.5).draw(player_key[1])
    tank_help_surface = []
    for index in range(2):
        surface = pygame.Surface((12 * unit, 6 * unit))
        for j in range(4):
            Image(players[index][j], (4.5 * unit + j * unit * 2, 0.5 * unit), 1).draw(surface)
        Text("HP", (255, 255, 255), my_font, (0.5 * unit, 2 * unit), 1).draw(surface)
        Text("move_speed", (255, 255, 255), my_font, (0.5 * unit, 3 * unit), 1).draw(surface)
        Text("fire_speed", (255, 255, 255), my_font, (0.5 * unit, 4 * unit), 1).draw(surface)
        for j in range(4):
            Text(str(config.player_label[j]['HP']),
                 (255, 255, 255), my_font, (4.5 * unit + j * unit * 2, 2 * unit), 1).draw(surface)
            Text(str(config.player_label[j]['move_speed']),
                 (255, 255, 255), my_font, (4.5 * unit + j * unit * 2, 3 * unit), 1).draw(surface)
            Text(str(config.player_label[j]['fire_speed']),
                 (255, 255, 255), my_font, (4.5 * unit + j * unit * 2, 4 * unit), 1).draw(surface)
        tank_help_surface.append(surface)
    for index in range(2):
        config.player_menu.add_display_button(DisplayButton(
            image=players[index][3],
            position=((2.5 + (index % 2) * 8) * unit, 4.5 * unit),
            scale=4,
            content=[Image(
                image=player_key[index],
                position=((2.5 + (index % 2) * 8) * unit, 4.5 * unit),
                scale=1
            )]
        ))
        config.player_menu.add_display_button(DisplayButton(
            image=get_text_surface("upgrade", (255, 0, 0), my_font),
            position=(None, None),
            scale=3,
            content=[Image(
                image=tank_help_surface[index],
                position=(2.5 * unit, 3.5 * unit),
                scale=1
            )],
            mid_width=(4.5 + (index % 2) * 8) * unit,
            mid_height=10.5 * unit
        ))


def load_esc_menu(bk):
    width, height = bk.get_size()
    unit = width / 17
    my_font = pygame.font.SysFont(['方正粗黑宋简体', 'microsoftsansserif'], int(unit / 2))
    config.esc_menu = Menu()
    config.esc_menu.add_button(Button(
        text='RESUME',
        position=(6 * unit, 2 * unit),
        color=(255, 43, 67),
        font=my_font,
        scale=1.5,
        event='resume',
        mid_width=width / 2
    ))
    config.esc_menu.add_button(Button(
        text='HELP',
        position=(6 * unit, 4 * unit),
        color=(255, 43, 67),
        font=my_font,
        scale=1.5,
        event='help',
        mid_width=width / 2
    ))
    config.esc_menu.add_button(Button(
        text='BACK TO GAME',
        position=(6 * unit, 6 * unit),
        color=(255, 43, 67),
        font=my_font,
        scale=1.5,
        event='back to game',
        mid_width=width / 2
    ))
    config.esc_menu.add_button(Button(
        text='QUIT GAME',
        position=(6 * unit, 8 * unit),
        color=(255, 43, 67),
        font=my_font,
        scale=1.5,
        event='quit game',
        mid_width=width / 2
    ))
    config.esc_menu.add_button(Button(
        text='EXIT TO DESKTOP',
        position=(6 * unit, 10 * unit),
        color=(255, 43, 67),
        font=my_font,
        scale=1.5,
        event='exit to desktop',
        mid_width=width / 2
    ))


def load_lose_menu(bk):
    width, height = bk.get_size()
    unit = width / 17
    my_font = pygame.font.SysFont(['方正粗黑宋简体', 'microsoftsansserif'], int(unit / 2))
    config.lose_stage_menu = Menu()
    config.lose_stage_menu.add_button(Button(
        text='Restart',
        position=(6 * unit, 6 * unit),
        color=(39, 165, 176),
        font=my_font,
        scale=3,
        event='restart'
    ))
    config.lose_stage_menu.add_button(Button(
        text='Quit',
        position=(7 * unit, 8 * unit),
        color=(224, 80, 1),
        font=my_font,
        scale=3,
        event='quit'
    ))


def load_main_menu(bk):
    width, height = bk.get_size()
    unit = width / 17
    my_font = pygame.font.SysFont(['方正粗黑宋简体', 'microsoftsansserif'], int(unit / 2))
    # blank0 iron1 river2 ice3 slime4 tree5 brick6
    logo_index = [
        [6, 6, 6, 6, 6, 0, 0, 0, 3, 0, 0, 0, 6, 0, 0, 0, 6, 0, 1, 0, 0, 1, 1],
        [0, 0, 6, 0, 0, 0, 0, 4, 0, 5, 0, 0, 6, 6, 0, 0, 6, 0, 1, 0, 1, 1, 0],
        [0, 0, 6, 0, 0, 0, 5, 5, 5, 5, 5, 0, 6, 0, 6, 0, 6, 0, 1, 1, 1, 0, 0],
        [0, 0, 6, 0, 0, 0, 5, 5, 0, 5, 5, 0, 6, 0, 0, 6, 6, 0, 1, 0, 1, 1, 0],
        [0, 0, 6, 0, 0, 0, 5, 0, 0, 0, 5, 0, 6, 0, 0, 0, 6, 0, 1, 0, 0, 1, 1]
    ]
    logo = pygame.Surface((23 * unit / 2, 5 * unit / 2))
    logo.fill((0, 0, 0))
    iron = pygame.transform.scale(config.image_dict['iron'][0], (unit / 4, unit / 4))
    river = pygame.transform.scale(config.image_dict['river'][0], (unit / 2, unit / 2))
    ice = pygame.transform.scale(config.image_dict['ice'][0], (unit / 2, unit / 2))
    slime = pygame.transform.scale(config.image_dict['slime'][0], (unit / 2, unit / 2))
    tree = pygame.transform.scale(config.image_dict['tree'][0], (unit / 2, unit / 2))
    brick = pygame.transform.scale(config.image_dict['brick'][0], (unit / 4, unit / 4))
    for i in range(5):
        for j in range(23):
            if logo_index[i][j] == 1:
                for x in range(4):
                    logo.blit(iron, (j * unit / 2 + (x % 2) * unit / 4, i * unit / 2 + (x // 2) * unit / 4))
            elif logo_index[i][j] == 2:
                logo.blit(river, (j * unit / 2, i * unit / 2))
            elif logo_index[i][j] == 3:
                logo.blit(river, (j * unit / 2, i * unit / 2))
            elif logo_index[i][j] == 4:
                logo.blit(slime, (j * unit / 2, i * unit / 2))
            elif logo_index[i][j] == 5:
                logo.blit(tree, (j * unit / 2, i * unit / 2))
            elif logo_index[i][j] == 6:
                for x in range(4):
                    logo.blit(brick, (j * unit / 2 + (x % 2) * unit / 4, i * unit / 2 + (x // 2) * unit / 4))
    config.main_menu = Menu()
    config.main_menu.add_image(Image(
        image=logo,
        position=(None, None),
        scale=1,
        mid_width=width / 2,
        mid_height=2.5 * unit
    ))
    config.main_menu.add_button(Button(
        text="SinglePlayer Mode",
        color=(255, 43, 123),
        event='single',
        position=(None, None),
        font=my_font,
        scale=2,
        mid_width=width / 2,
        mid_height=5 * unit
    ))
    config.main_menu.add_button(Button(
        text=" MultiPlayer Mode ",
        color=(255, 43, 123),
        event='multi',
        position=(None, None),
        font=my_font,
        scale=2,
        mid_width=width / 2,
        mid_height=7 * unit
    ))
    config.main_menu.add_button(Button(
        text="            Help            ",
        color=(255, 43, 123),
        event='help',
        position=(None, None),
        font=my_font,
        scale=2,
        mid_width=width / 2,
        mid_height=9 * unit
    ))
    config.main_menu.add_button(Button(
        text="            Quit            ",
        color=(255, 43, 123),
        event='quit',
        position=(None, None),
        font=my_font,
        scale=2,
        mid_width=width / 2,
        mid_height=11 * unit
    ))


def select_level_menu(bk):
    width, height = bk.get_size()
    unit = width / 17
    my_font = pygame.font.SysFont(['方正粗黑宋简体', 'microsoftsansserif'], int(unit))
    config.select_level_menu = Menu()
    config.select_level_menu.add_button(Button(
        text="<",
        position=(None, None),
        color=(255, 255, 255),
        font=my_font,
        scale=1,
        event="<",
        mid_width=5 * unit,
        mid_height=height / 2,
        bk_color=(0, 0, 0),
        effect=False
    ))
    config.select_level_menu.add_button(Button(
        text=">",
        position=(None, None),
        color=(255, 255, 255),
        font=my_font,
        scale=1,
        event=">",
        mid_width=12 * unit,
        mid_height=height / 2,
        bk_color=(0, 0, 0),
        effect=False
    ))
    config.select_level_menu.add_button(Button(
        text="  p l a y  ",
        position=(None, None),
        color=(255, 0, 0),
        font=my_font,
        scale=1,
        event="play",
        mid_width=width / 2,
        mid_height=9 * unit,
        bk_color=(0, 0, 0)
    ))
    config.select_level_menu.add_text(Text(
        text="Level 1",
        position=(None, None),
        color=(255, 255, 255),
        font=my_font,
        scale=1,
        mid_width=width / 2,
        mid_height=height / 2
    ))


def load_menu(bk):
    load_enemy_menu(bk)
    load_help_menu(bk)
    load_food_menu(bk)
    load_esc_menu(bk)
    load_lose_menu(bk)
    load_player_menu(bk)
    load_main_menu(bk)
    select_level_menu(bk)
