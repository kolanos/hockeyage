
from nose.tools import *

from hockeyage.game.clock import Clock, format_time
from hockeyage.game.match import Period


def test_format_time():
    assert_equal('14:45', format_time(885))
    assert_equal('3600:00', format_time(60*60*60))


def test_init():
    period = Period()
    clock = Clock(period)
    assert_equal(0, clock.clock)
    assert_equal(0, clock.last_tick)
    assert_equal(1200, clock.total_time)


def test_tick():
    period = Period()
    clock = Clock(period)
    clock.tick()
    assert_true(clock.clock > 0)
    period = Period()
    clock = Clock(period)
    clock.tick(30)
    assert_equal(30, clock.clock)


def test_end():
    period = Period()
    clock = Clock(period)
    clock.end()
    assert_true(clock.clock == clock.total_time)


def test_running():
    period = Period()
    clock = Clock(period)
    assert_true(clock.running)


def test_elapsed():
    period = Period()
    clock = Clock(period)
    assert_equal('00:00', clock.elapsed)
    clock.tick(30)
    assert_equal('00:30', clock.elapsed)


def test_remaining():
    period = Period()
    clock = Clock(period)
    assert_equal('20:00', clock.remaining)
    clock.tick(30)
    assert_equal('19:30', clock.remaining)


def test_since_last_tick():
    period = Period()
    clock = Clock(period)
    clock.tick(30)
    assert_equal(30, clock.since_last_tick)
