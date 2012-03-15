from hockeyage.game.clock import Clock
from hockeyage.game.event import Event
from hockeyage.game.play import Play
from hockeyage.game.team import Team

PERIOD_LENGTH = 1200
OVERTIME_LENGTH = 300

class Match(object):
    def __init__(self):
        self.play = Play()
        self.start_game()
    
    def start_game(self):
        self.home_team = Team('Calgary Flames', 'CGY')
        self.road_team = Team('Edmonton Oilers', 'EDM')
        self.event = Event()
        self.period = 0
        self.start_period()
    
    def start_period(self):
        self.period += 1
        self.clock = Clock(PERIOD_LENGTH, OVERTIME_LENGTH, self.period)
        self.play = Play()
        self.event.next_event(self.period, self.clock, 'start')
        self.event.next_event(self.period, self.clock, self.play())
        while self.clock.running():
            self.next_event()

    def end_period(self):
        self.clock.end()
        self.event.next_event(self.period, self.clock, 'end')
        if self.period < 3:
            self.start_period()
        else:
            self.end_game()
            
    def next_event(self):
        self.clock.tick()

        self.home_team.lineup.lines.add_toi(self.clock.since_last_tick)
        self.road_team.lineup.lines.add_toi(self.clock.since_last_tick)

        if not self.clock.running():
            self.end_period()
        else:
            self.home_team.lineup.lines.line_change()
            self.road_team.lineup.lines.line_change()

            self.event.next_event(self.period, self.clock, self.play())
    
    def end_game(self):
        self.event.show_events()
        #exit()


