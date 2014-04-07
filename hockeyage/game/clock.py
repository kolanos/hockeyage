import random


def format_time(seconds):
    minutes = seconds / 60
    seconds = seconds % 60
    return "%02d:%02d" % (minutes, seconds)


class Clock(object):
    PERIOD_LENGTH = 1200
    OVERTIME_LENGTH = 300
    MAX_TICK_INTERVAL = 12

    def __init__(self, period):
        self.clock = 0
        self.last_tick = 0
        self.total_time = self.PERIOD_LENGTH if period.period < 4 \
                                            else self.OVERTIME_LENGTH

    def tick(self, interval=None):
        self.last_tick = self.clock
        self.clock += random.randint(1, self.MAX_TICK_INTERVAL) \
            if interval is None else interval

    def end(self):
        self.last_tick = self.clock
        self.clock = self.total_time

    @property
    def running(self):
        return self.clock < self.total_time

    @property
    def elapsed(self):
        return format_time(self.clock)

    @property
    def remaining(self):
        return format_time(self.total_time - self.clock)

    @property
    def since_last_tick(self):
        return min(self.clock, self.total_time) - self.last_tick
