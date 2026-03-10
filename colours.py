def _color(red, green):
    return red + (green << 4)

COLOURS = {
    "black": _color(0, 0),

    "red_low": _color(1, 0),
    "red_med": _color(2, 0),
    "red_max": _color(3, 0),

    "green_low": _color(0, 1),
    "green_med": _color(0, 2),
    "green_max": _color(0, 3),

    "yellow_low": _color(1, 1),
    "yellow_med": _color(2, 2),
    "yellow_max": _color(3, 3),
}
