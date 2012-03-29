from hockeyage.game.team import Lineup, Lines, Team
from nose.tools import *


def test_team_init():
    team = Team('Foo Bars', 'FOO')
    assert_equal('Foo Bars', team.name)
    assert_equal('FOO', team.abbreviation)
    assert_true(isinstance(team.lineup, Lineup))


def test_lineup_init():
    lineup = Lineup()
    assert_equal(20, len(lineup.lineup))


def test_lines_init():
    lineup = Lineup()
    lines = Lines(lineup.lineup)
    assert_true('forward' in lines.preference)
    assert_true('defense' in lines.preference)
    assert_equal(4, len(lines.lw))
    assert_equal(4, len(lines.c))
    assert_equal(4, len(lines.rw))
    assert_equal(3, len(lines.ld))
    assert_equal(3, len(lines.rd))
    assert_equal(2, len(lines.gk))
    assert_true(lines.current_goalie in lines.gk)

def test_lines_event_strength():
    lineup = Lineup()
    lines = Lines(lineup.lineup)
    even_strength = lines.even_strength()
    assert_true('forward' in even_strength)
    assert_true('defense' in even_strength)
    assert_equal(4, len(even_strength['forward']))
    assert_equal(3, len(even_strength['defense']))
    assert_equal(3, len(even_strength['forward'][0]))
    assert_equal(2, len(even_strength['defense'][0]))
