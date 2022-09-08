import subprocess


def mhr_pid_lookup():
    return int(subprocess.check_output(['pgrep', 'MonsterHunterRi']))

def mhr_process_is_alive():
    try:
        mhr_pid_lookup()
        return True
    except:
        return False
