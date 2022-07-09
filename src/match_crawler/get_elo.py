from match_crawler.database import sql_statements as db


def get_match_elo(puuid, n):
    """
    Get the ELO of a match n matches ago.
    """

    return db.get_matches_by_puuid_last(puuid, n)[n - 1].match_elo


def get_elo_over_matches(puuid, n):
    """
    Get the ELO diff over n matches
    """

    return get_match_elo(puuid, 1) - get_match_elo(puuid, n + 1)
