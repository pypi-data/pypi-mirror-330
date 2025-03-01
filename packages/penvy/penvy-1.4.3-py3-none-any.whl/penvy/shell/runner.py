# pylint: disable=dangerous-default-value,consider-using-with
import io
import os
import sys
import codecs
import locale
import subprocess


def run_and_read_line(command: str, cwd: str = os.getcwd(), env: dict = os.environ, shell=False):
    proc = subprocess.Popen(command, cwd=cwd, env=env, stdout=subprocess.PIPE, shell=shell)
    line = io.TextIOWrapper(proc.stdout, encoding="utf-8").read().rstrip()

    if not line:
        raise Exception(f"No output returned to stdout for: {command}")

    return line


def run_shell_command(command: str, cwd: str = os.getcwd(), env: dict = os.environ, shell=False):
    proc = subprocess.Popen(command, cwd=cwd, env=env, shell=shell)
    stdout, stderr = proc.communicate()

    if proc.returncode != 0:
        raise Exception(f"Shell command failed with code: {proc.returncode}\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}")


def run_with_live_output(command: str, cwd: str = os.getcwd(), env: dict = os.environ, shell=False):
    proc = subprocess.Popen(command, cwd=cwd, env=env, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    decoder = codecs.getincrementaldecoder(locale.getpreferredencoding())()

    for bytes_chunk in iter(proc.stdout.readline, b""):
        decoded_chunk = decoder.decode(bytes_chunk)
        sys.stdout.write(decoded_chunk)
        sys.stdout.flush()

    proc.communicate()

    if proc.returncode != 0:
        raise Exception(f"Shell command failed with code: {proc.returncode}")
