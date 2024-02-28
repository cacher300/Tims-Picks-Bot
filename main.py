import subprocess
import sys

flask_process = subprocess.Popen([sys.executable, 'Frontend.py'])

timer_process = subprocess.Popen([sys.executable, '-c', 'from Site import timer; timer()'])

flask_process.wait()
timer_process.wait()