from hockeyage.game.match import *
from hockeyage.util import colors

class Event(object):
    def __init__(self):
        self.event = 0
        self.events = []
        self.plays = {}
        print(colors.white('#\tPERIOD\tELAPSED\tREMAINING\tPLAY', True))
    
    def next_event(self, period, clock, play):
        self.event += 1
        if play not in self.plays:
            self.plays[play] = 1
        else:
            self.plays[play] += 1
        self.events.append({'event': self.event,
                            'period': period,
                            'elapsed': clock.elapsed,
                            'remaining': clock.remaining,
                            'since': clock.since_last_tick,
                            'play': play})
    
    def show_events(self):
        for e in self.events:
            out = '%(event)d\t%(period)d\t%(elapsed)s\t%(remaining)s\t%(play)s' % e
            if e['play'] in ['penalty', 'stop']:
                out = colors.red(out, bold=True)
            print(out)

        print('goal; %(goal)d shot: %(shot)d block: %(block)d miss: %(miss)d hit: %(hit)d' % self.plays)
