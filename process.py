# Keith Scannell
# 120335743
class Process:
        def __init__(self, pid, time, priority, IO, IO_time):
            self._pid = pid
            self._time = time
            self._priority = priority
            self._IO = IO
            self._state = "Ready"
            self._IO_time = IO_time

        def __str__(self):
            return ("Process: %s, Burst time: %s, Priority level: %s, I/0: %s" % (self._pid, self._time, self._priority, self._IO ) )


if __name__ == "__main__":
    
    def testProcess():
        process = Process("p1",5,1,False)
        print(process)
        
    testProcess()