import csv
from dateutil.parser import parse
from mongoengine import connect
from models import *

connect('hockeyage')

teams = NHLTeam.objects.all()
teams = {1: teams[0], 2: teams[29], 3: teams[1], 4: teams[2], 5: teams[3], 
         6: teams[4], 7: teams[5], 8: teams[6], 9: teams[7], 10: teams[8], 
         11: teams[9], 12: teams[10], 13: teams[11], 14: teams[12], 15: teams[13], 
         16: teams[14], 17: teams[15], 18: teams[16], 19: teams[17], 20: teams[18], 
         21: teams[19], 22: teams[20], 23: teams[21], 24: teams[22], 25: teams[23], 
         26: teams[24], 27: teams[25], 28: teams[26], 29: teams[27], 30: teams[28]}

def nodupes(seq): 
    nodupes = []
    [nodupes.append(i) for i in seq if not nodupes.count(i)]
    return nodupes

def pos(pos, shoots):
    pos = pos.split('/')
    for i, p in enumerate(pos):
        if p == 'D' and shoots == 'L':
            del pos[i]
            pos = pos + ['LD','RD']
        elif p == 'D' and shoots == 'R':
            del pos[i]
            pos = pos + ['RD','LD']
        elif p == 'W' and shoots == 'L':
            del pos[i]
            pos = pos + ['LW','RW']
        elif p == 'W' and shoots == 'R':
            del pos[i]
            pos = pos + ['RW','LW']
        elif p == 'F':
            del pos[i]
            pos = pos + ['LW','C','RW']
    nodupes(pos)
    return pos



rows = csv.reader(open('csv/hockeyage.nhl_players.csv'), delimiter=';', quotechar='"')
for row in rows:
    if 'G' in row[5]:
        player = NHLPlayerGoalie()
    else:
        player = NHLPlayerSkater()
    player.external_id = row[1]
    if row[2] != 'NULL':
        t = int(row[2])
        player.team = teams[t]
    else:
        player.team = None
    player.name = row[3] if row[3] != 'NULL' else None
    player.no = row[4] if row[4] != 'NULL' else None
    player.pos = pos(row[5], row[6]) if row[5] != 'NULL' else 'L'
    player.shoots = row[6] if row[6] != 'NULL' else None
    player.dob = parse(row[7]) if row[7] != 'NULL' else None
    player.pob = row[8] if row[8] != 'NULL' else None
    player.height = row[9] if row[9] != 'NULL' else None
    player.weight = row[10] if row[10] != 'NULL' else None
    player.salary = row[11] if row[11] != 'NULL' else None
    player.seasons = row[12] if row[12] != 'NULL' else None
    player.drafted = row[13] if row[13] != 'NULL' else None
    player.signed = row[14] if row[14] != 'NULL' else None
    player.assets = row[15] if row[15] != 'NULL' else None
    player.flaws = row[16] if row[16] != 'NULL' else None
    player.potential = row[17] if row[17] != 'NULL' else None
    player.status = row[18] if row[18] != 'NULL' else None
    player.team_status = row[19] if row[19] != 'NULL' else None
    player.it = row[20] if row[20] != 'NULL' else None
    player.ck = row[21] if row[21] != 'NULL' else None
    player.fg = row[22] if row[22] != 'NULL' else None
    player.st = row[23] if row[23] != 'NULL' else None
    player.di = row[24] if row[24] != 'NULL' else None
    player.du = row[25] if row[25] != 'NULL' else None
    player.sp = row[26] if row[26] != 'NULL' else None
    player.ag = row[27] if row[27] != 'NULL' else None
    player.pa = row[28] if row[28] != 'NULL' else None
    player.pc = row[29] if row[29] != 'NULL' else None
    player.fo = row[30] if row[30] != 'NULL' else None
    player.sc = row[31] if row[31] != 'NULL' else None
    player.df = row[32] if row[32] != 'NULL' else None
    player.ex = row[33] if row[33] != 'NULL' else None
    player.ld = row[34] if row[34] != 'NULL' else None
    player.save()

