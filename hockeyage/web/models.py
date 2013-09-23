from peewee import CharField, DateField, ForeignKeyField, IntegerField, \
                   TextField

from hockeyage.web import db

from game.clock import format_time


class NHLTeam(db.Model):
    CONFERENCES = [('E', 'Eastern'),
                   ('W', 'Western')]

    DIVISIONS = [('A', 'Atlantic'),
                 ('C', 'Central'),
                 ('M', 'Metropolitan'),
                 ('P', 'Pacific')]

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
    SCHEDULE_TYPES = [('regular', 'Regular'),
                      ('pre', 'Preseason')]

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
    name = CharField()
    no = IntegerField()
    pos = CharField()
    shoots = CharField('Shoots/Catches', choices=self.SHOOTS, default='L')
    dob = DateField('Date of Birth')
    pob = CharField('Place of birth')
    height = IntegerField()
    weight = IntegerField()
    salary = IntegerField(default=550000)
    seasons = IntegerField(default=0)
    drafted = CharField()
    signed = CharField()
    assets = TextField()
    flaws = TextField()
    potential = CharField()
    status = CharField()
    team_status = CharField(choices=TEAM_STATUSES)
    it = IntegerField('Intensity')
    ck = IntegerField('Checking', null=True)
    fg = IntegerField('Fighting', null=True)
    st = IntegerField('Strength')
    di = IntegerField('Discipline')
    en = IntegerField('Endurance')
    du = IntegerField('Durability')
    sp = IntegerField('Speed')
    ag = IntegerField('Agility')
    pa = IntegerField('Passing')
    pc = IntegerField('Puck Control')
    fo = IntegerField('Faceoff')
    sc = IntegerField('Scoring')
    df = IntegerField('Defense')
    ex = IntegerField('Experience')
    ld = IntegerField('Leadership')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'nhl_player'
        order_by = ('name',)


class NHLPlayerSkaterStat(db.Model):
    SEASONS = [('regular', 'Regular'),
               ('playoff', 'Playoff')]

    player = ForeignKeyField(NHLPlayer)
    season = CharField(choices=self.SEASONS)
    year = CharField()
    team = CharField()
    league = CharField()
    gp = IntegerField('GP', null=True)
    g = IntegerField(null=True)
    a = IntegerField(null=True)
    pts = IntegerField('PTS', null=True)
    pm = IntegerField('+/-', null=True)
    pim = IntegerField('PIM', null=True)
    ppg = IntegerField('PPG', null=True)
    shg = IntegerField('SHG', null=True)
    gwg = IntegerField('GWG', null=True)
    shots = IntegerField(null=True)

    class Meta:
        db_table = 'nhl_player_skater_stat'
        order_by = ('-year', 'team', 'league')

    def __unicode__(self):
        return '%s %s (%s)' % (self.year,
                               self.team,
                               self.league)

    @property
    def ptspgp(self):
        if self.gp and self.pts:
            return '%.2f' % float(self.gp) / self.pts
        return None

    @property
    def shotpct(self):
        if self.shots and self.g:
            return '%.3f' % float(self.shots) / self.g
        return None


class NHLPlayerGoalieStat(db.Model):
    SEASONS = [('regular', 'Regular'),
               ('playoff', 'Playoff')]

    player = ForeignKeyField(NHLPlayer)
    season = CharField(choices=self.SEASONS, max_length=50)
    year = CharField(max_length=50)
    team = CharField(max_length=50)
    league = CharField(max_length=50)
    gpi = IntegerField('GPI', null=True)
    w = IntegerField(null=True)
    l = IntegerField(null=True)
    t = IntegerField(null=True)
    otl = IntegerField('OTL', null=True)
    min = IntegerField(null=True)
    so = IntegerField('SO', null=True)
    ga = IntegerField('GA', null=True)
    sha = IntegerField('SHA', null=True)

    class Meta:
        db_table = 'nhl_player_goalie_stat'
        order_by = ('-year', 'team', 'league')

    def __unicode__(self):
        return '%s %s (%s)' % (self.year, self.team, self.league)

    @property
    def gaa(self):
        if self.ga and self.min:
            return '%.2f' % self.ga / (self.min / 60.0)
        return None

    @property
    def svpct(self):
        if self.ga and self.sha:
            return '%.3f' % (1 - self.ga / float(self.sha))
        return None


class NHLMatchEvent(db.Model):
    season = CharField()
    game = IntegerField()
    number = IntegerField('#')
    period = IntegerField()
    strength = CharField(null=True)
    elapsed = IntegerField()
    remaining = IntegerField()
    type = CharField()
    zone = CharField(null=True)
    description = CharField(null=True)
    player1 = CharField(null=True)
    player2 = CharField(null=True)
    player3 = CharField(null=True)
    shot_type = CharField(null=True)
    distance = IntegerField()
    penalty = CharField(null=True)
    penalty_minutes = IntegerField()

    class Meta:
        db_table = 'nhl_match_event'
        order_by = ('game', 'number', 'period')


class League(db.Model):
    name = CharField()
    acronym = CharField(unique=True)
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
