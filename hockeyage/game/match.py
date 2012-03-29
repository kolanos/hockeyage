from hockeyage.game.clock import Clock
from hockeyage.game.event import Event
from hockeyage.game.play import Play
from hockeyage.game.team import Team
from hockeyage.util import probability

PERIOD_LENGTH = 1200
OVERTIME_LENGTH = 300


def zone(z):
    if z > 0:
        return 'HOME'
    if z < 0:
        return 'ROAD'
    return 'NEUTRAL'


class Match(object):
    def __init__(self, show_events=False):
        self.show_events = show_events

        self.event = Event()
        self.play = Play()

        self.home = Team('Calgary Flames', 'CGY')
        self.road = Team('Edmonton Oilers', 'EDM')

        self.period = 0
        self.zone = 0
        self.start_period()

    def start_period(self):
        self.period += 1
        self.clock = Clock(self.period, PERIOD_LENGTH, OVERTIME_LENGTH)
        self.play = Play()
        self.event.add(self.period, self.clock, 'start', zone(self.zone))
        self.event.add(self.period, self.clock, self.play(), zone(self.zone))
        while self.clock.running:
            self.next_event()

    def end_period(self):
        self.clock.end()
        self.event.add(self.period, self.clock, 'end', zone(self.zone))
        if self.period < 3:
            self.start_period()
        else:
            self.end_game()

    def next_event(self):
        self.clock.tick()

        self.home.lineup.lines.add_toi(self.clock.since_last_tick)
        self.road.lineup.lines.add_toi(self.clock.since_last_tick)

        if not self.clock.running:
            self.end_period()
        else:
            self.home.lineup.lines.line_change()
            self.road.lineup.lines.line_change()

            advance_choices = [(-1, self.road.lineup.lines.average_rating),
                               (1, self.home.lineup.lines.average_rating)]
            advance = probability.weighted_choice(advance_choices)
            self.zone += advance
            if self.zone > 0:
                self.zone = 1
            elif self.zone < 0:
                self.zone = -1

            self.event.add(self.period, self.clock, self.play(),
                           zone(self.zone))

    def end_game(self):
        if self.show_events:
            self.event.show()
