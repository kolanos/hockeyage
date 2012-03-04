from hockeyage.game.match import *
from hockeyage.util import colors

class Event(object):
    def __init__(self):
        self.event = 0
        self.events = []
        print(colors.white('#\tPERIOD\tELAPSED\tREMAINING\tPLAY SINCE', True))
    
    def next_event(self, period, clock):
        self.event += 1
        self.events.append({'event': self.event,
                            'period': period,
                            'elapsed': clock.elapsed,
                            'remaining': clock.remaining,
                            'since': clock.since_last_tick})
    
    def show_events(self):
        for e in self.events:
            print('%(event)d\t%(period)d\t%(elapsed)s\t%(remaining)s\t%(since)d' % e)
