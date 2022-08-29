# Keith Scannell
# 120335743
class Q:
        def __init__(self, timeSlice, priority):
            self._body = []
            self._timeSlice = timeSlice
            self._priority = priority
            self._state = "Ready"

        def __str__(self):
            retStr = "| "
            if len(self._body) == 0:
                return " Is empty"
            else:
                for i in self._body:
                    retStr += "%s, %sms" %(i._pid,i._time)
                    retStr += " | "
                return retStr


if __name__ == "__main__":
    
    def testQ():
        q = q("p1",4,2)
        print(q)
        
    testQ()

   