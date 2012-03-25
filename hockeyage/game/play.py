from hockeyage.util import probability


class Play(object):
    last_play = None

    def __init__(self):
        self.next_play = probability.weighted_choice_compile([('shot', 24),
                                                              ('stop', 20),
                                                              ('hit', 14),
                                                              ('penalty', 10),
                                                              ('block', 10),
                                                              ('miss', 9),
                                                              ('give', 6),
                                                              ('take', 5),
                                                              ('goal', 2)])

    def __call__(self):
        if self.last_play is None:
            self.last_play = 'face'
        else:
            self.last_play = getattr(self, self.last_play)()
        return self.last_play

    def start(self):
        return 'face'

    def end(self):
        return 'start'

    def stop(self):
        return 'face'

    def goal(self):
        return 'face'

    def penalty(self):
        return 'face'

    def face(self):
        return self.next_play()

    def shot(self):
        return self.next_play()

    def miss(self):
        return self.next_play()

    def block(self):
        return self.next_play()

    def give(self):
        return self.next_play()

    def take(self):
        return self.next_play()

    def hit(self):
        return self.next_play()
