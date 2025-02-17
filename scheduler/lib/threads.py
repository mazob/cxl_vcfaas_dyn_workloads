import logging
import threading
import time
import signal
import os

from types import SimpleNamespace

class ExitCommand(Exception):
    pass

def signal_handler(signal, frame):
    raise ExitCommand()

def thread_function(ns, var_lock):

    print(var_lock)
    print(f'Thready sleepy')
    time.sleep(5)

    with var_lock:
        print(f'THREAD HAS : {ns.var1}')
        print(f'THREAD SLEEP 5')
        time.sleep(5)
        print(f'THREAD MODIFYING')
        ns.var1 = "XXXXXX"
        print(f'THREAD HAS : {ns.var1}')

    print(f'Thready sleepy')
    time.sleep(5)

    with var_lock:
        print(f'THREAD HAS : {ns.var1}')
        print(f'THREAD SLEEP 5')
        time.sleep(5)
        print(f'THREAD MODIFYING')
        ns.var1 = "XXXXXX"
        print(f'THREAD HAS : {ns.var1}')

    os.kill(os.getpid(), signal.SIGUSR1)


if __name__ == "__main__":

    ns = SimpleNamespace()

    ns.var1 = "VAR1INITIALVALUE"
    var_lock = threading.Lock()

    signal.signal(signal.SIGUSR1, signal_handler)

    x = threading.Thread(target=thread_function, args=(ns,var_lock,))
    logging.info("Main    : before running thread")
    x.start()
    print("blurgle")
    time.sleep(1)
    print(var_lock)

    try:
        while True:
            with var_lock:
                print(f'MAIN VAR1 {ns.var1}')
                time.sleep(1)
            ns.var1 = "LASTVALUE"
    except ExitCommand:
        pass
    finally:
        print('finally will still run')