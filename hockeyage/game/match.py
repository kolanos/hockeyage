from hockeyage.game.clock import Clock
from hockeyage.game.event import Event
from hockeyage.game.play import Play
from hockeyage.game.team import Team
from hockeyage.util import probability


class Match(object):
    def __init__(self, show_events=False):
        self.show_events = show_events

        self.event = Event()

        self.home = Team('Calgary Flames', 'CGY')
        self.road = Team('Edmonton Oilers', 'EDM')

        self.period = Period()
        self.start_period()

    def start_period(self):
        self.period.next_period()
        self.clock = Clock(self.period)
        self.zone = Zone()
        self.possession = Possession()

        self.play = Play(self.home, self.road, self.zone, self.possession)

        self.event.add(self.period, self.clock, self.play(), self.zone.name)
        self.event.add(self.period, self.clock, self.play(), self.zone.name)

        while self.clock.running:
            self.next_event()

    def end_period(self):
        self.clock.end()
        self.event.add(self.period, self.clock, self.play.end(), self.zone.name)
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

            self.event.add(self.period,
                           self.clock,
                           self.play(),
                           self.zone.name)

    def end_game(self):
        if self.show_events:
            self.event.show()


class Period(object):
    def __init__(self):
        self.period = 0

    def next_period(self):
        self.period += 1


class Zone(object):
    NEUTRAL = 'neutral'
    HOME = 'home'
    ROAD = 'road'

    def __init__(self):
        self.zone = 0

    @property
    def name(self):
        if self.zone > 0:
            return self.HOME
        if self.zone < 0:
            return self.ROAD
        return self.NEUTRAL

    def center_ice(self):
        self.zone = 0

    def advance(self, advance):
        self.zone += advance
        if self.zone > 0:
            self.zone = 1
        elif self.zone < 0:
            self.zone = -1


class Possession(object):
    def __init__(self):
        self.has_possession = None
        self.has_puck = None

    def gain_possession(self, possession, player=None):
        self.has_possession = possession
        self.has_puck = player

        if not self.has_puck:
            self.has_puck = self.has_possession.lines.weighted_choice()

    def loose_puck(self):
        self.has_possession = None
