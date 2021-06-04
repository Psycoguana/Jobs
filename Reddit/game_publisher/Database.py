import sqlite3

import constants


class Database:
    # TODO: Add game date.
    def __init__(self):
        self.connection = sqlite3.Connection(constants.DATABASE_NAME)
        self.cursor = self.connection.cursor()
        self.table = 'Posted_Games'

        self._create_table(self.table)

    def _create_table(self, table_name):
        query = F"CREATE TABLE IF NOT EXISTS {table_name}(post_id text, local_team text, away_team text, tournament text, game_time text, game_date text)"
        self.cursor.execute(query)
        self.connection.commit()

    def insert_data(self, post_id, local_player, away_player, tournament, game_time, current_time):
        query = f"INSERT INTO {self.table}(post_id,local_team,away_team,tournament,game_time, game_date) VALUES (?, ?, ?, ?, ?, ?)"
        self.cursor.execute(query, (post_id, local_player, away_player, tournament, game_time, current_time,))
        self.connection.commit()

    def get_data(self):
        query = f"SELECT post_id, game_date FROM {self.table}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def search(self, local_team, away_team, tournament, game_time):
        query = f"SELECT * FROM {self.table} WHERE local_team=? AND away_team=? AND tournament=? AND game_time=?"
        self.cursor.execute(query, (local_team, away_team, tournament, game_time,))
        results = self.cursor.fetchall()
        return results

    def remove(self, game_id):
        query = f"DELETE FROM {self.table} WHERE post_id=?"
        self.cursor.execute(query, (game_id,))
        self.connection.commit()


if __name__ == '__main__':
    db = Database()
