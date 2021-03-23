import datetime
from typing import List

import constants
from Database import Database
from Game import Game
from Reddit_Handler import RedditHandler
from Scrapers.BBC import BBC


class Bot:
    def __init__(self):
        self.reddit = RedditHandler()
        self.database = Database()
        self.DATE_FORMAT = "%Y-%m-%d"
        self.current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    def main(self):
        games = BBC().run()
        games = self.remove_posted_games(games)
        games = self.remove_blacklisted_teams(games)

        if games:
            self.create_posts(games, self.current_date)
        else:
            print("No new games were found.")

        self.remove_old_games()

    def create_posts(self, games: List[Game], current_date):
        for game in games:
            post_title = constants.POST_TITLE.format(game.local, game.away, game.time, game.tournament)
            post_body = constants.POST_BODY

            print(f"Posting: {post_title}")
            new_post_id = self.reddit.create_post(post_title, post_body)
            self.database.insert_data(str(new_post_id), game.local, game.away, game.tournament, game.time, current_date)

    def remove_posted_games(self, games: List[Game]) -> List[Game]:
        new_games: List[Game] = []

        for game in games:
            # If any of the games scraped is in the database (so it's already been posted), it will not be added
            # to the list that will be return.
            if not self.database.search(game.local, game.away, game.tournament, game.time):
                new_games.append(game)

        return new_games

    @staticmethod
    def remove_blacklisted_teams(games: List[Game]) -> List[Game]:
        # I get every blacklisted team and create a list separating by a comma.
        # For each element, I remove the trailing space and make it lowercase.
        blacklisted_teams = [x.strip().lower() for x in constants.TEAMS_BLACKLIST.split(',')]

        allowed_games = games.copy()
        for game in games:
            # If the local or away team are in the blacklist, they get removed from the games list.
            if game.local.lower() in blacklisted_teams or game.away.lower() in blacklisted_teams:
                allowed_games.remove(game)

        return allowed_games

    def remove_old_games(self):
        print("Searching old posts...")
        games = self.database.get_data()

        for game_data in games:
            game_id, game_date = game_data
            game_date = datetime.datetime.strptime(game_date, self.DATE_FORMAT)

            # I calculate a delta of x days based on constants.DAYS_TO_REMOVE_POST
            delta = datetime.timedelta(days=constants.DAYS_TO_REMOVE_POST)
            # I get the time for this date
            today = datetime.datetime.strptime(self.current_date, self.DATE_FORMAT)
            # And then the amount of time between the both of them.
            x_days_ago = today - delta

            # If x_days_ago has already passed, the post is removed from reddit
            # and from the database to keep it light.
            if game_date < x_days_ago:
                print(f"\t{game_id} is old.")
                print(f"\t\tDeleting post...")
                self.reddit.remove_post(game_id)
                print(f"\t\tRemoving from database...")
                self.database.remove(game_id)


def send_error_dm():
    print(f"An error has occurred, {error}")
    print(f"Sending a message to {constants.OWNER}")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    owner = RedditHandler().reddit.redditor(constants.OWNER)
    owner.message(
        constants.ERROR_TITLE,
        constants.ERROR_MESSAGE.format(current_time, error)
    )


if __name__ == '__main__':
    # owner = RedditHandler().reddit.redditor(constants.OWNER)
    # subs = owner.submissions.new()
    # for sub in subs:
    #     if sub.subreddit == "bot_testing_pg":
    #         print("Removing")
    #         sub.delete()
    #
    # exit()

    try:
        bot = Bot()
        bot.main()
    except Exception as error:
        send_error_dm()
