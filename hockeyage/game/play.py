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

    def __init__(self, home, road, zone, possession):
        self.last_play = None

        self.home = home
        self.road = road
        self.zone = zone
        self.possession = possession

    def __call__(self):
        if self.last_play is None:
            self.last_play = Start(self.home, self.road, self.zone,
                                   self.possession)
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

        if self.zone.name == self.zone.NEUTRAL:
            shot_base = 1
            block_base = 1
            miss_base = 1
            goal_base = 0

        # Loose puck, battle for possession.
        if not self.possession.has_possession:
            takes_it = [(self.home, self.home.lines.average_rating),
                        (self.road, self.home.lines.average_rating)]
            takes_it = weighted_choice(takes_it)
            self.possession.gain_possession(takes_it)

        if self.possession.has_possession == self.home:
            # If badly outclassed the chance exists for rapid puck movement.
            breakaway = self.home.lines.average_rating - self.road.lines.average_rating
            if breakaway < 0:
                breakaway = 0

            advance = [(0, self.road.lines.average_rating),
                       (1, self.home.lines.average_rating),
                       (2, breakaway)]
            advance = weighted_choice(advance)
            self.zone.advance(advance)

        if self.possession.has_possession == self.road:
            breakaway = self.road.lines.average_rating - self.home.lines.average_rating
            if breakaway < 0:
                breakaway = 0

            advance = [(0, self.home.lines.average_rating),
                       (-1, self.road.lines.average_rating),
                       (-2, breakaway)]
            advance = weighted_choice(advance)
            self.zone.advance(advance)

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
        return Face(self.home, self.road, self.zone, self.possession)

    def end(self):
        return End(self.home, self.road, self.zone, self.possession)

    def stop(self):
        return Face(self.home, self.road, self.zone, self.possession)

    def goal(self):
        return Face(self.home, self.road, self.zone, self.possession)

    def penalty(self):
        return Face(self.home, self.road, self.zone, self.possession)

    def _pass(self):
        return self.next_play()(self.home, self.road, self.zone,
                self.possession)

    def face(self):
        return self.next_play()(self.home, self.road, self.zone,
                                self.possession)

    def shot(self):
        return self.next_play()(self.home, self.road, self.zone, self.possession)

    def miss(self):
        return self.next_play()(self.home, self.road, self.zone, self.possession)

    def block(self):
        return self.next_play()(self.home, self.road, self.zone, self.possession)

    def give(self):
        return self.next_play()(self.home, self.road, self.zone, self.possession)

    def take(self):
        return self.next_play()(self.home, self.road, self.zone, self.possession)

    def hit(self):
        return self.next_play()(self.home, self.road, self.zone, self.possession)


class PlayType(object):
    name = None
    player1 = None
    player2 = None
    player3 = None
    extra = None

    def __init__(self, home, road, zone, possession):
        self.home = home
        self.road = road
        self.zone = zone
        self.possession = possession

    def result(self):
        pass


class Start(PlayType):
    name = 'start'

    def result(self):
        self.zone.center_ice()
        self.possession.loose_puck()


class End(Start):
    name = 'end'


class Stop(PlayType):
    name = 'stop'

    def result(self):
        self.possession.loose_puck()


class Pass(PlayType):
    name = '_pass'


class Goal(PlayType):
    name = 'goal'

    def result(self):
        scoring_team = self.home if self.zone.name == self.zone.HOME \
                                 else self.road
        scoring_team = scoring_team.lines

        self.player1 = scoring_team.weighted_choice()

        num_assists = weighted_choice([(0, 10), (1, 20), (2, 70)])
        if num_assists > 0:
            self.player2 = scoring_team.weighted_choice(exclude=[self.player1])
        if num_assists > 1:
            self.player3 = scoring_team.weighted_choice(exclude=[self.player1,
                                                                 self.player2])


class Penalty(PlayType):
    name = 'penalty'


class Face(PlayType):
    name = 'face'

    def result(self):
        home_face = self.home.lines.forward_by_pos('C')
        road_face = self.road.lines.forward_by_pos('C')

        # Tossed from the faceoff circle?
        if weighted_choice([(True, 20), (False, 80)]):
            home_face = self.home.lines.weighted_forward(exclude=[home_face])
        if weighted_choice([(True, 20), (False, 80)]):
            road_face = self.road.lines.weighted_forward(exclude=[road_face])

        winner = weighted_choice([(self.home, home_face['overall']),
                                  (self.road, road_face['overall'])])

        if winner == self.home:
            self.player1 = home_face
            self.player2 = road_face

            self.possession.gain_possession(self.home)
        else:
            self.player1 = road_face
            self.player2 = home_face

            self.possession.gain_possession(self.road)


class Shot(PlayType):
    name = 'shot'


class Miss(PlayType):
    name = 'miss'


class Block(PlayType):
    name = 'block'


class Give(PlayType):
    name = 'give'

    def result(self):
        giving = self.home if self.possession.has_possession == sel.road \
                           else self.road
        taking = self.road if giving == self.home else self.home

        self.player1 = giving.lines.weighted_choice()
        self.player2 = taking.lines.weighted_choice()

        self.possession.gain_possession(taking)


class Take(PlayType):
    name = 'take'

    def result(self):
        taking = self.home if self.possession.has_possession == self.road \
                           else self.road
        giving = self.road if taking == self.home else self.home

        self.player1 = taking.lines.weighted_choice()
        self.player2 = giving.lines.weighted_choice()

        self.possession.gain_possession(taking)


class Hit(PlayType):
    name = 'hit'

    def result(self):
        hitter = self.road if self.possession.has_possession == self.home \
                           else self.home
        hittee = self.home if hitter == self.road else self.road

        self.player1 = hitter.lines.weighted_choice()
        self.player2 = hittee.lines.weighted_choice()

        # Oversimpliciation
        if self.player1.overall > self.player2.overall:
            self.possession.gain_possession(hitter)
