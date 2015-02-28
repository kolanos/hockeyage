from hockeyage.game.event import Event
from hockeyage.game.match import Match, Zone
from hockeyage.game.play import Play
from hockeyage.game.team import Team
from nose.tools import *


def test_zone():
    z = Zone()
    assert_equal(z.NEUTRAL, z.name)

    z = Zone()
    z.advance(1)
    assert_equal(z.HOME, z.name)

    z = Zone()
    z.advance(-1)
    assert_equal(z.ROAD, z.name)


def test_init():
    match = Match()
    assert_true(isinstance(match.event, Event))
    assert_true(isinstance(match.home, Team))
    assert_true(isinstance(match.road, Team))
    assert_true(isinstance(match.play, Play))
    assert_equal('start', match.event.events[0]['play'])
