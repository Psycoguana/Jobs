import re
import csv
import math
import time
from random import randint
from typing import List

import requests
from bs4 import BeautifulSoup


# A simple class to hold information.
class Item:
    def __init__(self, business_name, address, telephone, fax, website, description):
        self.business_name = business_name
        self.address = address
        self.telephone = telephone
        self.fax = fax
        self.website = website
        self.description = description


class Bot:
    def __init__(self):
        self.url = 'https://hta.org.uk/memberDirectory/filterMembers/?itemclass=.article-block-item&primary_business_type=retailer&interest_type=&q=&search_by=business_name&maxrows=10&page={}&startRow=11'
        self.pages = self.get_pages()

    def main(self):
        parsed_items: List[Item] = []

        for page in range(1, self.pages + 1):
            print(f"Parsing page: {page}/{self.pages}")
            # Parse items from a single page.
            r = requests.get(self.url.format(page)).content
            # Add the parsed items into a list.
            parsed_items.extend(self.parse_page(r))
            # Sleep between 0 and 2 seconds to not overwhelm the server.
            time.sleep(randint(0, 2))

        print(f"{len(parsed_items)} items found")
        # Write all the parsed items into a CSV file.
        self.write_to_csv(parsed_items)

    @staticmethod
    def get_pages():
        url = 'https://hta.org.uk/member-directory.html?primary_business_type=retailer'
        r = requests.get(url).content
        site = BeautifulSoup(r, 'html.parser')

        pattern = r'Retailer \(([0-9]+)\)'
        total_items = site.find(text=re.compile(pattern))

        total_items = re.search(pattern, total_items).group(1)

        # 10 being the number of items each page request retrieves.
        return math.ceil(int(total_items) / 10)

    @staticmethod
    def parse_page(raw_html):
        raw_site = BeautifulSoup(raw_html, 'html.parser')
        parsed_items: List[Item] = []

        items = raw_site.select('div > article > div')
        for item in items:
            name = item.select_one('h2.member-name').text.strip()
            address = item.select_one('p.member-location').text.strip()
            contacts = item.select('div > span.member-meta-item')

            # Add a blank string in case no phone or fax are found.
            phone = ""
            fax = ""
            for contact in contacts:
                if "fa-fax" in str(contact.find_next()):
                    fax = contact.text.strip().replace('Fax ', '')
                elif 'fa-phone' in str(contact.find_next()):
                    phone = contact.text.strip().replace('Tel ', '')

            description = item.select_one('div#member-read-more')
            description = "" if not description else description.text.strip()

            url = item.find('a')
            url = '' if not url else url['href']

            parsed_items.append(
                Item(business_name=name, address=address, telephone=phone, fax=fax, website=url,
                     description=description)
            )

        return parsed_items

    @staticmethod
    def write_to_csv(items: List[Item]):
        with open('result.csv', 'w') as csv_file:
            fieldnames = ['Business_Name',
                          'Address',
                          'Telephone',
                          'Fax',
                          'Website',
                          'Description']

            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for item in items:
                writer.writerow(
                    {'Business_Name': item.business_name, 'Address': item.address, 'Telephone': item.telephone,
                     'Fax': item.fax, 'Website': item.website, 'Description': item.description}
                )


if __name__ == '__main__':
    bot = Bot()
    bot.main()
