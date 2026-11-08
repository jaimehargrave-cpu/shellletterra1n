# shellletterra1n

A terminal-based falling-letter animation with Python and C implementations. Both versions start directly with the rain—there is no title screen—and let you switch color themes while it runs.

## Python

No third-party packages are required. Python's built-in `curses` module is available by default on most Unix-like systems.

```bash
python3 main.py
```

## C

The C version requires a C compiler and the ncurses development library. On Debian/Ubuntu, install it with `sudo apt install libncurses-dev`.

```bash
cc -Wall -Wextra -O2 c/shellletterra1n.c -lncurses -o shellletterra1n
./shellletterra1n
```

## Controls

- `c` to cycle color themes
- `s` to toggle slow mode
- `r` to reset the rain
- `q` or `Esc` to quit

Themes: Matrix green, cyber cyan, neon magenta, and classic white. Color support depends on your terminal.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
