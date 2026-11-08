# shellletterra1n

A terminal-based falling-letter animation with Python and C implementations. Both versions start directly with the rain—there is no title screen—and let you switch color themes while it runs.

## Python

### Linux and macOS

Python's built-in `curses` module is available by default on most Unix-like systems.

```bash
python3 main.py
```

### Windows Command Prompt

Install the Windows-compatible curses package, then run the app:

```powershell
py -m pip install windows-curses
py main.py
```

Use a recent version of Windows 10 or Windows 11 for the best color support in Command Prompt.

## C

### Linux

The C version requires a C compiler and the ncurses development library. On Debian/Ubuntu, install it with `sudo apt install libncurses-dev`.

```bash
cc -Wall -Wextra -O2 c/shellletterra1n.c -lncurses -o shellletterra1n
./shellletterra1n
```

### Windows Command Prompt

Install a Windows curses implementation such as PDCurses and a compatible C compiler. Compile the source while linking PDCurses; for a MinGW setup where PDCurses is installed as `pdcurses`, for example:

```bat
gcc -Wall -Wextra -O2 c\shellletterra1n.c -lpdcurses -o shellletterra1n.exe
shellletterra1n.exe
```

PDCurses installation paths and library names depend on your toolchain. Use a recent Windows 10 or Windows 11 terminal for color support.

## Controls

- `c` to cycle color themes
- `s` to toggle slow mode
- `r` to reset the rain
- `q` or `Esc` to quit

Themes: Matrix green, cyber cyan, neon magenta, and classic white. Color support depends on your terminal.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
