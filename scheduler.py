# Keith Scannell
# 120335743
from process import Process
from queue_ import Q
class Scheduler:
    def __init__(self,quantum):
        """ Initaises queues """
        self._q0 = Q((2**0)*(quantum),0) 
        self._q1 = Q((2**1)*quantum,1)
        self._q2 = Q((2**2)*quantum,2)
        self._q3 = Q((2**3)*quantum,3)
        self._q4 = Q((2**4)*quantum,4)
        self._q5 = Q((2**5)*quantum,5)
        self._q6 = Q((2**6)*quantum,6)
        self._q7 = Q((2**7)*quantum,7) 
        self._blockedQ = []
        self._queues = [self._q0,self._q1,self._q2,self._q3,self._q4,self._q5,self._q6,self._q7]
        self._time = 0
        #self._totalP = 0

    def __str__(self):
        retStr = ""
        queue_num =["q7","q6","q5","q4","q3","q2","q1","q0"]
        for q in self._queues:
            
            retStr += "%s: %s \n" %  (queue_num[-1],q)
            queue_num.pop(-1)
        if len(self._blockedQ) >0 :
            retStr += "Blocked: "
            for p in self._blockedQ:
                 
                retStr +="%s, %sms \n" % (p._pid,p._IO_time )
        
        retStr += "Time elapsed %s\n#####################################\n"% self._time
        return retStr 
        
    def enqueue(self,process):
        """ Adds a process to the queue."""


        if process._priority < len(self._queues):      
            q = self._queues[process._priority]
            q._body.append(process)
        else:
            print("Queue not found ")

    def dequeue(self,priority):
        """ Removes process from the queue and returns the process."""     


        q = self._queues[priority]
        if len(q._body) > 0:
            process = q._body[0]
            q._body.pop(0)
            return process
        else:
            print("Queue is empty")

    def mlfq(self):
        """ Multi-level feedback queue """


        print(self)
        i = 0 
        while i < len(self._queues):
            q = self._queues[i]
            if len(q._body) == 0: 
                i += 1   # queue is empty, goes to lower priority
            else:
                p = q._body[0]
                
                if p._time <= q._timeSlice: 
                    self._terminateProcess(q,p)
                    i = 0
                else:
                    if p._priority < 7:
                        self._priorityDown(q,p)
                        i = 0
                    else:
                        self._roundRobin(q,p)
                        i = 0
        print("Idle process takes over\nSleep state: On")

            
    def _checkIO(self,q,p):
        """ checks process for I/O operation,
            if I/O operation is triggered, process is blocked and leaves the queue and goes to blocked queue """


        if p._IO == None:
            return
        else:
            if p._IO <= 0 and p._state == "Ready": 
                p._state = "Blocked"
                print("~~~~~~~ %s is Blocked ~~~~~~~" % p._pid)
                self._blockedQ.append(self.dequeue(q._priority))

    def _unblock(self, p):
        """ checks blocked processes if they are finished I/O operation.
        If so, process state is ready, leaves blocked queue and returns to a boosted priority   """


        if len(self._blockedQ) > 0:
            if p._IO_time <= 0:         #  
                p._priority -= 2        # Boosts priority 
                if p._priority < 1:     #
                    p._priority = 1     #
                p._state = "Ready"
                print("~~~~~~~~ %s is Ready ~~~~~~~~\n~~~~~ %s Boosted to Queue %s ~~~~" % (p._pid, p._pid,p._priority))
                self.enqueue(p)
                self._blockedQ.pop(0)
               
    def _priorityDown(self,q,p):
        """ gives process time in the CPU and then lowers its priority """


        print("%s takes control of CPU"% p._pid)
        print("Time slice: %s" % q._timeSlice)
        p._time -= q._timeSlice
        self._time += q._timeSlice
        if p._IO is not None and p._IO > 0:
            p._IO -= q._timeSlice
            self._checkIO(q, p)
        #if len(self._blockedQ) > 0:
        for b in self._blockedQ:
            if b._state == "Blocked":
                b._IO_time -= q._timeSlice
                self._unblock(b)

        if p._state =="Ready":
            p._priority += 1
            self.enqueue(self.dequeue(q._priority))
        
        print(self)  

    def _terminateProcess(self, q, p):
        """ terminates a completed process """


        defaultTimeSlice = q._timeSlice 
        q._timeSlice = p._time
        
        print("%s takes control of CPU"% p._pid)

        
        p._time -= q._timeSlice
        self._time += q._timeSlice
        print("Time slice: %s" % q._timeSlice)
        if p._IO is not None and p._IO > 0:
            p._IO -= q._timeSlice
            self._checkIO(q, p)
        self.dequeue(q._priority)
        
        print("%s finished" % p._pid)

        if p._state == "Blocked":
            if len(self._blockedQ) > 0: 
                self._blockedQ.pop(0)
        for b in self._blockedQ:
                if b._state == "Blocked":
                    b._IO_time -= q._timeSlice
                    self._unblock(b)

        q._timeSlice = defaultTimeSlice
        print(self)

    def _roundRobin(self, q, p):
        """ process is in the lowest priority queue and is scheduled in a round-robin manner """


        p._time -= q._timeSlice
        self._time += q._timeSlice
        print("Time slice: %s" % q._timeSlice)
        print("%s takes control of CPU"% p._pid)
        #print("After",p._time)
        if p._IO is not None and p._IO > 0:
            p._IO -= q._timeSlice
            self._checkIO(q, p)
        for b in self._blockedQ:   
            if b._state == "Blocked": 
                b._IO_time -= q._timeSlice   
                self._unblock(b)      
        self.enqueue(self.dequeue(q._priority))
        print(self)
    
if __name__ == "__main__":

    def testSchedule():
        Schedule = Scheduler(10)  # quantum = 10
        Schedule.enqueue(Process("p1",100,1,None,None)) # process 1, duration of 100ms, priority 1, no I/O 
        Schedule.enqueue(Process("p2",220,2,None,None))
        Schedule.enqueue(Process("p3",270,2,80,200)) # I/O starts at 80ms - I/O runs for 200ms 
        Schedule.enqueue(Process("p4",550,3,180,300)) # I/O starts at 180ms - I/O runs for 300ms 
        Schedule.enqueue(Process("p5",2140,5,None,None))
        Schedule.enqueue(Process("p6",2200,6,None, None))
        Schedule.mlfq()
    testSchedule()
