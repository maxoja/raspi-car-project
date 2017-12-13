import threading
from time import sleep

class WhileTrueThread(threading.Thread) :
    def __init__(self, interval = 0) :
        threading.Thread.__init__(self)
        self.__interval = interval
        self.__stop = False

    def stop(self) :
        self.__stop = True
        
    def _prepare(self) :
        pass

    def _loop(self) :
        pass

    def _end(self) :
        pass

    def run(self) :
        
        self._prepare()
        
        while not self.__stop :
            self._loop()
            sleep(self.__interval)

        self._end()
            
            
