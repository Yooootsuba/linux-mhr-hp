import subprocess


class MHRProcess():
    def get_pid(self):
        return int(subprocess.check_output(['pgrep', 'MonsterHunterRi']))

    def is_alive(self):
        try:
            self.get_pid()
            return True
        except:
            return False
