import re
import urllib2

from BeautifulSoup import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

PLAYS_URL = 'http://www.nhl.com/scores/htmlreports/%s/PL02%s.HTM'
ROSTER_URL = 'http://www.nhl.com/scores/htmlreports/%s/RO02%s.HTM'
SUMMARY_URL = 'http://www.nhl.com/scores/htmlreports/%s/GS02%s.HTM'


def pad_zeroes(id, length=4):
    id = str(id)
    while len(id) < length:
        id = '0%s' % str(id)
    return id


def game_generator(season, start, end):
    for i in xrange(start, end+1):
        game = urllib2.urlopen(PLAYS_URL % (season, pad_zeroes(i)))
        game = BeautifulSoup(game)
        yield (i, game)


def event_generator(root):
    for period in root.html.body.findAll('table', attrs={'class': 'tablewidth'}, recursive=False):
        for event in period.findAll(name="tr", recursive=False, attrs={'class': 'evenColor'}):
            event = event_decoder(event)
            yield event


def event_description(type, desc):
    desc = desc.replace('&nbsp;', ' ')
    d = dict(description=desc)
    if type == 'BLOCK':
        d['type'] = 'block'
        d['player1'], rest = desc.split(' BLOCKED BY  ')
        d['team'], d['player1'] = d['player1'].split(' ', 1)
        d['player2'], d['shot_type'], d['zone'] = rest.split(', ')
        _, d['player2'] = d['player2'].split(' ', 1)
    elif type == 'FAC':
        d['type'] = 'face'
        d['team'], rest = desc.split(' won ')
        d['zone'], rest = rest.split(' - ')
        player1, player2 = rest.split(' vs ')
        if d['team'] == player1[:3]:
            d['player1'], d['player2'] = player1, player2
        else:
            d['player1'], d['player2'] = player2, player1
        _, d['player1'] = d['player1'].split(' ', 1)
        _, d['player2'] = d['player2'].split(' ', 1)
    elif type == 'GIVE':
        d['type'] = 'give'
        d['team'], rest = desc.split(' GIVEAWAY - ')
        d['player1'], d['zone'] = rest.split(', ')
    elif type == 'GOAL':
        d['type'] = 'goal'
        d['player1'], d['shot_type'], d['zone'], distance_rest = desc.split(', ')
        if d['player1'].find('(') != -1:
            d['player1'], _ = d['player1'].split('(')
        assists = []
        if desc.find('Assist') != -1:
            d['distance'], assists_ = distance_rest.split(' ft.Assist')
            _, assists_ = assists_.split(': ')
            assists_ = assists_.split('; ')
            d['team'], d['player1'] = d['player1'].split(' ', 1)
            for assist in assists_:
                if assist.find('(') != -1:
                    assist, _ = assist.split('(')
                assists.append(assist)
            if len(assists) == 1:
                d['player2'] = assists[0]
            elif len(assists) == 2:
                d['player2'] = assists[0]
                d['player3'] = assists[1]
        else:
            d['distance'], _ = distance_rest.split(' ft.')
    elif type == 'HIT':
        d['type'] = 'hit'
        d['player1'], rest = desc.split(' HIT ')
        d['team'], d['player1'] = d['player1'].split(' ', 1)
        d['player2'], d['zone'] = rest.split(', ')
        _, d['player2'] = d['player2'].split(' ', 1)
    elif type == 'MISS':
        d['type'] = 'miss'
        d['player1'], d['shot_type'], d['where'], d['zone'], d['distance'] = desc.split(', ')
        d['team'], d['player1'] = d['player1'].split(' ', 1)
        d['distance'], _ = d['distance'].split(' ')
    elif type == 'PENL':
        d['type'] = 'penalty'
        taken, drawn = desc.split(' min)')
        if taken.find('Served') != -1:
            taken, served = taken.split(' Served By: ')
            _, d['player3'] = served.split(' ', 1)
        d['team'], taken = taken.split(' ', 1)
        taken, d['penalty_minutes'] = taken.split('(', 1)
        d['player1'], d['penalty'] = taken.rsplit(' ', 1)
        rest = None
        if drawn.find('Drawn') != -1:
            rest, d['player2'] = drawn.split(' Drawn By: ')
            _, d['player2'] = d['player2'].split(' ', 1)
        if rest and rest.find('Zone') != -1:
            d['zone'] = rest[2:]
    elif type in ['PEND', 'GEND']:
        d['type'] = 'end'
    elif type == 'PSTR':
        d['type'] = 'start'
    elif type == 'SHOT':
        d['type'] = 'shot'
        d['team'], rest = desc.split(' ONGOAL - ')
        d['player1'], d['shot_type'], d['zone'], d['distance'] = rest.split(', ')
        d['distance'], _ = d['distance'].split(' ')
    elif type == 'STOP':
        d['type'] = 'stop'
        if desc.find(',') != -1:
            stop, _ = desc.split(",", 1)
            tv_timeout = _.find("TV") != -1
            visitor_timeout = _.find("VISITOR") != -1
            home_timeout = _.find("HOME") != -1
        else:
            stop = desc
            tv_timeout = False
            home_timeout = False
            visitor_timeout = False
    elif type == 'TAKE':
        d['type'] = 'take'
        d['team'], rest = desc.split(' TAKEAWAY - ')
        d['player1'], d['zone'] = rest.split(', ')
    elif type == 'SOC':
        d['type'] = 'shootout'
    else:
        d['type'] = 'unknown'
    return d


def event_decoder(raw_event):
    def decode_time(time):
        idx = time.text.find(":")
        elapsed = time.text[:idx+3]
        remaining = time.text[idx+3:]
        return (elapsed, remaining)

    def decode_player_on_ice(players):
        _players = []
        if len(players.findAll("table")) == 0:
            return _players
        for player in players.table.tr.findAll("table"):
            name = player.font['title'].split(" - ")[1]
            number = int(player.font.text)
            position = player.findAll("td")[1].text
            _players.append((name,number,position))
        return _players

    elems = [elem for elem in raw_event.findAll("td", recursive=False)]
    e = {
        'number': int(elems[0].text),
        'period': int(elems[1].text),
        'strength': elems[2].text if elems[2].text != '&nbsp;' else None,
        'elapsed': decode_time(elems[3])[0],
        'remaining': decode_time(elems[3])[1],
        #'type': elems[4].text,
        #'description': elems[5].text,
        #'road_on_ice': decode_player_on_ice(elems[6]),
        #'home_on_ice': decode_player_on_ice(elems[7])
    }
    e.update(event_description(elems[4].text, elems[5].text))
    return e


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--season', action='store', dest='season',
                    default='20112012', help='Season to parse'),
        make_option('--start', action='store', type='int', dest='start',
                    default=1, help='Game ID to start at'),
        make_option('--end', action='store', type='int', dest='end', default=1230,
                    help='Game ID to end at'),
        make_option('--events', action='store_true', dest='events',
                    default=False, help='Parse game events'),
        make_option('--rosters', action='store_true', dest='rosters',
                    default=False, help='Parse game rosters'),
        make_option('--save', action='store_true', dest='save',
                    default=False, help='Save parse results in database'),
    )

    def handle(self, *args, **options):
        if options['events']:
            for i, game in game_generator(options['season'], options['start'],
                                       options['end']):
                self.stdout.write('Parsing Game %d\n' % i)
                for e in event_generator(game):
                    pass
                self.stdout.write('Done.\n')
