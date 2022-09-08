import time
import curses


quest_status = {
    0 : 'In village',
    1 : 'Loading quest',
    2 : 'In Quest',
    3 : 'Victory',
    4 : 'Defeat',
    5 : 'Quest reset',
    6 : 'Quest time out',
    7 : 'Exit quest',
}


class MHRUI():
    def __init__(self):
        self.stdscr = curses.initscr()
        self.init_ui()

        self.start_x = self.stdscr.getmaxyx()[1] // 2
        self.start_y = self.stdscr.getmaxyx()[0] // 2

    def __del__(self):
        curses.endwin()

    def init_ui(self):
        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(0)

    def update(self, game):
        self.stdscr.clear()
        self.stdscr.border()

        text = 'Quest status : ' + quest_status[game['quest_status']]

        self.stdscr.addstr(
            self.start_y,
            self.start_x - len(text) // 2,
            text,
        )

        self.stdscr.refresh()
        time.sleep(0.3)
