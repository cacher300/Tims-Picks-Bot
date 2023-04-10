import subprocess

flask_process = subprocess.Popen(['python', 'Frontend.py'])

    # Run timer function as a separate process
timer_process = subprocess.Popen(['python', '-c', 'from Site import timer; timer()'])

    # Wait for both processes to complete
flask_process.wait()
timer_process.wait()