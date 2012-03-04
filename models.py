from mongoengine import *

class NHLPlayer(Document):
    external_id = IntField(unique=True)
    team = ReferenceField('NHLTeam')
    name = StringField()
    no = IntField()
    pos = ListField(StringField(choices=('LW','C','RW','LD','RD','G')))
    shoots = StringField(default='L', choices=('L','R'))
    dob = DateTimeField()
    pob = StringField()
    height = IntField()
    weight = IntField()
    salary = DecimalField(default=0.450)
    seasons = IntField(default=0)
    drafted = StringField()
    signed = StringField()
    assets = StringField()
    flaws = StringField()
    potential = StringField()
    status = StringField()
    team_status = StringField(choices=('pro','farm','prospect','retired'))
    it = IntField()
    ck = IntField()
    fg = IntField()
    st = IntField()
    di = IntField()
    en = IntField()
    du = IntField()
    sp = IntField()
    ag = IntField()
    pa = IntField()
    pc = IntField()
    fo = IntField()
    sc = IntField()
    df = IntField()
    ex = IntField()
    ld = IntField()
    meta = {'collection': 'nhl_players'}

    def __unicode__(self):
        return self.name

class NHLPlayerGoalie(NHLPlayer):
    pos = ['G']
    ck = None
    fg = None
    stats = ListField(EmbeddedDocumentField('NHLPlayerGoalieStat'))

class NHLPlayerGoalieStat(EmbeddedDocument):
    type = StringField(choices=('regular','playoff'))
    year = StringField()
    team = StringField()
    league = StringField()
    gpi = IntField()
    w = IntField()
    l = IntField()
    t = IntField()
    otl = IntField()
    min = IntField()
    so = IntField()
    ga = IntField()
    sha = IntField()
    gaa = DecimalField()
    svpct = DecimalField()

class NHLPlayerSkater(NHLPlayer):
    pos = ListField(StringField(choices=('LW','C','RW','LD','RD')))
    stats = ListField(EmbeddedDocumentField('NHLPlayerSkaterStat'))

class NHLPlayerSkaterStat(EmbeddedDocument):
    type = StringField(choices=('regular','playoff'))
    year = StringField()
    team = StringField()
    league = StringField()
    gp = IntField()
    g = IntField()
    a = IntField()
    pts = IntField()
    d = IntField()
    pim = IntField()
    ppg = IntField()
    shg = IntField()
    gwg = IntField()
    shots = IntField()

class NHLSchedule(Document):
    name = StringField()
    type = StringField(choices=('regular','pre'))
    day = IntField()
    game = IntField()
    date = DateTimeField()
    home = ReferenceField('NHLTeam')
    road = ReferenceField('NHLTeam')
    meta = {'collection': 'nhl_schedules'}

class NHLTeam(Document):
    city = StringField()
    name = StringField()
    abbr = StringField()
    meta = {
        'collection': 'nhl_teams',
        'ordering': ['city', 'name']
    }

    def __unicode__(self):
        return '%s %s' % (self.city, self.name)

