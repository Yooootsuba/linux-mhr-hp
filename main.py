from lib.ui import MHRUI
from lib.memory import MHRMemory
from lib.process import MHRProcess


if __name__ == '__main__':
    try:
        process = MHRProcess()
        pid = process.get_pid()
    except:
        print('MHR process not found !')
        exit()

    memory = MHRMemory(pid)
    ui = MHRUI()

    while process.is_alive():
        game = memory.update()
        ui.update(game)
