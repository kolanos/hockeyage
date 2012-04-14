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


class NHLTeam(models.Model):
    city = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    acronym = models.CharField(max_length=3)
    conference = models.CharField(max_length=1, choices=(("E", "Eastern"), ("W", "Western")))
    division = models.CharField(max_length=1, choices=(('A', 'Atlantic'),
                                                       ('C', 'Central'),
                                                       ('NE', 'Northeast'),
                                                       ('NW', 'Northwest'),
                                                       ('P', 'Pacific'),
                                                       ('S', 'Southeast')))

    def __unicode__(self):
        return '%s %s' % (self.city, self.name)

    class Meta:
        db_table = 'nhl_teams'
        ordering = ['city', 'name']
        verbose_name = 'NHL Team'


class NHLSchedule(models.Model):
    name = models.CharField(max_length=6)
    type = models.CharField(max_length=7, choices=(('regular', 'Regular'),
                                                   ('pre', 'Preseason')))
    day = models.PositiveSmallIntegerField(max_length=3)
    game = models.PositiveSmallIntegerField(max_length=2)
    date = models.DateField()
    home = models.ForeignKey(NHLTeam, related_name='home_id')
    road = models.ForeignKey(NHLTeam, related_name='road_id')

    def __unicode__(self):
        return u'%s %s Day %d Game %d' % (self.name,
                                          self.type,
                                          self.day, self.game)

    class Meta:
        db_table = 'nhl_schedules'
        ordering = ['-name', 'type', 'game', 'day']
        verbose_name = 'NHL Schedule'


class NHLPlayer(models.Model):
    external_id = models.PositiveIntegerField(unique=True)
    nhl_team = models.ForeignKey(NHLTeam)
    name = models.CharField(max_length=100)
    no = models.PositiveSmallIntegerField()
    pos = models.CharField(max_length=30)
    shoots = models.CharField(max_length=1,
                              default='L',
                              choices=(('L', 'Left'),
                                       ('R', 'Right')))
    dob = models.DateField()
    pob = models.CharField(max_length=50)
    height = models.PositiveIntegerField(max_length=3)
    weight = models.PositiveIntegerField(max_length=3)
    salary = models.DecimalField(decimal_places=3, default=0.45, max_digits=10)
    seasons = models.PositiveIntegerField(default=0, max_length=3)
    drafted = models.CharField(max_length=50)
    signed = models.CharField(max_length=50)
    assets = models.TextField()
    flaws = models.TextField()
    potential = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    team_status = models.CharField(max_length=10,
                                   choices=(('pro', 'Pro'),
                                            ('farm', 'Farm'),
                                            ('prospect', 'Prospect'),
                                            ('retired', 'Retired')))
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
    player = models.ForeignKey(NHLPlayer)
    type = models.CharField(max_length=50,
                            choices=(('regular', 'Regular'),
                                     ('playoff', 'Playoff')))
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
    type = models.CharField(max_length=50,
                            choices=(('regular', 'Regular'),
                                     ('playoff', 'Playoff')))
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
