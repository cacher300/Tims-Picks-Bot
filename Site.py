from Text import texts
import time
from model import main


def timer():
    while True:
        main()
        texts()
        time.sleep(1800)
