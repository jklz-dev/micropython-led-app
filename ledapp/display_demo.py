from .pixel import pixel
import uasyncio

color_value = 125
if color_value != 255:
    color_red = (0, color_value, 0)
    color_green = (color_value, 0, 0)
    color_blue = (0, 0, color_value)
    color_white = (color_value, color_value, color_value)
    color_off = (0, 0, 0)
else:
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
    'speed': 750,
}

demo_flash_blue = {
    'type': 'flash',
    'color': color_blue,
    'speed': 750,
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
    ],
}
demo_pattern_two = {
    'type': 'pattern',
    'pattern': [
        color_red,
        color_white,
        color_green,
        color_white,
        color_white,
        color_blue,
        color_off,
    ],
}

demo_scroll_one = {
    'type': 'scroll',
    'pattern': [
        color_red,
        color_green,
        color_white,
        color_off,
        color_off,
        color_off,
    ],
    'speed': 500,
}
demo_scroll_two = {
    'type': 'scroll',
    'pattern': [
        color_red,
        color_white,
        color_green,
        color_white,
    ],
    'speed': 500,
}


async def run_demo():
    demos = [
        demo_solid_red,
        # demo_solid_green,
        # demo_solid_blue,
        # demo_flash_red,
        # demo_flash_green,
        # demo_flash_blue,
        demo_pattern_one,
        demo_pattern_two,
        demo_scroll_one,
        demo_scroll_two,
    ]

    while True:
        for demo in demos:
            print("Demo: {}".format(demo))
            await pixel.set_display(demo)
            await uasyncio.sleep(3)
        print("end of demo")
