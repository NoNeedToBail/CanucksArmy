import requests
import html5lib
from modules import teamroster

ID = 0
NAME = 1
DOB = 3
HOMETOWN = 4
HEIGHT = 5
WEIGHT = 6
SHOOTS = 7

METRIC = 0
IMPERIAL = 1

""" ROSTER PARSER """


def get_player_rosters(league, season, results_array=None, multiple_teams=False):
    league = str(league)
    season = str(season)

    if results_array is None or len(results_array) == 0:
        results_array.append(['Name', 'Position', 'Season', 'League', 'Team', 'DOB', 'Hometown', 'Height', 'Weight', 'Shoots'])
    player_ids = []
    team_urls = []

    """ Get the league link """

    team_search_url = "http://www.eliteprospects.com/standings.php?league={0}&startdate={1}".format(league, str(int(season) - 1))
    team_search_request = requests.get(team_search_url)

    # All tag names have this prepended to them
    html_prefix = '{http://www.w3.org/1999/xhtml}'
    team_search_page = html5lib.parse(team_search_request.text)
    # /html/body/div/table[3]/tbody/tr/td[5]/table[3]
    team_table = team_search_page.find(
        './{0}body/{0}div/{0}table[3]/{0}tbody/{0}tr/{0}td[5]/{0}table[3]'.format(html_prefix))

    teams = team_table.findall('.//{0}tbody/{0}tr/{0}td[2]/{0}a'.format(html_prefix))

    on_first_row = True

    for team in teams:
        if on_first_row:
            on_first_row = False
            continue
        team_urls.append(team.attrib['href'])

    """ Get the players """

    for team_url in team_urls:
        teamroster.get_team_roster(team_url, season, league, player_ids, results_array, multiple_teams)

    return results_array
