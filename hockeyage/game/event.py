from hockeyage.util import colors


class Event(object):
    def __init__(self):
        self.event = 0
        self.events = []
        self.plays = {'start': 0, 'end': 0, '_pass': 0, 'shot': 0, 'stop': 0,
                      'hit': 0, 'penalty': 0, 'block': 0, 'miss': 0, 'give': 0,
                      'take': 0, 'goal': 0, 'face': 0}
        self.zones = {'home': 0, 'neutral': 0, 'road': 0}

    def add(self, period, clock, play, zone):
        self.event += 1

        self.plays[play.name] += 1
        self.zones[zone.name] += 1

        self.events.append({'event': self.event,
                            'period': period.period,
                            'elapsed': clock.elapsed,
                            'remaining': clock.remaining,
                            'since': clock.since_last_tick,
                            'play': play.name,
                            'zone': zone.name,
                            'player1': play.player1,
                            'player2': play.player2,
                            'player3': play.player3})

    def show(self):
        print(colors.white('#\tPERIOD\tELAPSED\tREMAINING\tPLAY\tZONE\tPLAYER1\tPLAYER2\tPLAYER3', True))
        for e in self.events:
            out = '{event}\t{period}\t{elapsed}\t{remaining}\t\t{play}\t{zone}\t{player1}\t{player2}\t{player3}'
            out = out.format(**e)
            if e['play'] in ['penalty', 'stop']:
                out = colors.red(out, bold=True)
            print(out)
        print('pass: %(_pass)d shot: %(shot)d face: %(face)d hit: %(hit)d penalty: %(penalty)d block: %(block)d miss: %(miss)d give: %(give)d take: %(take)d goal; %(goal)d' % self.plays)
        print('neutral: %f home: %f road: %f' % (float(self.zones['neutral']) / sum(self.zones.values()),
                                                 float(self.zones['home']) / sum(self.zones.values()),
                                                 float(self.zones['road']) / sum(self.zones.values())))
