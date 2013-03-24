from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from game.clock import format_time


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    @classmethod
    def create_user_profile(cls, sender, instance, created, **kwargs):
        if created:
            cls.objects.create(user=instance)

post_save.connect(UserProfile.create_user_profile, sender=User)


class NHLTeam(models.Model):
    CONFERENCES = (('E', 'Eastern'),
                   ('W', 'Western'))

    DIVISIONS = (('A', 'Atlantic'),
                 ('C', 'Central'),
                 ('NE', 'Northeast'),
                 ('NW', 'Northwest'),
                 ('P', 'Pacific'),
                 ('SE', 'Southeast'))

    city = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    acronym = models.CharField(max_length=3)
    conference = models.CharField(choices=self.CONFERENCES, max_length=1)
    division = models.CharField(choices=self.DIVISIONS, max_length=1)

    def __unicode__(self):
        return '%s %s' % (self.city, self.name)

    class Meta:
        db_table = 'nhl_teams'
        ordering = ['city', 'name']
        verbose_name = 'NHL Team'

class NHLSchedule(models.Model):
    SCHEDULE_TYPES = (('regular', 'Regular'),
                      ('pre', 'Preseason'))

    name = models.CharField(max_length=6)
    type = models.CharField(choices=self.SCHEDULE_TYPES, max_length=7)
    day = models.PositiveSmallIntegerField(max_length=3)
    game = models.PositiveSmallIntegerField(max_length=2)
    date = models.DateField()
    home = models.ForeignKey(NHLTeam, related_name='home')
    road = models.ForeignKey(NHLTeam, related_name='road')

    def __unicode__(self):
        return '%s %s Day %d Game %d' % (self.name,
                                         self.type,
                                         self.day,
                                         self.game)

    class Meta:
        db_table = 'nhl_schedules'
        ordering = ['-name', 'type', 'game', 'day']
        verbose_name = 'NHL Schedule'




class NHLPlayer(models.Model):
    SHOOTS = (('L', 'Left'),
              ('R', 'Right'))

    TEAM_STATUSES = (('pro', 'Pro'),
                     ('farm', 'Farm'),
                     ('prospect', 'Prospect'),
                     ('retired', 'Retired'))

    external_id = models.PositiveIntegerField(unique=True)
    team = models.ForeignKey(NHLTeam)
    name = models.CharField(max_length=100)
    no = models.PositiveSmallIntegerField()
    pos = models.CharField(max_length=30)
    shoots = models.CharField(default='L', choices=self.SHOOTS, max_length=1)
    dob = models.DateField("Date of Birth")
    pob = models.CharField("Place of birth", max_length=50)
    height = models.PositiveIntegerField(max_length=3)
    weight = models.PositiveIntegerField(max_length=3)
    salary = models.PositiveIntegerField(default=550000)
    seasons = models.PositiveIntegerField(default=0, max_length=3)
    drafted = models.CharField(max_length=50)
    signed = models.CharField(max_length=50)
    assets = models.TextField()
    flaws = models.TextField()
    potential = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    team_status = models.CharField(choices=TEAM_STATUSES, max_length=10)
    it = models.PositiveSmallIntegerField('Intensity', max_length=2)
    ck = models.PositiveSmallIntegerField('Checking', max_length=2, null=True)
    fg = models.PositiveSmallIntegerField('Fighting', max_length=2, null=True)
    st = models.PositiveSmallIntegerField('Strength', max_length=2)
    di = models.PositiveSmallIntegerField('Discipline', max_length=2)
    en = models.PositiveSmallIntegerField('Endurance', max_length=2)
    du = models.PositiveSmallIntegerField('Durability', max_length=2)
    sp = models.PositiveSmallIntegerField('Speed', max_length=2)
    ag = models.PositiveSmallIntegerField('Agility', max_length=2)
    pa = models.PositiveSmallIntegerField('Passing', max_length=2)
    pc = models.PositiveSmallIntegerField('Puck Control', max_length=2)
    fo = models.PositiveSmallIntegerField('Faceoff', max_length=2)
    sc = models.PositiveSmallIntegerField('Scoring', max_length=2)
    df = models.PositiveSmallIntegerField('Defense', max_length=2)
    ex = models.PositiveSmallIntegerField('Experience', max_length=2)
    ld = models.PositiveSmallIntegerField('Leadership', max_length=2)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'nhl_players'
        ordering = ['name']
        verbose_name = 'NHL Player'


