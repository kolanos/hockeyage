from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    @classmethod
    def create_user_profile(cls, sender, instance, created, **kwargs):
        if created:
            cls.objects.create(user=instance)

post_save.connect(UserProfile.create_user_profile, sender=User)


CONFERENCE_CHOICES = (("E", "Eastern"),
                      ("W", "Western"))

DIVISION_CHOICES = (('A', 'Atlantic'),
                    ('C', 'Central'),
                    ('NE', 'Northeast'),
                    ('NW', 'Northwest'),
                    ('P', 'Pacific'),
                    ('SE', 'Southeast'))


class NHLTeam(models.Model):
    city = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    acronym = models.CharField(max_length=3)
    conference = models.CharField(choices=CONFERENCE_CHOICES, max_length=1)
    division = models.CharField(choices=DIVISION_CHOICES, max_length=1)

    def __unicode__(self):
        return '%s %s' % (self.city, self.name)

    class Meta:
        db_table = 'nhl_teams'
        ordering = ['city', 'name']
        verbose_name = 'NHL Team'


SCHEDULE_TYPE_CHOICES = (('regular', 'Regular'),
                         ('pre', 'Preseason'))


class NHLSchedule(models.Model):
    name = models.CharField(max_length=6)
    type = models.CharField(choices=SCHEDULE_TYPE_CHOICES, max_length=7)
    day = models.PositiveSmallIntegerField(max_length=3)
    game = models.PositiveSmallIntegerField(max_length=2)
    date = models.DateField()
    home = models.ForeignKey(NHLTeam, related_name='home')
    road = models.ForeignKey(NHLTeam, related_name='road')

    def __unicode__(self):
        return u'%s %s Day %d Game %d' % (self.name,
                                          self.type,
                                          self.day, self.game)

    class Meta:
        db_table = 'nhl_schedules'
        ordering = ['-name', 'type', 'game', 'day']
        verbose_name = 'NHL Schedule'


SHOOT_CHOICES = (('L', 'Left'),
                  ('R', 'Right'))

TEAM_STATUS_CHOICES = (('pro', 'Pro'),
                       ('farm', 'Farm'),
                       ('prospect', 'Prospect'),
                       ('retired', 'Retired'))


class NHLPlayer(models.Model):
    external_id = models.PositiveIntegerField(unique=True)
    nhl_team = models.ForeignKey(NHLTeam, related_name='players')
    name = models.CharField(max_length=100)
    no = models.PositiveSmallIntegerField()
    pos = models.CharField(max_length=30)
    shoots = models.CharField(default='L', choices=SHOOT_CHOICES, max_length=1)
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
    team_status = models.CharField(choices=TEAM_STATUS_CHOICES, max_length=10)
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


SEASON_CHOICES = (('regular', 'Regular'),
                  ('playoff', 'Playoff'))


class NHLPlayerSkaterStat(models.Model):
    player = models.ForeignKey(NHLPlayer)
    season = models.CharField(choices=SEASON_CHOICES, max_length=50)
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
        return u'%s %s (%s)' % (self.year,
                               self.team,
                               self.league)

    class Meta:
        db_table = 'nhl_player_skater_stats'
        ordering = ['-year', 'team', 'league']
        verbose_name = 'NHL Skater Stat'


class NHLPlayerGoalieStat(models.Model):
    player = models.ForeignKey(NHLPlayer)
    season = models.CharField(choices=SEASON_CHOICES, max_length=50)
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
        return '%s %s (%S)' % (self.year, self.team, self.league)

    class Meta:
        db_table = 'nhl_player_goalie_stats'
        ordering = ['-year', 'team', 'league']
        verbose_name = 'NHL Goalie Stat'

class League(models.Model):
    name = models.CharField(max_length=255)
    acronym = models.CharField(max_length=6, unique=True)
    description = models.TextField()
    commissioner = models.ForeignKey(User)
    public = models.BooleanField(default=True)


class Season(models.Model):
    pass


class Match(models.Model):
    season = models.ForeignKey(Season)
    day = models.PositiveSmallIntegerField()
    game = models.PositiveSmallIntegerField()
    home = models.ForeignKey(Team, related_name='home')
    road = models.ForeignKey(Team, related_name='road')


POSITION_CHOICES = (('lw', 'Left Wing'),
                    ('c', 'Center'),
                    ('rw', 'Right Wing'),
                    ('ld', 'Left Defense'),
                    ('rd', 'Right Defense'),
                    ('g', 'Goalie'))


STATUS_CHOICES = (('pro', 'Pro'),
                  ('farm', 'Farm'),
                  ('prospect', 'Prospect'))


class Player(models.Model):
    league = models.ForeignKey(League)
    team = models.ForeignKey(Team)
    nhl_player = models.ForeignKey(NHLPlayer)
    pos = models.CharField(choices=POSITION_CHOICES, max_length=2)
    status = models.CharField(choices=STATUS_CHOICES, default='farm',
                              max_length=8)
    condition = models.PositiveSmallIntegerField(default=100, max_length=3)
    morale = models.PositiveSmallIntegerField(default=100, max_length=3)


LINE_STRENGTH_CHOICES = (('ev', 'Even Strength'),
                         ('pp', 'Power Play'),
                         ('pk', 'Penalty Kill'),
                         ('lm', 'Last Minute'),
                         ('ex', 'Extra'))


class Line(models.Model):
    match = models.ForeignKey(Match)
    team = models.ForeignKey(Team)
    strength = models.CharField(choices=LINE_STRENGTH_CHOICES, default='ev',
                                max_length=2)
    man = models.PositiveSmallIntegerField(default=5, max_length=1)
    number = models.PositiveSmallIntegerField(default=1, max_length=1)
    percent = models.PositiveSmallIntegerField(default=20, max_length=2)
    lw = models.ForeignKey(Player, related_name='lw')
    c = models.ForeignKey(Player, related_name='c')
    rw = models.ForeignKey(Player, related_name='rw')
    f = models.ForeignKey(Player, related_name='f')
    w = models.ForeignKey(Player, related_name='w')
    ld = models.ForeignKey(Player, related_name='ld')
    rd = models.foreignKey(Player, related_name='rd')


STRENGTH_CHOICES = (('ev', 'Even Strength'),
                    ('pp', 'Power Play'),
                    ('pk', 'Penalty Kill'))

ZONE_CHOICES = (('home', 'Home'),
                ('neutral', 'Neutral'),
                ('road', 'Road'))


class Play(models.Model):
    match = models.ForeignKey(Match)
    team = models.ForeignKey(Team)
    period = models.PositiveSmallIntegerField(max_length=1)
    strength = models.CharField(choices=STRENGTH_CHOICES, max_length=2)
    play = models.CharField()
    zone = models.CharField(choices=ZONE_CHOICES)
    player1 = models.ForeignKey(Player)
    player2 = models.ForeignKey(Player)
    player3 = models.ForeignKey(Player)
