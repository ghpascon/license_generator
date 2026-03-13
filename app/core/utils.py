import os
import subprocess
import sys


def restart_application():
	subprocess.Popen([sys.executable] + sys.argv)
	os._exit(0)


def exit_application():
	os._exit(0)