class NHLPlayerSkaterStat(models.Model):
    SEASONS = (('regular', 'Regular'),
               ('playoff', 'Playoff'))

    player = models.ForeignKey(NHLPlayer)
    season = models.CharField(choices=self.SEASONS, max_length=50)
    year = models.CharField(max_length=50)
    team = models.CharField(max_length=50)
    league = models.CharField(max_length=50)
    gp = models.PositiveIntegerField(null=True)
    g = models.PositiveIntegerField(null=True)
    a = models.PositiveIntegerField(null=True)
    pts = models.PositiveIntegerField(null=True)
    d = models.IntegerField(null=True)
    pim = models.PositiveIntegerField(null=True)
    ppg = models.PositiveIntegerField(null=True)
    shg = models.PositiveIntegerField(null=True)
    gwg = models.PositiveIntegerField(null=True)
    shots = models.PositiveIntegerField(null=True)

    @property
    def ptspgp(self):
        return '%.2f' % (float(self.gp) / self.pts)

    @property
    def shotpct(self):
        return '%.3f' % (float(self.shots) / self.g)

    def __unicode__(self):
        return '%s %s (%s)' % (self.year,
                               self.team,
                               self.league)

    class Meta:
        db_table = 'nhl_player_skater_stats'
        ordering = ['-year', 'team', 'league']
        verbose_name = 'NHL Skater Stat'


class NHLPlayerGoalieStat(models.Model):
    SEASONS = (('regular', 'Regular'),
               ('playoff', 'Playoff'))

    player = models.ForeignKey(NHLPlayer)
    season = models.CharField(choices=self.SEASONS, max_length=50)
    year = models.CharField(max_length=50)
    team = models.CharField(max_length=50)
    league = models.CharField(max_length=50)
    gpi = models.PositiveIntegerField(null=True)
    w = models.PositiveIntegerField(null=True)
    l = models.PositiveIntegerField(null=True)
    t = models.PositiveIntegerField(null=True)
    otl = models.PositiveIntegerField(null=True)
    min = models.PositiveIntegerField(null=True)
    so = models.PositiveIntegerField(null=True)
    ga = models.PositiveIntegerField(null=True)
    sha = models.PositiveIntegerField(null=True)

    @property
    def gaa(self):
        return '%.2f' % (self.ga / (self.min / 60.0))

    @property
    def svpct(self):
        return '%.3f' % (1 - (self.ga / float(self.sha)))

    def __unicode__(self):
        return '%s %s (%s)' % (self.year, self.team, self.league)

    class Meta:
        db_table = 'nhl_player_goalie_stats'
        ordering = ['-year', 'team', 'league']
        verbose_name = 'NHL Goalie Stat'


class NHLMatchEvent(models.Model):
    season = models.CharField(max_length=8)
    game = models.PositiveIntegerField()
    number = models.PositiveSmallIntegerField('#')
    period = models.PositiveSmallIntegerField()
    strength = models.CharField(max_length=2, null=True)
    elapsed = models.PositiveIntegerField()
    remaining = models.PositiveIntegerField()
    type = models.CharField(max_length=50)
    zone = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=255, null=True)
    player1 = models.CharField(max_length=255, null=True)
    player2 = models.CharField(max_length=255, null=True)
    player3 = models.CharField(max_length=255, null=True)
    shot_type = models.CharField(max_length=50, null=True)
    distance = models.PositiveIntegerField()
    penalty = models.CharField(max_length=50, null=True)
    penalty_minutes = models.PositiveSmallIntegerField()


class League(models.Model):
    name = models.CharField(max_length=255)
    acronym = models.CharField(max_length=6, unique=True)
    description = models.TextField(null=True)
    commissioner = models.ForeignKey(User)
    public = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.acronym)

    class Meta:
        db_table = 'leagues'
        ordering = ('name',)


class Team(models.Model):
    nhl_team = models.ForeignKey(NHLTeam)
    league = models.ForeignKey(League)
    gm = models.ForeignKey(User)

    def __unicode__(self):
        return '%s (%s)' % (unicode(self.nhl_team),
                               unicode(self.league))

    class Meta:
        db_table = 'teams'
        ordering = ['league']


