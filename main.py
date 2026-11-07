#!/usr/bin/env python3
import curses
import random
import time

# Characters used in the falling rain effect.
CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#@%&*+=?"


def init_colors():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_BLACK, -1)


def rain(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)
    init_colors()

    slow_mode = False
    columns = []

    def reset_columns():
        nonlocal columns
        h, w = stdscr.getmaxyx()
        columns = [
            {
                "x": x,
                "y": random.randint(-h, h),
                "speed": random.randint(1, 3),
                "trail": random.randint(7, 18),
                "chars": [random.choice(CHARSET) for _ in range(random.randint(4, 12))],
            }
            for x in range(w)
        ]

    reset_columns()

    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()

        ch = stdscr.getch()
        if ch in (ord("q"), ord("Q"), 27):
            break
        if ch in (ord("s"), ord("S")):
            slow_mode = not slow_mode
        if ch in (ord("r"), ord("R")):
            reset_columns()

        for col in columns:
            x = col["x"]
            y = col["y"]
            trail = col["trail"]

            # Draw trail.
            for offset in range(trail):
                cy = y - offset
                if 0 <= cy < h and 0 <= x < w:
                    if offset == 0:
                        attr = curses.color_pair(1) | curses.A_BOLD
                        stdscr.addstr(cy, x, random.choice(CHARSET), attr)
                    else:
                        attr = curses.color_pair(1)
                        stdscr.addstr(cy, x, random.choice(CHARSET), attr)

            # Advance column.
            col["y"] += col["speed"]
            if col["y"] > h + trail:
                col["y"] = random.randint(-h, 0)
                col["speed"] = random.randint(1, 3)
                col["trail"] = random.randint(7, 18)

        stdscr.refresh()
        time.sleep(0.03 if not slow_mode else 0.08)


def main():
    try:
        curses.wrapper(rain)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
