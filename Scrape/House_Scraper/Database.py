import logging
import os
from typing import List

import psycopg2

from House import House


class Database:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

        DATABASE_URL = ''
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()
        self.table = 'Houses'
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {self.table}('
            f'link varchar primary key ,'
            f'address varchar,'
            f'city varchar,'
            f'status varchar,'
            f'property_year integer,'
            f'date_on_market varchar,'
            f'price varchar,'
            f'square_feet float,'
            f'price_per_square_feet varchar,'
            f'school_names varchar,'
            f'taxableLandValue varchar,'
            f'taxableImprovementValue varchar,'
            f'rollYear varchar, '
            f'taxesDue varchar);')
        self.conn.commit()

    def insert_new_values(self, new_data: List[House]):
        insert_query = (f'INSERT INTO {self.table}'
                        f'(link,'
                        f'address,'
                        f'city,'
                        f'status,'
                        f'property_year,'
                        f'date_on_market, '
                        f'price,'
                        f' square_feet,'
                        f' price_per_square_feet,'
                        f' school_names,'
                        f'taxableLandValue,'
                        f'taxableImprovementValue,'
                        f'rollYear,'
                        f'taxesDue) '
                        f'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                        f'ON CONFLICT DO NOTHING;')

        for item in new_data:
            logging.info(f"Database: Inserting {item}")
            logging.debug(item.__dict__)
            self.cursor.execute(insert_query,
                                (item.link,
                                 item.address,
                                 item.city,
                                 item.status,
                                 item.property_year,
                                 item.date_on_market,
                                 item.price,
                                 item.square_feet,
                                 item.price_per_square_feet,
                                 item.school_names,
                                 item.taxableLandValue,
                                 item.taxableImprovementValue,
                                 item.rollYear,
                                 item.taxesDue)
                                )

        self.conn.commit()

    def get_values(self):
        # I simply fetch and return every value.
        self.cursor.execute(f'SELECT * FROM {self.table};')
        records = self.cursor.fetchall()
        logging.debug(f"Found records -> {records}")

        return records

    def remove(self, link):
        logging.info(f"Removing {link}...")
        query = f'DELETE FROM {self.table} WHERE link = %s'
        self.cursor.execute(query, (link,))

        self.conn.commit()


if __name__ == '__main__':
    db = Database()
    print(db.get_values())
