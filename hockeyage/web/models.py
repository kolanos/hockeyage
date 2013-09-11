from peewee import CharField, DateField, ForeignKeyField, IntegerField, \
                   TextField

from hockeyage.web import db

from game.clock import format_time


class NHLTeam(db.Model):
    CONFERENCES = (('E', 'Eastern'),
                   ('W', 'Western'))

    DIVISIONS = (('A', 'Atlantic'),
                 ('C', 'Central'),
                 ('NE', 'Northeast'),
                 ('NW', 'Northwest'),
                 ('P', 'Pacific'),
                 ('SE', 'Southeast'))

    city = CharField(max_length=32)
    name = CharField(max_length=32)
    acronym = CharField(max_length=3)
    conference = CharField(choices=self.CONFERENCES, max_length=1)
    division = CharField(choices=self.DIVISIONS, max_length=1)

    def __unicode__(self):
        return '%s %s' % (self.city, self.name)

    class Meta:
        db_table = 'nhl_team'
        order_by = ('city', 'name')


class NHLSchedule(db.Model):
    SCHEDULE_TYPES = (('regular', 'Regular'),
                      ('pre', 'Preseason'))

    name = CharField(max_length=6)
    type = CharField(choices=self.SCHEDULE_TYPES, max_length=7)
    day = IntegerField(max_length=3)
    game = IntegerField(max_length=2)
    date = DateField()
    home = ForeignKeyField(NHLTeam, related_name='home')
    road = ForeignKeyField(NHLTeam, related_name='road')

    def __unicode__(self):
        return '%s %s Day %d Game %d' % (self.name,
                                         self.type,
                                         self.day,
                                         self.game)

    class Meta:
        db_table = 'nhl_schedule'
        order_by = ['-name', 'type', 'game', 'day']


class NHLPlayer(db.Model):
    SHOOTS = [('L', 'Left'),
              ('R', 'Right')]

    TEAM_STATUSES = [('pro', 'Pro'),
                     ('farm', 'Farm'),
                     ('prospect', 'Prospect'),
                     ('retired', 'Retired')]

    external_id = IntegerField(unique=True)
    team = ForeignKeyField(NHLTeam)
    name = CharField(max_length=100)
    no = IntegerField()
    pos = CharField(max_length=30)
    shoots = CharField(default='L', choices=self.SHOOTS, max_length=1)
    dob = DateField("Date of Birth")
    pob = CharField("Place of birth", max_length=50)
    height = IntegerField(max_length=3)
    weight = IntegerField(max_length=3)
    salary = IntegerField(default=550000)
    seasons = IntegerField(default=0, max_length=3)
    drafted = CharField(max_length=50)
    signed = CharField(max_length=50)
    assets = TextField()
    flaws = TextField()
    potential = CharField(max_length=255)
    status = CharField(max_length=50)
    team_status = CharField(choices=TEAM_STATUSES, max_length=10)
    it = IntegerField('Intensity', max_length=2)
    ck = IntegerField('Checking', max_length=2, null=True)
    fg = IntegerField('Fighting', max_length=2, null=True)
    st = IntegerField('Strength', max_length=2)
    di = IntegerField('Discipline', max_length=2)
    en = IntegerField('Endurance', max_length=2)
    du = IntegerField('Durability', max_length=2)
    sp = IntegerField('Speed', max_length=2)
    ag = IntegerField('Agility', max_length=2)
    pa = IntegerField('Passing', max_length=2)
    pc = IntegerField('Puck Control', max_length=2)
    fo = IntegerField('Faceoff', max_length=2)
    sc = IntegerField('Scoring', max_length=2)
    df = IntegerField('Defense', max_length=2)
    ex = IntegerField('Experience', max_length=2)
    ld = IntegerField('Leadership', max_length=2)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'nhl_player'
        order_by = ('name',)


class NHLPlayerSkaterStat(db.Model):
    SEASONS = [('regular', 'Regular'),
               ('playoff', 'Playoff')]

    player = ForeignKeyField(NHLPlayer)
    season = CharField(choices=self.SEASONS, max_length=50)
    year = CharField(max_length=50)
    team = CharField(max_length=50)
    league = CharField(max_length=50)
    gp = IntegerField(null=True)
    g = IntegerField(null=True)
    a = IntegerField(null=True)
    pts = IntegerField(null=True)
    d = IntegerField(null=True)
    pim = IntegerField(null=True)
    ppg = IntegerField(null=True)
    shg = IntegerField(null=True)
    gwg = IntegerField(null=True)
    shots = IntegerField(null=True)

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
        db_table = 'nhl_player_skater_stat'
        order_by = ('-year', 'team', 'league')


class NHLPlayerGoalieStat(db.Model):
    SEASONS = [('regular', 'Regular'),
               ('playoff', 'Playoff')]

    player = ForeignKeyField(NHLPlayer)
    season = CharField(choices=self.SEASONS, max_length=50)
    year = CharField(max_length=50)
    team = CharField(max_length=50)
    league = CharField(max_length=50)
    gpi = IntegerField(null=True)
    w = IntegerField(null=True)
    l = IntegerField(null=True)
    t = IntegerField(null=True)
    otl = IntegerField(null=True)
    min = IntegerField(null=True)
    so = IntegerField(null=True)
    ga = IntegerField(null=True)
    sha = IntegerField(null=True)

    @property
    def gaa(self):
        return '%.2f' % (self.ga / (self.min / 60.0))

    @property
    def svpct(self):
        return '%.3f' % (1 - (self.ga / float(self.sha)))

    def __unicode__(self):
        return '%s %s (%s)' % (self.year, self.team, self.league)

    class Meta:
        db_table = 'nhl_player_goalie_stat'
        order_by = ('-year', 'team', 'league')


