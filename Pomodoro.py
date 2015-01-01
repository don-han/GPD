from datetime import datetime
from time import sleep
class Timer:
    def run(self, interval, message=""):
        remaining = interval//2#interval * 60    # minute -> seconds
        startTime = datetime.now()
        print("Started at {0:02}:{1:02}'{2:02}".format(startTime.hour, startTime.minute, startTime.second))
        for i in range(remaining):
            mins, secs = self.secondsToTime(remaining - i)
            print("{0:02}:{1:02} {2}".format(mins, secs, message), end="\r") 
            sleep(1)
        endTime = datetime.now()
        print("Ended at {0:02}:{1:02}'{2:02}".format(endTime.hour, endTime.minute, endTime.second))

    def secondsToTime(self,s):
        minutes = s // 60
        seconds = s - (minutes * 60)
        return minutes, seconds

if __name__ == "__main__":
    pomo = Timer()
    while True:
        pomo.run(25)
        pomo.run(5)
        pomo.run(25)
        pomo.run(5)
        pomo.run(25)
        pomo.run(5)
        pomo.run(25)
        pomo.run(15)

