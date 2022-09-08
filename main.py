from lib.ui import MHRUI
from lib.game import MHRGame
from lib.process import mhr_pid_lookup, mhr_process_is_alive


if __name__ == '__main__':
    try:
        pid = mhr_pid_lookup()
    except:
        print('MHR process not found !')
        exit()

    game = MHRGame()
    ui   = MHRUI()

    while mhr_process_is_alive():
        game.quest.update()

        if game.quest.status_code == 2:
            for monster in game.monsters:
                monster.update()

        ui.update()
