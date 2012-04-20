from hockeyage.game.clock import Clock, format_time
from nose.tools import *


def test_format_time():
    assert_equal('14:45', format_time(885))
    assert_equal('3600:00', format_time(60*60*60))


def test_init():
    clock = Clock()
    assert_equal(0, clock.clock)
    assert_equal(0, clock.last_tick)
    assert_equal(1200, clock.total_time)


def test_tick():
    clock = Clock()
    clock.tick()
    assert_true(clock.clock > 0)
    clock = Clock()
    clock.tick(30)
    assert_equal(30, clock.clock)


def test_end():
    clock = Clock()
    clock.end()
    assert_true(clock.clock == clock.total_time)


def test_running():
    clock = Clock()
    assert_true(clock.running)


def test_elapsed():
    clock = Clock()
    assert_equal('00:00', clock.elapsed)
    clock.tick(30)
    assert_equal('00:30', clock.elapsed)


def test_remaining():
    clock = Clock()
    assert_equal('20:00', clock.remaining)
    clock.tick(30)
    assert_equal('19:30', clock.remaining)


def test_since_last_tick():
    clock = Clock()
    clock.tick(30)
    assert_equal(30, clock.since_last_tick)
