import time
import curses


from lib.game import MHRGame


class MHRUI():
    def __init__(self):
        self.stdscr = curses.initscr()
        self.init_ui()

        self.start_x = self.stdscr.getmaxyx()[1] // 2
        self.start_y = self.stdscr.getmaxyx()[0] // 2

        self.start_x = 4
        self.start_y = 4

        self.game = MHRGame()

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

    def update(self):
        self.stdscr.clear()
        self.stdscr.border()

        self.addstr(0, 0, 'Quest status : ' + self.game.quest.status())

        if self.game.quest.status_code == 2:
            self.addstr(2, 0, f'#{self.game.monsters[0].id} {self.game.monsters[0].get_monster_name():{20}} {self.game.monsters[0].current_health}/{self.game.monsters[0].max_health}')
            self.addstr(3, 0, f'#{self.game.monsters[1].id} {self.game.monsters[1].get_monster_name():{20}} {self.game.monsters[1].current_health}/{self.game.monsters[1].max_health}')
            self.addstr(4, 0, f'#{self.game.monsters[2].id} {self.game.monsters[2].get_monster_name():{20}} {self.game.monsters[2].current_health}/{self.game.monsters[2].max_health}')

        self.stdscr.refresh()
        time.sleep(0.3)
