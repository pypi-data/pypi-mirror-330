import time
import threading
from .logging import log

class Solnir:
    _exit_flag = False

    @staticmethod
    def exit():
        Solnir._exit_flag = True
        log("Exiting solnir main loop.")

    @staticmethod
    def main(func):
        def wrapper():
            log("Starting solnir main loop.")
            while not Solnir._exit_flag:
                func()
            log("solnir main loop has stopped.")
        return wrapper

def exit():
    Solnir.exit()

def run(func):
    main_thread = threading.Thread(target=func)
    main_thread.start()
    main_thread.join()

def sleep(t):
    time.sleep(t)