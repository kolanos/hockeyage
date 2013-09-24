from django.core.management.base import BaseCommand, CommandError
from hockeyage.models import NHLTeam

# TODO: Move this to a config file
NHL_TEAMS = [
    dict(city='Anahein', name='Ducks', acronym='ANA', conference='W', division='P'),
    dict(city='Boston', name='Bruins', acronym='BOS', conference='E', division='A'),
    dict(city='Buffalo', name='Sabres', acronym='BUF', conference='E', division='A'),
    dict(city='Calgary', name='Flames', acronym='CGY', conference='W', division='P'),
    dict(city='Carolina', name='Hurricanes', acronym='CAR', conference='E', division='SE'),
    dict(city='Chicago', name='Blackhawks', acronym='CHI', conference='W', division='C'),
    dict(city='Colorado', name='Avalanche', acronym='COL', conference='W', division='P'),
    dict(city='Columbus', name='Blue Jackets', acronym='CLB', conference='W', division='C'),
    dict(city='Dallas', name='Stars', acronym='DAL', conference='W', division='P'),
    dict(city='Detroit', name='Red Wings', acronym='DET', conference='E', division='A'),
    dict(city='Edmonton', name='Oilers', acronym='EDM', conference='W', division='P'),
    dict(city='Florida', name='Panthers', acronym='FLA', conference='E', division='A'),
    dict(city='Los Angeles', name='Kings', acronym='LAK', conference='W', division='P'),
    dict(city='Minnesota', name='Wild', acronym='MIN', conference='W', division='P'),
    dict(city='Montreal', name= 'Canadiens', acronym='MTL', conference='E', division='A'),
    dict(city='Nashville', name= 'Predators', acronym='NSH', conference='W', division='C'),
    dict(city='New Jersey', name= 'Devils', acronym='NJD', conference='E', division='C'),
    dict(city='New York', name= 'Islanders', acronym='NYI', conference='E', division='C'),
    dict(city='New York', name= 'Rangers', acronym='NYR', conference='E', division='C'),
    dict(city='Ottawa', name= 'Senators', acronym='OTT', conference='E', division='A'),
    dict(city='Philadelphia', name= 'Flyers', acronym='PHI', conference='E', division='M'),
    dict(city='Phoenix', name= 'Coyotes', acronym='PHX', conference='W', division='P'),
    dict(city='Pittsburgh', name= 'Penguins', acronym='PIT', conference='E', division='M'),
    dict(city='San Jose', name= 'Sharks', acronym='SJS', conference='W', division='P'),
    dict(city='St. Louis', name= 'Blues', acronym='STL', conference='W', division='C'),
    dict(city='Tampa Bay', name= 'Lightning', acronym='TBL', conference='E', division='A'),
    dict(city='Toronto', name= 'Maple Leafs', acronym='TOR', conference='E', division='A'),
    dict(city='Vancouver', name= 'Canucks', acronym='VAN', conference='W', division='P'),
    dict(city='Washington', name= 'Capitals', acronym='WSH', conference='E', division='M'),
    dict(city='Winnipeg', name='Jets', acronym='WPG', conference='E', division='C'),
]


class Command(BaseCommand):
    args = '<...>'
    help = 'Load a list of NHL teams'

    def handle(self, *args, **options):
        for t in NHL_TEAMS:
            try:
                team, _ = NHLTeam.objects.get_or_create(**t)
            except e:
                raise CommandError(str(e))

            self.stdout.write('Successfully loaded NHL teams')
