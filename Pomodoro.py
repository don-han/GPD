from datetime import datetime
from time import sleep
class Timer:
    def __init__(self, interval, message):
        self.interval = interval * 60 # minute -> seconds
        self.message = message
    def run(self):
        remaining = self.interval
        startTime = datetime.now()
        print("Started at {0:02}:{1:02}'{2:02}".format(startTime.hour, startTime.minute, startTime.second))
        for i in range(remaining)
            mins, secs = secondsToTime(i)
            print("{0:02}:{1:02} {2}".format(mins, secs, self.message), end="\r") 
            sleep(1)
        endTime = datetime.now()
        print("Ended at {0:02}:{1:02}'{2:02}".format(endTime.hour, endTime.minute, endTime.second ))
    def secondsToTime(s):
        minutes = s // 60
        seconds = s - (minutes * 60)
        return minutes, seconds
