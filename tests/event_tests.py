from nose.tools import *

from hockeyage.game.clock import Clock
from hockeyage.game.event import Event
from hockeyage.game.match import Period
from hockeyage.game.match import Possession
from hockeyage.game.match import Zone
from hockeyage.game.play import Start


def test_init():
    event = Event()
    assert_equal([], event.events)


def test_add():
    event = Event()
    period = Period()
    clock = Clock(period)
    possession = Possession()
    zone = Zone()
    play = Start(None, None, zone, possession)
    event.add(period, clock, play, zone)
    assert_equal(1, event.event)
    assert_true(len(event.events) == 1)
    assert_equal(period.period, event.events[0]['period'])
    assert_equal('00:00', event.events[0]['elapsed'])
    assert_equal('20:00', event.events[0]['remaining'])
    assert_equal(play.name, event.events[0]['play'])
    assert_equal(zone.name, event.events[0]['zone'])
