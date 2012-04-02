from django.db import models


class NHLTeam(models.Model):
    city = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    abbr = models.CharField(max_length=3)

    def __unicode__(self):
        return '%s %s' % (self.city, self.name)

    class Meta:
        ordering = ('city', 'name')


class NHLSchedule(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=(('regular', 'Regular'),
                                                    ('pre', 'Preseason')))
    day = models.PositiveSmallIntegerField()
    game = models.PositiveSmallIntegerField()
    date = models.DateField()
    home = models.ForeignKey(NHLTeam, related_name='home_id')
    road = models.ForeignKey(NHLTeam, related_name='road_id')

    def __unicode__(self):
        return u'%s %s Day %d Game %d' % (self.name,
                                          self.type,
                                          self.day, self.game)

max_length=255
    class Meta:
        ordering = ('-name', 'type', 'game', 'day')


class NHLPlayer(models.Model):
    external_id = models.PositiveIntegerField(unique=True)
    team = models.ForeignKey(NHLTeam)
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
    salary = models.DecimalField(decimal_places=3, default=0.450, max_digits=10)
    seasons = models.PositiveIntegerField(default=0, max_length=2)
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
    it = models.PositiveSmallIntegerField()
    ck = models.PositiveSmallIntegerField(null=True)
    fg = models.PositiveSmallIntegerField(null=True)
    st = models.PositiveSmallIntegerField()
    di = models.PositiveSmallIntegerField()
    en = models.PositiveSmallIntegerField()
    du = models.PositiveSmallIntegerField()
    sp = models.PositiveSmallIntegerField()
    ag = models.PositiveSmallIntegerField()
    pa = models.PositiveSmallIntegerField()
    pc = models.PositiveSmallIntegerField()
    fo = models.PositiveSmallIntegerField()
    sc = models.PositiveSmallIntegerField()
    df = models.PositiveSmallIntegerField()
    ex = models.PositiveSmallIntegerField()
    ld = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


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

    def __unicode__(self):
        return u'%s %s (%s)' % (self.year,
                               self.team,
                               self.league)

    class Meta:
        ordering = ('-year', 'team', 'league')


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
    gaa = models.DecimalField(decimal_places=3, max_digits=10, null=True)
    svpct = models.DecimalField(decimal_places=3, max_digits=10, null=True)

    def __unicode__(self):
        return '%s %s (%S)' % (self.year, self.team, self.league)

    class Meta:
        ordering = ('-year', 'team', 'league')
