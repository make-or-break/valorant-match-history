import time

from match_crawler.database import sql_statements as db


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

    return get_match_elo(puuid, 1) - get_match_elo(puuid, n + 1)


def matches_within_time(puuid, n):
    """
    Finde the number of matches within a timespan!
    """

    # days in seconds
    seconds = n * 24 * 60 * 60

    matches = 0

    while time.time() - int(get_match_date(puuid, matches + 1)) < seconds:
        matches += 1

    return matches


def get_elo_over_time(puuid, n):
    """
    Get the ELO diff over n days
    """

    return get_elo_over_matches(puuid, matches_within_time(puuid, n))


if __name__ == "__main__":
    """
    for testing this module isolated
    """

    puuid = "d515e2d5-b50e-5c77-a79e-eeb46dbe488a"
    # get elo diff last 2 days
    print(get_elo_over_time(puuid, 1))
