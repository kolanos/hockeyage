from hockeyage.game.match import *
from hockeyage.util import colors

class Event(object):
    def __init__(self):
        self.event = 0
        self.events = []
        self.plays = {}
        self.zones = {}
    
    def add(self, period, clock, play, zone):
        self.event += 1

        if play not in self.plays:
            self.plays[play] = 1
        else:
            self.plays[play] += 1

        if zone not in self.zones:
            self.zones[zone] = 1
        else:
            self.zones[zone] += 1

        self.events.append({'event': self.event,
                            'period': period,
                            'elapsed': clock.elapsed,
                            'remaining': clock.remaining,
                            'since': clock.since_last_tick,
                            'play': play,
                            'zone': zone})
    
    def show(self):
        print(colors.white('#\tPERIOD\tELAPSED\tREMAINING\tPLAY\tZONE', True))
        for e in self.events:
            out = '%(event)d\t%(period)d\t%(elapsed)s\t%(remaining)s\t\t%(play)s\t%(zone)s' % e
            if e['play'] in ['penalty', 'stop']:
                out = colors.red(out, bold=True)
            print(out)
        print('shot: %(shot)d face: %(face)d hit: %(hit)d penalty: %(penalty)d block: %(block)d miss: %(miss)d give: %(give)d take: %(take)d goal; %(goal)d' % self.plays)
        print('neutral: %f home: %f road: %f' % (float(self.zones['NEUTRAL']) / sum(self.zones.values()),
                                                 float(self.zones['HOME']) / sum(self.zones.values()),
                                                 float(self.zones['ROAD']) / sum(self.zones.values())))
