import datetime
import time

from valorant import current_season
from valorant import data

from .database import sql_statements as db


def get_match_last(puuid, n):
    """
    Get the n matches ago match of a player
    """

    return db.get_matches_by_puuid_last(puuid, n)[n - 1]


def get_match_elo(puuid, n):
    """
    Get the ELO of a match n matches ago.
    """

    return get_match_last(puuid, n).match_elo


def get_match_date(puuid, n):
    """
    Get the datch of a match n matches ago.
    """

    return get_match_last(puuid, n).match_start


def get_elo_over_matches(puuid, n):
    """
    Get the ELO diff over n matches
    """

    if n == len(db.get_matches_by_puuid(puuid)):
        n = n - 1

    return get_match_elo(puuid, 1) - get_match_elo(puuid, n + 1)


def get_end_of_match(match):
    """
    Get the end of a match
    """

    end_match = int(match.match_start) + (int(match.match_length) / 1000)

    return time.mktime(datetime.datetime.fromtimestamp(end_match).timetuple())


def get_wins_losses(puuid, n):
    """
    Get the number of wins and looses over n matches
    """

    wins = 0
    looses = 0

    from .log_setup import logger

    for i in range(1, n + 1):
        # debug output
        logger.info("get_wins_losses: " + str(i))

        match = get_match_last(puuid, i)
        if int(match.match_mmr_change) > 0:
            wins += 1
        else:
            looses += 1

    return wins, looses


def matches_within_time(puuid, n):
    """
    Find the number of matches within a timespan!
    """

    # days in seconds
    seconds = n * 24 * 60 * 60

    matches = 0
    max_matches = len(db.get_matches_by_puuid(puuid))

    while (time.time() - int(get_match_date(puuid, matches + 1))) < seconds:
        matches += 1
        if matches == max_matches:
            return matches
    return matches


def get_elo_over_time(puuid, n):
    """
    Get the ELO diff over n days
    """

    return get_elo_over_matches(puuid, matches_within_time(puuid, n))


def get_match_history(puuid, n):
    """
    Get the match history over n days
    """

    matches = matches_within_time(puuid, 1)

    output_string = ""

    for i in range(1, matches + 1):
        match = get_match_last(puuid, i)

        time = str(
            datetime.datetime.utcfromtimestamp(int(match.match_start)).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

        output_string = output_string + str(time)
        output_string = output_string + " - elo: " + match.match_mmr_change
        output_string = output_string + " = " + str(match.match_elo)
        output_string = output_string + "\n"

    return output_string


def get_highest_elo_match(puuid):
    """
    Get the highest ELO match of a player
    """

    # get all matches
    matches = db.get_matches_by_puuid(puuid)

    i = 0
    # get first match with elo
    while matches[i].match_elo is None:
        i += 1
    # set best match to first match with elo
    best_match = matches[i]

    # get match with highest elo
    for match in matches:
        # make sure match has elo
        if match.match_elo is not None:
            # check if match has higher elo
            if match.match_elo > best_match.match_elo:
                best_match = match

    # return match with highest elo
    return best_match


def get_highest_elo_match_season(puuid):
    """
    Get the highest ELO match of a player during the current season
    """

    season = data.COMPETETIVE_SEASONS[current_season()[0]]
    start = time.mktime(time.strptime(season["start"], "%Y-%m-%dT%H:%M:%SZ"))

    # get all matches
    matches = db.get_matches_by_puuid(puuid)

    # find the index of the first match of the season with elo
    i = 0
    while int(matches[i].match_start) < start or matches[i].match_elo is None:
        i += 1

    # set best match to first match of the season
    best_match = matches[i]

    # get match with highest elo of the season
    for match in matches:
        # make sure match has elo
        if match.match_elo is not None:
            # check if match is in season
            if int(match.match_start) > start:
                # check if match has higher elo
                if match.match_elo > best_match.match_elo:
                    best_match = match

    return best_match


if __name__ == "__main__":
    """
    for testing this module isolated
    """

    puuid = "d515e2d5-b50e-5c77-a79e-eeb46dbe488a"
    # print matches within last 1 day
    print(get_match_history(puuid, 1))
