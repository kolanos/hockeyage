from datetime import datetime

from peewee import CharField, DateField, DateTimeField, ForeignKeyField, \
                   IntegerField, TextField

from hockeyage.game.clock import format_time
from hockeyage.web import db


class NHLTeam(db.Model):
    CONFERENCES = [('E', 'Eastern'),
                   ('W', 'Western')]

    DIVISIONS = [('A', 'Atlantic'),
                 ('C', 'Central'),
                 ('M', 'Metropolitan'),
                 ('P', 'Pacific')]

    city = CharField()
    name = CharField()
    acronym = CharField()
    conference = CharField(choices=self.CONFERENCES)
    division = CharField(choices=self.DIVISIONS)

    class Meta:
        db_table = 'nhl_team'
        order_by = ('city', 'name')

    def __unicode__(self):
        return '{} {}'.format(self.city, self.name)


class NHLSchedule(db.Model):
    SCHEDULE_TYPES = [('regular', 'Regular'),
                      ('pre', 'Preseason')]

    name = CharField()
    type = CharField(choices=self.SCHEDULE_TYPES)
    day = IntegerField()
    game = IntegerField()
    date = DateField()
    home = ForeignKeyField(NHLTeam, related_name='home_games')
    road = ForeignKeyField(NHLTeam, related_name='road_games')

    class Meta:
        db_table = 'nhl_schedule'
        order_by = ['-name', 'type', 'game', 'day']

    def __unicode__(self):
        return '{} {} Day {} Game {}'.format(self.name,
                                             self.type,
                                             self.day,
                                             self.game)


class NHLPlayer(db.Model):
    SHOOTS = [('L', 'Left'),
              ('R', 'Right')]

    TEAM_STATUSES = [('pro', 'Pro'),
                     ('farm', 'Farm'),
                     ('prospect', 'Prospect'),
                     ('retired', 'Retired')]

    external_id = IntegerField(unique=True)
    team = ForeignKeyField(NHLTeam, related_name='players')
    name = CharField()
    no = IntegerField()
    pos = CharField()
    shoots = CharField(choices=self.SHOOTS, verbose_name='Shoots/Catches')
    dob = DateField(verbose_name='Date of Birth')
    pob = CharField(verbose_name='Place of Birth')
    height = IntegerField()
    weight = IntegerField()
    salary = IntegerField(null=True)
    seasons = IntegerField(default=0)
    drafted = CharField()
    signed = CharField()
    assets = TextField()
    flaws = TextField()
    potential = CharField()
    status = CharField()
    team_status = CharField(choices=TEAM_STATUSES)
    it = IntegerField(verbose_name='Intensity')
    ck = IntegerField(null=True, verbose_name='Checking')
    fg = IntegerField(null=True, verbose_name='Fighting')
    st = IntegerField(verbose_name='Strength')
    di = IntegerField(verbose_name='Discipline')
    en = IntegerField(verbose_name='Endurance')
    du = IntegerField(verbose_name='Durability')
    sp = IntegerField(verbose_name='Speed')
    ag = IntegerField(verbose_name='Agility')
    pa = IntegerField(verbose_name='Passing')
    pc = IntegerField(verbose_name='Puck Control')
    fo = IntegerField(verbose_name='Faceoff')
    sc = IntegerField(verbose_name='Scoring')
    df = IntegerField(verbose_name='Defense')
    ex = IntegerField(verbose_name='Experience')
    ld = IntegerField(verbose_name='Leadership')

    class Meta:
        db_table = 'nhl_player'
        order_by = ('name',)

    def __unicode__(self):
        return self.name


