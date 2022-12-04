from sitepackge import config
import pygame
from sitepackge.menu import Image, Text, Gif, DisplayButton, Button, Menu


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
    width, height = bk.get_size()
    unit = width / 17
    config.food_menu = Menu()
    for index, gif in enumerate(config.image_dict['food_gif']):
        config.food_menu.add_display_button(DisplayButton(
            image=config.image_dict['food'][index],
            position=(1.5 * unit + (index % 4) * unit * 4, 1.5 * unit + (index // 4) * unit * 4),
            scale=2,
            content=Gif(
                images=gif,
                position=(1.5 * unit, 1.5 * unit),
                scale=0.5
            )
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
        middle_width=17 * unit
    ))
    config.help_menu.add_button(Button(
        text='Player',
        position=(6 * unit, 6 * unit),
        color=(255, 43, 67),
        font=my_font,
        scale=2,
        event='player',
        middle_width=17 * unit
    ))
    config.help_menu.add_button(Button(
        text='Enemy',
        position=(6 * unit, 9 * unit),
        color=(255, 43, 67),
        font=my_font,
        scale=2,
        event='enemy',
        middle_width=17 * unit
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
        middle_width=17 * unit
    ))
    config.esc_menu.add_button(Button(
        text='HELP',
        position=(6 * unit, 4 * unit),
        color=(255, 43, 67),
        font=my_font,
        scale=1.5,
        event='help',
        middle_width=17 * unit
    ))
    config.esc_menu.add_button(Button(
        text='BACK TO GAME',
        position=(6 * unit, 6 * unit),
        color=(255, 43, 67),
        font=my_font,
        scale=1.5,
        event='back to game',
        middle_width=17 * unit
    ))
    config.esc_menu.add_button(Button(
        text='QUIT GAME',
        position=(6 * unit, 8 * unit),
        color=(255, 43, 67),
        font=my_font,
        scale=1.5,
        event='quit game',
        middle_width=17 * unit
    ))
    config.esc_menu.add_button(Button(
        text='EXIT TO DESKTOP',
        position=(6 * unit, 10 * unit),
        color=(255, 43, 67),
        font=my_font,
        scale=1.5,
        event='exit to desktop',
        middle_width=17 * unit
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


def load_menu(bk):
    load_enemy_menu(bk)
    load_help_menu(bk)
    load_food_menu(bk)
    load_esc_menu(bk)
    load_lose_menu(bk)
