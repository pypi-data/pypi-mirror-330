import subprocess


def is_windows_cmd():
    # pylint: disable=subprocess-run-check
    proc = subprocess.run("true", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return proc.returncode == 1
