#include <curses.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define THEME_COUNT 4
#define CHARSET "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#@%&*+=?"

typedef struct {
    int y;
    int speed;
    int trail;
} Column;

typedef struct {
    const char *name;
    short color;
} Theme;

static const Theme themes[THEME_COUNT] = {
    {"Matrix green", COLOR_GREEN},
    {"Cyber cyan", COLOR_CYAN},
    {"Neon magenta", COLOR_MAGENTA},
    {"Classic white", COLOR_WHITE},
};

static int random_between(int low, int high) {
    return low + rand() % (high - low + 1);
}

static void reset_columns(Column *columns, int width, int height) {
    for (int x = 0; x < width; ++x) {
        columns[x].y = random_between(-height, height);
        columns[x].speed = random_between(1, 3);
        columns[x].trail = random_between(6, 18);
    }
}

static void safe_status(const char *text) {
    int height, width;
    getmaxyx(stdscr, height, width);
    if (height > 0 && width > 1) {
        attron(A_REVERSE);
        mvaddnstr(0, 0, text, width - 1);
        attroff(A_REVERSE);
    }
}

static void init_theme_colors(void) {
    if (!has_colors()) return;
    start_color();
    use_default_colors();
    for (short i = 0; i < THEME_COUNT; ++i) {
        init_pair((short)(i + 1), themes[i].color, -1);
    }
}

static void run_rain(void) {
    int height, width;
    getmaxyx(stdscr, height, width);
    if (width < 1) width = 1;

    Column *columns = calloc((size_t)width, sizeof(*columns));
    if (columns == NULL) return;
    reset_columns(columns, width, height);

    int theme = 0;
    bool slow_mode = false;
    nodelay(stdscr, TRUE);
    keypad(stdscr, TRUE);

    for (;;) {
        int new_height, new_width;
        getmaxyx(stdscr, new_height, new_width);
        if (new_width < 1) new_width = 1;
        if (new_width != width) {
            Column *resized = realloc(columns, (size_t)new_width * sizeof(*columns));
            if (resized == NULL) break;
            columns = resized;
            width = new_width;
            height = new_height;
            reset_columns(columns, width, height);
        } else {
            height = new_height;
        }

        erase();
        int key = getch();
        if (key == 'q' || key == 'Q' || key == 27) break;
        if (key == 'c' || key == 'C') theme = (theme + 1) % THEME_COUNT;
        else if (key == 's' || key == 'S') slow_mode = !slow_mode;
        else if (key == 'r' || key == 'R') reset_columns(columns, width, height);

        for (int x = 0; x < width; ++x) {
            int head_y = columns[x].y;
            for (int offset = 0; offset < columns[x].trail; ++offset) {
                int y = head_y - offset;
                if (y >= 0 && y < height) {
                    int attr = has_colors() ? COLOR_PAIR(theme + 1) : A_NORMAL;
                    if (offset == 0) attr |= A_BOLD;
                    else if (offset > columns[x].trail / 2) attr |= A_DIM;
                    attron(attr);
                    mvaddch(y, x, CHARSET[random_between(0, (int)sizeof(CHARSET) - 2)]);
                    attroff(attr);
                }
            }
            columns[x].y += columns[x].speed;
            if (columns[x].y > height + columns[x].trail) {
                columns[x].y = random_between(-height, 0);
                columns[x].speed = random_between(1, 3);
                columns[x].trail = random_between(6, 18);
            }
        }

        char status[128];
        snprintf(status, sizeof(status), " %s | C color  S speed  R reset  Q quit ", themes[theme].name);
        safe_status(status);
        refresh();
        napms(slow_mode ? 80 : 35);
    }
    free(columns);
}

int main(void) {
    srand((unsigned int)time(NULL));
    initscr();
    curs_set(0);
    init_theme_colors();
    run_rain();
    endwin();
    return EXIT_SUCCESS;
}