class NHLPlayerSkaterStat(db.Model):
    SEASONS = [('regular', 'Regular'),
               ('playoff', 'Playoff')]

    player = ForeignKeyField(NHLPlayer, related_name='skater_stats')
    season = CharField(choices=self.SEASONS)
    year = CharField()
    team = CharField()
    league = CharField()
    gp = IntegerField(null=True, verbose_name='GP')
    g = IntegerField(null=True)
    a = IntegerField(null=True)
    pts = IntegerField(null=True, verbose_name='PTS')
    pm = IntegerField(null=True, verbose_name='+/-')
    pim = IntegerField(null=True, verbose_name='PIM')
    ppg = IntegerField(null=True, verbose_name='PPG')
    shg = IntegerField(null=True, verbose_name='SHG')
    gwg = IntegerField(null=True, verbose_name='GWG')
    shots = IntegerField(null=True)

    class Meta:
        db_table = 'nhl_player_skater_stat'
        order_by = ('-year', 'team', 'league')

    def __unicode__(self):
        return '{} {} ({})'.format(self.year,
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

    player = ForeignKeyField(NHLPlayer, related_name='goalie_stats')
    season = CharField(choices=self.SEASONS)
    year = CharField()
    team = CharField()
    league = CharField()
    gpi = IntegerField(null=True, verbose_name='GPI')
    w = IntegerField(null=True)
    l = IntegerField(null=True)
    t = IntegerField(null=True)
    otl = IntegerField(null=True, verbose_name='OTL')
    min = IntegerField(null=True)
    so = IntegerField(null=True, verbose_name='SO')
    ga = IntegerField(null=True, verbose_name='GA')
    sha = IntegerField(null=True, verbose_name='SHA')

    class Meta:
        db_table = 'nhl_player_goalie_stat'
        order_by = ('-year', 'team', 'league')

    def __unicode__(self):
        return '{} {} ({})'.format(self.year, self.team, self.league)

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
    number = IntegerField(verbose_name='#')
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
    commissioner = ForeignKeyField(User, related_name='commish_leagues')
    public = BooleanField(default=True)
    password = CharField(null=True)

    class Meta:
        order_by = ('name',)

    def __unicode__(self):
        return '{} ({})'.format(self.name, self.acronym)


class Team(db.Model):
    nhl_team = ForeignKeyField(NHLTeam)
    league = ForeignKeyField(League, related_name='teams')
    gm = ForeignKeyField(User, related_name='managed_teams',
                         verbose_name='General Manager')

    class Meta:
        order_by = ('league',)

    def __unicode__(self):
        return '{} ({})'.format(self.nhl_team, self.league)


class Season(db.Model):
    league = ForeignKeyField(League, related_name='seasons')
    year = IntegerField(default=1)

    class Meta:
        order_by = ('-year',)

    def __unicode__(self):
        return '{} Year {}'.format(self.league, self.year)


class Match(db.Model):
    season = ForeignKeyField(Season, related_name='matches')
    day = IntegerField()
    game = IntegerField()
    home = ForeignKeyField(Team, related_name='home_games')
    road = ForeignKeyField(Team, related_name='road_games')

    class Meta:
        order_by = ('day', 'game')

    def __unicode__(self):
        return 'Day {} Game {} ({} @ {})'.format(self.day,
                                                 self.game,
                                                 self.road,
                                                 self.home)


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

    league = ForeignKeyField(League, related_name='players')
    team = ForeignKeyField(Team, related_name='players')
    nhl_player = ForeignKeyField(NHLPlayer)
    pos = CharField(choices=self.POSITIONS)
    status = CharField(choices=self.STATUSES, default='farm')
    condition = IntegerField(default=100)
    morale = IntegerField(default=100)

    class Meta:
        order_by = ('status', 'pos')

    def __unicode__(self):
        return unicode(self.nhl_player)

    @property
    def stats(self):
        if self.pos == 'g':
            return self.goalie_stats
        return self.skater_stats


class Roster(db.Model):
    match = ForeignKeyField(Match, related_name='rosters')
    team = ForeignKeyField(Team)
    player = ForeignKeyField(Player)
 

class Line(db.Model):
    LINE_STRENGTHS = [('ev', 'Even Strength'),
                      ('pp', 'Power Play'),
                      ('pk', 'Penalty Kill'),
                      ('lm', 'Last Minute'),
                      ('ex', 'Extra')]

    match = ForeignKeyField(Match, related_name='lines')
    team = ForeignKeyField(Team)
    strength = CharField(choices=LINE_STRENGTHS, default='ev')
    man = IntegerField(default=5)
    number = IntegerField(default=1)
    percent = IntegerField(default=20)
    lw = ForeignKeyField(Player, null=True, verbose_name='Left Wing')
    c = ForeignKeyField(Player, null=True, verbose_name='Center')
    rw = ForeignKeyField(Player, null=True, verbose_name='Right Wing')
    f = ForeignKeyField(Player, null=True, verbose_name='Forward')
    w = ForeignKeyField(Player, null=True, verbose_name='Wing')
    ld = ForeignKeyField(Player, null=True, verbose_name='Left Defense')
    rd = ForeignKeyField(Player, null=True, verbose_name='Right Defense')

    class Meta:
        order_by = ('strength', 'man', '-number')

    def __unicode__(self):
        return '{} {} {}'.format(self.strength, self.man, self.number)


class Play(db.Model):
    STRENGTHS = [('ev', 'Even Strength'),
                 ('pp', 'Power Play'),
                 ('pk', 'Penalty Kill')]

    ZONES = [('home', 'Home'),
             ('neutral', 'Neutral'),
             ('road', 'Road')]

    match = ForeignKeyField(Match, related_name='plays')
    team = ForeignKeyField(Team)
    period = IntegerField()
    clock = IntegerField()
    strength = CharField(choices=self.STRENGTHS)
    play = CharField()
    zone = CharField(choices=self.ZONES)
    player1 = ForeignKeyField(Player, null=True)
    player2 = ForeignKeyField(Player, null=True)
    player3 = ForeignKeyField(Player, null=True)

    class Meta:
        order_by = ('-period', '-clock')

    def __unicode__(self):
        return 'Period {} {} - {} - {} - {} - {}'.format(self.period,
                                                         self.elapsed,
                                                         self.strength,
                                                         self.play,
                                                         self.zone,
                                                         self.player1)

    @property
    def elapsed(self):
        return format_time(self.clock)


class SkaterStat(db.Model):
    match = ForeignKeyField(Match, related_name='skater_stats')
    player = ForeignKeyField(Player, related_name='skater_stats')
    team = ForeignKeyField(Team, related_name='skater_stats')
    g = IntegerField(null=True)
    a = IntegerField(null=True)
    d = IntegerField(null=True, verbose_name='+/-')
    pim = IntegerField(null=True, verbose_name='PIM')
    ppg = IntegerField(null=True, verbose_name='PPG')
    ppa = IntegerField(null=True, verbose_name='PPA')
    shg = IntegerField(null=True, verbose_name='SHG')
    sha = IntegerField(null=True, verbose_name='SHA')
    gwg = IntegerField(null=True, verbose_name='GWG')
    gtg = IntegerField(null=True, verbose_name='GTG')
    shots = IntegerField(null=True)
    toi = IntegerField(null=True, verbose_name='TOI')
    shifts = IntegerField(null=True)

    class Meta:
        db_table = 'skater_stat'
        order_by = ('team', '-toi')

    def __unicode__(self):
        return ''.join(['{}G, '.format(self.g) if self.g else '',
                        '{}A, '.format(self.a) if self.a else '',
                        '{}PIM'.format(self.pim) if self.pim else ''])
 

class GoalieStat(db.Model):
    match = ForeignKeyField(Match, related_name='goalie_stats')
    player = ForeignKeyField(Player, related_name='goalie_stats')
    team = ForeignKey(Team, related_name='goalie_stats')
    w = IntegerField(null=True)
    l = IntegerField(null=True)
    otl = IntegerField(null=True, verbose_name='OTL')
    min = IntegerField(null=True)
    so = IntegerField(null=True, verbose_name='SO')
    ga = IntegerField(null=True, verbose_name='GA')
    sha = IntegerField(null=True, verbose_name='SHA')

    class Meta:
        db_table = 'goalie_stat'
        order_by = ('team', '-min')

    def __unicode__(self):
        return ''.join(['W, ' if self.w else '',
                        'L, ' if self.l else '',
                        'OTL, ' if self.otl else '',
                        '{}SHA, '.format(self.sha) if self.sha else '',
                        '{}GA'.format(self.ga) if self.ga else '',
                        'SO' if self.so else ''])


class Pick(db.Model):
    owner = ForeignKeyField(Team, related_name='picks')
    team = ForeignKeyField(Team)
    season = ForeignKeyField(Season)
    round = IntegerField()
    overall = IntegerField(null=True)
    player = ForeignKeyField(Player, null=True)

    class Meta:
        order_by = ['season', 'overall', 'round']

    def __unicode__(self):
        return 'Year {} Round {}'.format(self.season.year, self.round)


class Trade(db.Model):
    STATUSES = [('created', 'Created'),
                ('proposed', 'Proposed'),
                ('accepted', 'Accepted'),
                ('rejected', 'Rejected'),
                ('approved', 'Approved'),
                ('disputed', 'Disputed'),
                ('withdrawn', 'Withdrawn')]

    from_team = ForeignKeyField(Team, related_name='trades_offered')
    to_team = ForeignKeyField(Team, related_name='trades_received')
    status = CharField(choies=self.STATUSES, default='created')
    created = DateTimeField(default=datetime.utcnow)
    proposed = DateTimeField(null=True)

    class Meta:
        order_by = ('-created',)

    def __unicode__(self):
        from_assets = []
        from_players = self.players.where(TradePlayer.from_team == self.from_team)
        from_assets.append(unicode(p.player) for p in from_players
        from_picks = self.picks.where(TradePick.from_team == self.from_team)
        from_assets.append(unicode(p.pick)) for p in from_picks

        to_assets = []
        to_players = self.players.where(TradePlayer.from_team == self.to_team)
        to_assets.append(unicode(p.player) for p in to_players
        to_picks = self.picks.where(TradePick.from_team == self.to_team)
        to_assets.append(unicode(p.pick)) for p in from_picks

        return '{} for {}'.format(', '.join(from_assets),
                                  ', '.join(to_assets))

    @property
    def is_valid(self):
        """
        Ensure that the teams involved in the trade still own the players and
        picks being traded.
        """
        for player in self.players:
            if player.from_team != player.player.team:
                return False
        for pick in self.picks:
            if pick.from_team != pick.pick.owner:
                return False
        return True


class TradePlayer(db.Model):
    trade = ForeignKeyField(Trade, related_name='players')
    from_team = ForeignKeyField(Team)
    player = ForeignKeyField(Player)

    class Meta:
        db_table = 'trade_player'

    def __unicode__(self):
        return unicode(self.player)


class TradePick(db.Model):
    trade = ForeignKeyField(Trade, related_name='picks')
    from_team = ForeignKeyField(Team)
    pick = ForeignKeyField(Pick)

    class Meta:
        db_table = 'trade_pick'

    def __unicode__(self):
        return unicode(self.pick)
