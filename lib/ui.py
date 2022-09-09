import time
import curses


from lib.game import MHRGame


class MHRUI():
    def __init__(self, game):
        self.stdscr = curses.initscr()
        self.init_ui()

        self.start_x = self.stdscr.getmaxyx()[1] // 2
        self.start_y = self.stdscr.getmaxyx()[0] // 2

        self.start_x = 4
        self.start_y = 4

        self.game = game

    def __del__(self):
        curses.endwin()

    def init_ui(self):
        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(0)

    def addstr(self, y, x, text):
        self.stdscr.addstr(
            self.start_y + y,
            self.start_x + x,
            text,
        )

    def update_quest(self):
        self.addstr(0, 0, 'Quest status : ' + self.game.quest.status())

    def update_monsters(self):
        for monster in self.game.monsters:
            if monster.id != 0:
                self.addstr(
                    2 + monster.index,
                    0,
                    f'{monster.index}  {monster.id:4d}  {monster.get_name():25s}  {monster.current_health}/{monster.max_health}  {monster.get_hp():.2f}%'
                )

    def update(self):
        self.stdscr.clear()

        self.stdscr.border()
        self.update_quest()
        if self.game.quest.is_in_quest():
            self.update_monsters()

        self.stdscr.refresh()
        time.sleep(0.3)
