import random

class Clock(object):
    def __init__(self, period_length, overtime_length, period):
        self.clock = 0
        self.time_left = period_length if period < 4 else overtime_length 
    
    def running(self):
        return self.clock < self.time_left
    
    def tick(self):
        self.last_tick = self.clock
        self.clock += random.randint(1, 25)
    
    @property
    def elapsed(self):
        seconds = self.clock
        minutes = seconds / 60
        seconds -= 60*minutes
        return "%02d:%02d" % (minutes, seconds)

    @property
    def remaining(self):
        seconds = self.time_left - self.clock
        minutes = seconds / 60
        seconds -= 60*minutes
        return "%02d:%02d" % (minutes, seconds)

    @property
    def since_last_tick(self):
        return min(self.clock, self.time_left) - self.last_tick

    @staticmethod
    def format_time(seconds):
        minutes = seconds / 60
        seconds -= 60*minutes
        return "%02d:%02d" % (minutes, seconds)
