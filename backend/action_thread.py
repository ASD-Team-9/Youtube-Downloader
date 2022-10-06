"The main threading class"
import threading
import backend.constant_variables as CONST

class ActionThread:
    """
    A simple class controlling the threads.
    Every instance of this class will auto start but depending
    on the v.threads, it may not activate at all.
    """
    def __init__(self, thread_name, thread_delegate) -> None:
        def thread_action():
            self.thread_delegate()
            CONST.THREADS[self.name] = None

        if CONST.THREADS[thread_name] is None:
            self.name = thread_name
            self.thread_delegate = thread_delegate
            CONST.THREADS[thread_name] = threading.Thread(target=thread_action)
            CONST.THREADS[thread_name].start()
