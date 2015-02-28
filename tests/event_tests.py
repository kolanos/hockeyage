
from nose.tools import *

from hockeyage.game.clock import Clock
from hockeyage.game.event import Event
from hockeyage.game.match import Period


def test_init():
    event = Event()
    assert_equal([], event.events)


def test_add():
    event = Event()
    period = Period()
    clock = Clock(period)
    event.add(1, clock, 'face', 'NEUTRAL')
    assert_equal(1, event.event)
    assert_true(len(event.events) == 1)
    assert_equal(1, event.events[0]['period'])
    assert_equal('00:00', event.events[0]['elapsed'])
    assert_equal('20:00', event.events[0]['remaining'])
    assert_equal('face', event.events[0]['play'])
    assert_equal('NEUTRAL', event.events[0]['zone'])
