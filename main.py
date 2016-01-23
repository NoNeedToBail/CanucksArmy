import argparse

from modules import helpers
from modules import stats
from modules import roster


def main():
    arg_parser = argparse.ArgumentParser(description="Get prospect data from any league on the planet over a range of seasons")
    arg_parser.add_argument('--roster', action='store_true', help="Output roster list for the given league(s) and season(s)")
    arg_parser.add_argument('--stats', action='store_true', help="Output stats list for the given league(s) and season(s)")
    arg_parser.add_argument('leagues', type=helpers.comma_delimited_list, help="Comma-delimited list (no spaces) of leagues")
    arg_parser.add_argument('start_season', type=int, help="Earliest season for which to scrape data. Second year of the season (i.e. passing 2014 refers to the 2013-14 season)")
    arg_parser.add_argument('--range', type=int, help="Choose the latest season to parse to parse many seasons at once. Second year of the season (i.e. passing 2014 refers to the 2013-14 season)", required=False)

    args = arg_parser.parse_args()

    start_season = args.start_season
    end_season = args.range if args.range is not None else args.start_season

    if args.roster:
        results_array = []

        for league in args.leagues:
            for season in range(start_season, end_season + 1):
                roster.get_player_rosters(league, season, results_array)

        helpers.export_array_to_csv(results_array, '{0}-{1}_{2}_rosters.csv'.format(start_season, end_season, '-'.join(args.leagues)))

    if args.stats:
        results_array = []

        for league in args.leagues:
            for season in range(start_season, end_season + 1):
                stats.get_player_stats(league, season, results_array)

        helpers.export_array_to_csv(results_array, '{0}-{1}_{2}_stats.csv'.format(start_season, end_season, '-'.join(args.leagues)))

    print("Success!")


main()