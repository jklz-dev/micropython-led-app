from .pixel import pixel
from time import sleep

color_red = (0, 255, 0)
color_green = (255, 0, 0)
color_blue = (0, 0, 255)
color_white = (255, 255, 255)
color_off = (0, 0, 0)

demo_solid_red = {
    'type': 'solid',
    'color': color_red,
}

demo_solid_green = {
    'type': 'solid',
    'color': color_green,
}

demo_solid_blue = {
    'type': 'solid',
    'color': color_blue,
}

demo_flash_red = {
    'type': 'flash',
    'color': color_red,
    'speed': 500,
}

demo_flash_blue = {
    'type': 'flash',
    'color': color_blue,
    'speed': 500,
}

demo_flash_green = {
    'type': 'flash',
    'color': color_green,
    'speed': 500,
}

demo_pattern_one = {
    'type': 'pattern',
    'pattern': [
        color_red,
        color_white,
        color_white,
        color_white,
        color_white,
    ],
}

demo_scroll_one = {
    'type': 'scroll',
    'pattern': [
        color_white,
        color_off,
        color_off,
        color_off,
        color_off,
        color_off,
        color_off,
        color_off,
        color_off,
    ],
    'speed': 500,
}

def display_demo():
    demos = [
        demo_solid_red,
        demo_solid_green,
        demo_solid_blue,
        demo_flash_red,
        demo_flash_green,
        demo_flash_blue,
    ]

    while True:
        for demo in demos:
            pixel.set_display(demo)
            sleep(5)
