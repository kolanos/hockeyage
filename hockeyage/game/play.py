from hockeyage.util.probability import weighted_choice


class Play(object):
    PASS_BASELINE = 48
    SHOT_BASELINE = 12
    STOP_BASELINE = 10
    HIT_BASELINE = 7
    PENALTY_BASELINE = 5
    BLOCK_BASELINE = 5
    MISS_BASELINE = 4
    GIVE_BASELINE = 3
    TAKE_BASELINE = 2
    GOAL_BASELINE = 1

    def __init__(self, home, road, zone):
        self.last_play = None

        self.home = home
        self.road = road
        self.zone = zone

    def __call__(self):
        if self.last_play is None:
            self.last_play = self.face()
        else:
            self.last_play = getattr(self, self.last_play.name)()
        return self.last_play

    def next_play(self):
        pass_base = self.PASS_BASELINE
        shot_base = self.SHOT_BASELINE
        stop_base = self.STOP_BASELINE
        hit_base = self.HIT_BASELINE
        penalty_base = self.PENALTY_BASELINE
        block_base = self.BLOCK_BASELINE
        miss_base = self.MISS_BASELINE
        give_base = self.GIVE_BASELINE
        take_base = self.TAKE_BASELINE
        goal_base = self.GOAL_BASELINE

        return weighted_choice(((Pass, pass_base),
                                (Shot, shot_base),
                                (Stop, stop_base),
                                (Hit, hit_base),
                                (Penalty, penalty_base),
                                (Block, block_base),
                                (Miss, miss_base),
                                (Give, give_base),
                                (Take, take_base),
                                (Goal, goal_base)))

    def start(self):
        return Face(self.home, self.road, self.zone)

    def end(self):
        return Start(self.home, self.road, self.zone)

    def stop(self):
        return Face(self.home, self.road, self.zone)

    def goal(self):
        return Face(self.home, self.road, self.zone)

    def penalty(self):
        return Face(self.home, self.road, self.zone)

    def _pass(self):
        return self.next_play()(self.home, self.road, self.zone)

    def face(self):
        return self.next_play()(self.home, self.road, self.zone)

    def shot(self):
        return self.next_play()(self.home, self.road, self.zone)

    def miss(self):
        return self.next_play()(self.home, self.road, self.zone)

    def block(self):
        return self.next_play()(self.home, self.road, self.zone)

    def give(self):
        return self.next_play()(self.home, self.road, self.zone)

    def take(self):
        return self.next_play()(self.home, self.road, self.zone)

    def hit(self):
        return self.next_play()(self.home, self.road, self.zone)


class PlayType(object):
    def __init__(self, home, road, zone):
        self.home = home
        self.road = road
        self.zone = zone


class Start(PlayType):
    name = 'start'

    def __init__(self, home, road, zone):
        super(Start, self).__init__(home, road, zone)

        self.home.lose_possession()
        self.road.lose_possession()
        self.zone.center_ice()


class End(Start):
    name = 'end'


class Stop(PlayType):
    name = 'stop'

    def __init__(self, home, road, zone):
        super(Stop, self).__init__(home, road, zone)

        self.home.lose_possession()
        self.road.lose_possession()


class Pass(PlayType):
    name = '_pass'

    def __init__(self, home, road, zone):
        super(Pass, self).__init__(home, road, zone)


class Goal(PlayType):
    name = 'goal'

    def __init__(self, home, road, zone):
        super(Goal, self).__init__(home, road, zone)


class Penalty(PlayType):
    name = 'penalty'

    def __init__(self, home, road, zone):
        super(Penalty, self).__init__(home, road, zone)


class Face(PlayType):
    name = 'face'

    def __init__(self, home, road, zone):
        super(Face, self).__init__(home, road, zone)


class Shot(PlayType):
    name = 'shot'

    def __init__(self, home, road, zone):
        super(Shot, self).__init__(home, road, zone)


class Miss(PlayType):
    name = 'miss'

    def __init__(self, home, road, zone):
        super(Miss, self).__init__(home, road, zone)


class Block(PlayType):
    name = 'block'

    def __init__(self, home, road, zone):
        super(Block, self).__init__(home, road, zone)


class Give(PlayType):
    name = 'give'

    def __init__(self, home, road, zone):
        super(Give, self).__init__(home, road, zone)


class Take(PlayType):
    name = 'take'

    def __init__(self, home, road, zone):
        super(Take, self).__init__(home, road, zone)


class Hit(PlayType):
    name = 'hit'

    def __init__(self, home, road, zone):
        super(Hit, self).__init__(home, road, zone)