class Season(models.Model):
    league = models.ForeignKey(League)
    year = models.PositiveSmallIntegerField(default=1)

    def __unicode__(self):
        return '%s - Year %d' % (unicode(self.league), self.year)

    class Meta:
        db_table = 'seasons'
        ordering = ['-year']


class Match(models.Model):
    season = models.ForeignKey(Season)
    day = models.PositiveSmallIntegerField()
    game = models.PositiveSmallIntegerField()
    home = models.ForeignKey(Team, related_name='home')
    road = models.ForeignKey(Team, related_name='road')

    def __unicode__(self):
        return 'Day %d Game %d (%s @ %s)' % (self.day,
                                             self.game,
                                             self.road,
                                             self.home)

    class Meta:
        db_table = 'matches'
        ordering = ['day', 'game']


class Player(models.Model):
    POSITIONS = (('lw', 'Left Wing'),
                 ('c', 'Center'),
                 ('rw', 'Right Wing'),
                 ('ld', 'Left Defense'),
                 ('rd', 'Right Defense'),
                 ('g', 'Goalie'))

    STATUSES = (('pro', 'Pro'),
                ('farm', 'Farm'),
                ('prospect', 'Prospect'))

    league = models.ForeignKey(League)
    team = models.ForeignKey(Team)
    nhl_player = models.ForeignKey(NHLPlayer)
    pos = models.CharField(choices=self.POSITIONS, max_length=2)
    status = models.CharField(choices=self.STATUSES, default='farm',
                              max_length=8)
    condition = models.PositiveSmallIntegerField(default=100, max_length=3)
    morale = models.PositiveSmallIntegerField(default=100, max_length=3)

    def __unicode__(self):
        return unicode(self.nhl_player)

    class Meta:
        db_table = 'players'
        ordering = ['status', 'pos']


class Line(models.Model):
    LINE_STRENGTHS = (('ev', 'Even Strength'),
                      ('pp', 'Power Play'),
                      ('pk', 'Penalty Kill'),
                      ('lm', 'Last Minute'),
                      ('ex', 'Extra'))

    match = models.ForeignKey(Match)
    team = models.ForeignKey(Team)
    strength = models.CharField(choices=LINE_STRENGTHS, default='ev',
                                max_length=2)
    man = models.PositiveSmallIntegerField(default=5, max_length=1)
    number = models.PositiveSmallIntegerField(default=1, max_length=1)
    percent = models.PositiveSmallIntegerField(default=20, max_length=2)
    lw = models.ForeignKey(Player, null=True, related_name='lw')
    c = models.ForeignKey(Player, null=True, related_name='c')
    rw = models.ForeignKey(Player, null=True, related_name='rw')
    f = models.ForeignKey(Player, null=True, related_name='f')
    w = models.ForeignKey(Player, null=True, related_name='w')
    ld = models.ForeignKey(Player, null=True, related_name='ld')
    rd = models.ForeignKey(Player, null=True, related_name='rd')

    def __unicode__(self):
        return '%s %d %d' % (self.strength, self.man, self.number)

    class Meta:
        db_table = 'lines'
        ordering = ['strength', 'man', '-number']


class Play(models.Model):
    STRENGTHS = (('ev', 'Even Strength'),
                 ('pp', 'Power Play'),
                 ('pk', 'Penalty Kill'))

    ZONES = (('home', 'Home'),
             ('neutral', 'Neutral'),
             ('road', 'Road'))

    match = models.ForeignKey(Match)
    team = models.ForeignKey(Team)
    period = models.PositiveSmallIntegerField(max_length=1)
    clock = models.PositiveSmallIntegerField()
    strength = models.CharField(choices=self.STRENGTHS, max_length=2)
    play = models.CharField(max_length=15)
    zone = models.CharField(choices=self.ZONES, max_length=7)
    player1 = models.ForeignKey(Player, related_name='player1')
    player2 = models.ForeignKey(Player, null=True, related_name='player2')
    player3 = models.ForeignKey(Player, null=True, related_name='player3')

    def __unicode__(self):
        return 'Period %d %s - %s - %s - %s - %s' % (self.period,
                                                     self.elapsed,
                                                     self.strength,
                                                     self.play,
                                                     self.zone,
                                                     self.player1)

    @property
    def elapsed(self):
        return format_time(self.clock)

    class Meta:
        db_table = 'plays'
        ordering = ['-period', '-clock']
