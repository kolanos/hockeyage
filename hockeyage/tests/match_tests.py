from hockeyage.game.event import Event
from hockeyage.game.match import Match, zone
from hockeyage.game.play import Play
from hockeyage.game.team import Team
from nose.tools import *


def test_zone():
    z = zone(0)
    assert_equal('NEUTRAL', z)
    z = zone(1)
    assert_equal('HOME', z)
    z = zone(-1)
    assert_equal('ROAD', z)


def test_init():
    match = Match()
    assert_true(isinstance(match.event, Event))
    assert_true(isinstance(match.home, Team))
    assert_true(isinstance(match.road, Team))
    assert_true(isinstance(match.play, Play))
    assert_equal('start', match.event.events[0]['play'])
