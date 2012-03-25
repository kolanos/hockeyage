from hockeyage.game.clock import Clock
from hockeyage.game.event import Event
from nose.tools import *


def test_init():
    event = Event()
    assert_equal([], event.events)


def test_add():
    event = Event()
    clock = Clock()
    event.add(1, clock, 'face', 'NEUTRAL')
    assert_equal(1, event.event)
    assert_true(len(event.events) == 1)
    assert_equal(1, event.events[0]['period'])
    assert_equal('00:00', event.events[0]['elapsed'])
    assert_equal('20:00', event.events[0]['remaining'])
    assert_equal('face', event.events[0]['play'])
    assert_equal('NEUTRAL', event.events[0]['zone'])
