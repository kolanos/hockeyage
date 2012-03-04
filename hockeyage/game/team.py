import random

from hockeyage.util import dotdict, probability

class Team(object):
    def __init__(self, name, abbreviation):
        self.name = name
        self.abbreviation = abbreviation
        self.lineup = Lineup()

class Lineup(object):
    def __init__(self, lineup=None):
        if lineup:
            self.lineup = lineup
        else:
            self.generate()

        self.lines = Lines(self.lineup)

    def generate(self):
        self.lineup = {}
        for pos in ['LW1', 'C1', 'RW1', 'LD1', 'RD1', 'GK1',
                    'LW2', 'C2', 'RW2', 'LD2', 'RD2', 'GK2',
                    'LW3', 'C3', 'RW3', 'LD3', 'RD3',
                    'LW4', 'C4', 'RW4']:
            self.lineup[pos] = Player(overall=random.randrange(50, 99), toi=0)

class Lines(object):
    def __init__(self, lineup, line_preference=None):
        self.lineup = lineup

        if line_preference:
            self.line_preference = line_preference
        else:
            self.line_preference = {'forward': [(0, 40), (1, 30), (2, 20), (3, 10)],
                                    'defense': [(0, 40), (1, 35), (2, 25)]}

        self.lw = self.get_by_pos('LW')
        self.c = self.get_by_pos('C')
        self.rw = self.get_by_pos('RW')
        self.ld = self.get_by_pos('LD')
        self.rd = self.get_by_pos('RD')
        self.gk = self.get_by_pos('GK')

        self.lines = self.even_strength()
        self.select_goalie()
        self.line_change()

    def even_strength(self):
        lines = {'forward': [], 'defense': []}
        for i in xrange(4):
            lines['forward'].append((self.lw[i], self.c[i], self.rw[i]))
        for i in xrange(3):
            lines['defense'].append((self.ld[i], self.rd[i]))
        return lines

    def select_goalie(self):
        selection = probability.weighted_choice([(0, 80), (1, 20)])
        self.current_goalie = self.gk[selection]

    def line_change(self):
        self.forward_line = probability.weighted_choice(self.line_preference['forward'])
        self.defense_line = probability.weighted_choice(self.line_preference['defense'])
        self.current_line = {'forward': self.lines['forward'][self.forward_line],
                             'defense': self.lines['defense'][self.defense_line]}

    def get_by_pos(self, pos, sort=True):
        players = []
        for k, v in self.lineup.items():
            if k.startswith(pos):
                players.append(v)
        if sort:
            players = sorted(players, key=lambda k: k['overall'], reverse=True)
        return players

    def add_toi(self, toi):
        for forward in self.current_line['forward']:
            forward['toi'] = forward['toi'] + toi
        for defense in self.current_line['defense']:
            defense['toi'] = defense['toi'] + toi
        self.current_goalie['toi'] = self.current_goalie['toi'] + toi

class Player(dotdict):
    pass
