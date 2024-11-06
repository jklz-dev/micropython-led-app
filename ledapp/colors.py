
class WeatherGround(dict):
    grass: tuple[int, int, int]
    snow: tuple[int, int, int]


class WeatherSky(dict):
    day: tuple[int, int, int]
    night: tuple[int, int, int]
    cloud: tuple[int, int, int]
    sun: tuple[int, int, int]
    moon: tuple[int, int, int]


class WeatherForecast(dict):
    rain: tuple[int, int, int]
    snow: tuple[int, int, int]
    wind: tuple[int, int, int]
    fog: tuple[int, int, int]


class Colors(dict[str, tuple[int, int, int] | None]):
    # white
    white = (255, 255, 255)
    snow = (255, 250, 250)
    honeydew = (240, 255, 240)
    mintcream = (245, 255, 250)
    azure = (240, 255, 255)
    aliceblue = (240, 248, 255)
    ghostwhite = (248, 248, 255)
    whitesmoke = (245, 245, 245)
    seashell = (255, 245, 238)
    beige = (245, 245, 220)
    oldlace = (253, 245, 230)
    floralwhite = (255, 250, 240)
    ivory = (255, 255, 240)
    antiquewhite = (250, 235, 215)
    linen = (250, 240, 230)
    lavenderblush = (255, 240, 245)
    mistyrose = (255, 228, 225)
    navajowhite = (255, 222, 173)
    # cyan
    lightcyan = (224, 255, 255)
    cyan = (0, 255, 255)
    aqua = (0, 255, 255)
    aquamarine = (127, 255, 212)
    mediumaquamarine = (102, 205, 170)
    paleturquoise = (175, 238, 238)
    turquoise = (64, 224, 208)
    mediumturquoise = (72, 209, 204)
    darkturquoise = (0, 206, 209)
    lightseagreen = (32, 178, 170)
    cadetblue = (95, 158, 160)
    darkcyan = (0, 139, 139)
    teal = (0, 128, 128)
    # blue https://www.rapidtables.com/web/color/blue-color.html
    lavender = (230, 230, 250)
    powderblue = (176, 224, 230)
    lightblue = (173, 216, 230)
    lightskyblue = (135, 206, 250)
    skyblue = (135, 206, 235)
    deepskyblue = (0, 191, 255)
    lightsteelblue = (176, 196, 222)
    dodgerblue = (30, 144, 255)
    cornflowerblue = (100, 149, 237)
    steelblue = (70, 130, 180)
    mediumslateblue = (123, 104, 238)
    slateblue = (106, 90, 205)
    darkslateblue = (72, 61, 139)
    royalblue = (65, 105, 225)
    blue = (0, 0, 255)
    mediumblue = (0, 0, 205)
    darkblue = (0, 0, 139)
    navy = (0, 0, 128)
    midnightblue = (25, 25, 112)
    blueviolet = (138, 43, 226)
    indigo = (75, 0, 130)
    # green
    lawngreen = (124, 252, 0)
    chartreuse = (127, 255, 0)
    limegreen = (50, 205, 50)
    lime = (0, 255, 0)
    forestgreen = (34, 139, 34)
    green = (0, 128, 0)
    darkgreen = (0, 100, 0)
    greenyellow = (173, 255, 47)
    yellowgreen = (154, 205, 50)
    springgreen = (0, 255, 127)
    mediumspringgreen = (0, 250, 154)
    lightgreen = (144, 238, 144)
    palegreen = (152, 251, 152)
    darkseagreen = (143, 188, 143)
    mediumseagreen = (60, 179, 113)
    seagreen = (46, 139, 87)
    olive = (128, 128, 0)
    darkolivegreen = (85, 107, 47)
    olivedrab = (107, 142, 35)
    # yellow
    lightyellow = (255, 255, 224)
    lemonchiffon = (255, 250, 205)
    lightgoldenrodyellow = (250, 250, 210)
    papayawhip = (255, 239, 213)
    moccasin = (255, 228, 181)
    peachpuff = (255, 218, 185)
    palegoldenrod = (238, 232, 170)
    khaki = (240, 230, 140)
    darkkhaki = (189, 183, 107)
    yellow = (255, 255, 0)
    # grey
    gainsboro = (220, 220, 220)
    lightgrey = (211, 211, 211)
    silver = (192, 192, 192)
    darkgrey = (169, 169, 169)
    grey = (128, 128, 128)
    dimgrey = (105, 105, 105)
    lightslategrey = (119, 136, 153)
    slategrey = (112, 128, 144)
    darkslategrey = (47, 79, 79)
    black = (0, 0, 0)
    # gold
    # azure = ()
    # azure = ()
    # azure = ()
    # azure = ()
    # azure = ()
    # azure = ()
    # azure = ()
    # azure = ()
    # azure = ()
    # azure = ()
    # azure = ()
    # azure = ()
    # azure = ()
    # azure = ()
    # azure = ()
    # azure = ()


class WeatherColors(object):
    ground: WeatherGround = {
        "grass": Colors.forestgreen,
        "snow": Colors.whitesmoke,
    }
    sky: WeatherSky = {
        "day": Colors.deepskyblue,
        "night": Colors.midnightblue,
        "cloud": Colors.dimgrey,
        "sun": Colors.lightgoldenrodyellow,
        "moon": Colors.palegoldenrod,
    }
    forcast: WeatherForecast = {
        "rain": Colors.dodgerblue,
        "snow": Colors.whitesmoke,
    }
