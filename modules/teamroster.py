import requests
from bs4 import BeautifulSoup

ID = 0
NAME = 1
DOB = 3
HOMETOWN = 4
HEIGHT = 5
WEIGHT = 6
SHOOTS = 7

METRIC = 0
IMPERIAL = 1


def get_team_roster(team_url, season, player_ids=[], results_array=[], multiple_teams=False):
    if len(results_array) == 0:
        results_array.append(['Name', 'Position', 'Season', 'League', 'Team', 'DOB', 'Hometown', 'Height', 'Weight', 'Shoots'])

    team_search_request = requests.get('http://www.eliteprospects.com/{0}'.format(team_url))
    team_page = BeautifulSoup(team_search_request.text, "html.parser")

    def global_nav_tag(tag):
        return tag.has_attr('id') and tag.attrs['id'] == 'globalnav'

    def team_name_tag(tag):
        return tag.has_attr('id') and tag.attrs['id'] == 'fontHeader'

    def league_name_tag(tag):
        return tag.has_attr('id') and tag.attrs['id'] == 'fontMainlink2'

    league = team_page.find(global_nav_tag).find_parent().previous_sibling.find(league_name_tag).text.strip()

    player_table = team_page.find(global_nav_tag).find_next_sibling('table')

    players = player_table.find_all('tr')

    team_name = team_page.find(team_name_tag).text

    """ Row 0 is the title row """
    for playerIndex in range(1, len(players)):
        player = players[playerIndex]
        player_stats = player.find_all('td')

        """ Only add to the array if the row isn't blank """
        if player_stats[ID].font is not None:
            continue

        try:
            name = player_stats[NAME].a.text.strip()
            position = player_stats[NAME].font.text.strip()[1:-1]
            dob = player_stats[DOB].text.strip()
            hometown = player_stats[HOMETOWN].a.text.strip()
            height = player_stats[HEIGHT].find_all('span')[METRIC].text
            weight = player_stats[WEIGHT].find_all('span')[METRIC].text
            shoots = player_stats[SHOOTS].text
        except IndexError:
            continue

        if not multiple_teams:
            player_id = name + dob + hometown
            if player_id in player_ids:
                index = player_ids.index(player_id)
                results_array[index][4] = 'multiple'
                continue

            player_ids.append(player_id)

        results_array.append([
            name,
            position,
            season,
            league,
            team_name,
            dob,
            hometown,
            height,
            weight,
            shoots
        ])