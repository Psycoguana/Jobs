from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup, Tag

from Game import Game


class BBC:
    def __init__(self):
        self.base_url = 'https://www.bbc.com/sport/rugby-union/scores-fixtures'

    def run(self):
        """ Try to run the parser. In case of failure, it will show a simple message. """
        try:
            return self._main()
        except Exception as error:
            print("There was an error trying to parse BBC.")
            print(f"Please check that {self.base_url} is accessible from your website")
            print(error)

    def _main(self):
        """
        This method moves the whole parser. It gets a date which will be use to construct the url.
        Gets the raw website, extracts the tournaments from everything else.
        Then parses the important data into a list of Game objects, which will be returned.
         """
        date = datetime.now().date()
        url = f"{self.base_url}/{date}"
        raw_site = self._fetch_site(url)
        tournaments = self._get_raw_tournaments(raw_site)
        parsed_games = self._parse_games(tournaments)

        return parsed_games

    @staticmethod
    def _fetch_site(url):
        response = requests.get(url)
        return response.content

    @staticmethod
    def _get_raw_tournaments(website) -> List[Tag]:
        website = BeautifulSoup(website, 'html.parser')
        tournaments = website.find_all('span', {'class', 'qa-fixture-block'})
        return tournaments

    @staticmethod
    def _parse_games(tournaments: List[Tag]) -> List[Game]:
        parsed_games: List[Game] = []

        for tournament in tournaments:
            current_tournament = tournament.select_one('h3.sp-c-fixture-block-heading')

            games = current_tournament.next_sibling.select('ul > li > a > article > div')
            for game in games:
                game_time = game.select_one('span.sp-c-fixture__block > span').text
                if ':' not in game_time:
                    # The match has already been played, so instead of an hour we find a score.
                    # So let's move on to the next game.
                    continue

                local = game.select_one('span.sp-c-fixture__team--time-home > span > span.qa-full-team-name').text
                away = game.select_one('span.sp-c-fixture__team--time-away > span > span.qa-full-team-name').text

                aux_game = Game(local, away, tournament=current_tournament.text, date=game_time)
                parsed_games.append(aux_game)

        return parsed_games


if __name__ == '__main__':
    BBC().run()
