import subprocess

flask_process = subprocess.Popen(['python', 'Frontend.py'])

timer_process = subprocess.Popen(['python', '-c', 'from Site import timer; timer()'])

flask_process.wait()
timer_process.wait()