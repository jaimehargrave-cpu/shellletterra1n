#!/usr/bin/env python3
"""Terminal letter rain with keyboard-selectable color themes."""

import curses
import random
import time

CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#@%&*+=?<>^|\\/"
THEMES = [
    ("Matrix green", curses.COLOR_GREEN),
    ("Cyber cyan", curses.COLOR_CYAN),
    ("Neon magenta", curses.COLOR_MAGENTA),
    ("Classic white", curses.COLOR_WHITE),
]


def init_colors():
    if not curses.has_colors():
        return
    curses.start_color()
    try:
        curses.use_default_colors()
    except curses.error:
        pass
    for pair, (_, color) in enumerate(THEMES, start=1):
        try:
            curses.init_pair(pair, color, -1)
        except curses.error:
            curses.init_pair(pair, color, curses.COLOR_BLACK)


def make_columns(height, width):
    return [
        {
            "y": random.randint(-height, height),
            "speed": random.randint(1, 3),
            "trail": random.randint(6, 18),
        }
        for _ in range(width)
    ]


def rain(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.nodelay(True)
    init_colors()

    theme = 0
    slow_mode = False
    old_size = None
    columns = []

    while True:
        height, width = stdscr.getmaxyx()
        if (height, width) != old_size:
            columns = make_columns(height, width)
            old_size = (height, width)

        stdscr.erase()
        key = stdscr.getch()
        if key in (ord("q"), ord("Q"), 27):
            break
        if key in (ord("c"), ord("C")):
            theme = (theme + 1) % len(THEMES)
        elif key in (ord("s"), ord("S")):
            slow_mode = not slow_mode
        elif key in (ord("r"), ord("R")):
            columns = make_columns(height, width)

        color = curses.color_pair(theme + 1) if curses.has_colors() else curses.A_NORMAL
        for x, column in enumerate(columns):
            head_y = column["y"]
            for offset in range(column["trail"]):
                y = head_y - offset
                if 0 <= y < height and 0 <= x < width:
                    attr = color | (curses.A_BOLD if offset == 0 else curses.A_DIM if offset > column["trail"] // 2 else 0)
                    try:
                        stdscr.addch(y, x, random.choice(CHARSET), attr)
                    except curses.error:
                        pass

            column["y"] += column["speed"]
            if column["y"] > height + column["trail"]:
                column.update(
                    y=random.randint(-height, 0),
                    speed=random.randint(1, 3),
                    trail=random.randint(6, 18),
                )

        status = f" {THEMES[theme][0]} | C color  S speed  R reset  Q quit "
        try:
            stdscr.addnstr(0, 0, status, max(0, width - 1), curses.A_REVERSE)
        except curses.error:
            pass
        stdscr.refresh()
        time.sleep(0.08 if slow_mode else 0.035)


def main():
    try:
        curses.wrapper(rain)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