class NHLMatchEvent(db.Model):
    season = CharField(max_length=8)
    game = IntegerField()
    number = IntegerField('#')
    period = IntegerField()
    strength = CharField(max_length=2, null=True)
    elapsed = IntegerField()
    remaining = IntegerField()
    type = CharField(max_length=50)
    zone = CharField(max_length=50, null=True)
    description = CharField(max_length=255, null=True)
    player1 = CharField(max_length=255, null=True)
    player2 = CharField(max_length=255, null=True)
    player3 = CharField(max_length=255, null=True)
    shot_type = CharField(max_length=50, null=True)
    distance = IntegerField()
    penalty = CharField(max_length=50, null=True)
    penalty_minutes = IntegerField()

    class Meta:
        db_table = 'nhl_match_event'
        order_by = ('game', 'number', 'period')


class League(db.Model):
    name = CharField(max_length=255)
    acronym = CharField(max_length=6, unique=True)
    description = TextField(null=True)
    commissioner = ForeignKeyField(User)
    public = BooleanField(default=True)

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.acronym)

    class Meta:
        order_by = ('name',)


class Team(db.Model):
    nhl_team = ForeignKeyField(NHLTeam)
    league = ForeignKeyField(League)
    gm = ForeignKeyField(User)

    def __unicode__(self):
        return '%s (%s)' % (unicode(self.nhl_team),
                               unicode(self.league))

    class Meta:
        order_by = ('league',)


class Season(db.Model):
    league = ForeignKeyField(League)
    year = IntegerField(default=1)

    def __unicode__(self):
        return '%s - Year %d' % (unicode(self.league), self.year)

    class Meta:
        order_by = ('-year',)


class Match(db.Model):
    season = ForeignKeyField(Season)
    day = IntegerField()
    game = IntegerField()
    home = ForeignKeyField(Team, related_name='home')
    road = ForeignKeyField(Team, related_name='road')

    def __unicode__(self):
        return 'Day %d Game %d (%s @ %s)' % (self.day,
                                             self.game,
                                             self.road,
                                             self.home)

    class Meta:
        order_by = ('day', 'game')


class Player(db.Model):
    POSITIONS = [('lw', 'Left Wing'),
                 ('c', 'Center'),
                 ('rw', 'Right Wing'),
                 ('ld', 'Left Defense'),
                 ('rd', 'Right Defense'),
                 ('g', 'Goalie')]

    STATUSES = [('pro', 'Pro'),
                ('farm', 'Farm'),
                ('prospect', 'Prospect')]

    league = ForeignKeyField(League)
    team = ForeignKeyField(Team)
    nhl_player = ForeignKeyField(NHLPlayer)
    pos = CharField(choices=self.POSITIONS, max_length=2)
    status = CharField(choices=self.STATUSES, default='farm', max_length=8)
    condition = IntegerField(default=100, max_length=3)
    morale = IntegerField(default=100, max_length=3)

    def __unicode__(self):
        return unicode(self.nhl_player)

    class Meta:
        order_by = ('status', 'pos')


class Line(db.Model):
    LINE_STRENGTHS = [('ev', 'Even Strength'),
                      ('pp', 'Power Play'),
                      ('pk', 'Penalty Kill'),
                      ('lm', 'Last Minute'),
                      ('ex', 'Extra')]

    match = ForeignKeyField(Match)
    team = ForeignKeyField(Team)
    strength = CharField(choices=LINE_STRENGTHS, default='ev',
                                max_length=2)
    man = IntegerField(default=5, max_length=1)
    number = IntegerField(default=1, max_length=1)
    percent = IntegerField(default=20, max_length=2)
    lw = ForeignKeyField(Player, null=True, related_name='lw')
    c = ForeignKeyField(Player, null=True, related_name='c')
    rw = ForeignKeyField(Player, null=True, related_name='rw')
    f = ForeignKeyField(Player, null=True, related_name='f')
    w = ForeignKeyField(Player, null=True, related_name='w')
    ld = ForeignKeyField(Player, null=True, related_name='ld')
    rd = ForeignKeyField(Player, null=True, related_name='rd')

    def __unicode__(self):
        return '%s %d %d' % (self.strength, self.man, self.number)

    class Meta:
        order_by = ('strength', 'man', '-number')


class Play(db.Model):
    STRENGTHS = [('ev', 'Even Strength'),
                 ('pp', 'Power Play'),
                 ('pk', 'Penalty Kill')]

    ZONES = [('home', 'Home'),
             ('neutral', 'Neutral'),
             ('road', 'Road')]

    match = ForeignKeyField(Match)
    team = ForeignKeyField(Team)
    period = IntegerField(max_length=1)
    clock = IntegerField()
    strength = CharField(choices=self.STRENGTHS, max_length=2)
    play = CharField(max_length=15)
    zone = CharField(choices=self.ZONES, max_length=7)
    player1 = ForeignKeyField(Player, null=True, related_name='player1')
    player2 = ForeignKeyField(Player, null=True, related_name='player2')
    player3 = ForeignKeyField(Player, null=True, related_name='player3')

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
        order_by = ('-period', '-clock')
