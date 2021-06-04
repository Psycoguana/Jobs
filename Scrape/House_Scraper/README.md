# House Scraper

This bot receives links from a Telegram Bot.
It parses them and replies with an Excel file containing the house parsed data, such as:
* Address
* Price
* Highschools nearby
* Square Footage
* Time on the market
* And many more

## 📦 Requirements
```
- Python 3
- Pip
```

## 🔧 Setup

The setup requires creating a telegram bot from the app to get a token,
and setting up a PostgreSQL database.

Then need to install the dependencies, you can do that by running: `pip install -r requirements.txt`

(The whole setup is usually done by me).

## 🖥️ Usage

It's super easy, just run `python3.8 main.py` and the telegram bot will start listening for new messages indefinetely.

There are 2 commands:

* `/start`: Give a simple instructions message

* `/del`: Send a link next to it and that house will be removed from the database.

If the message sent is a valid url, it will get scraped, added to the database and an excel file with all the houses will be sent

If the message is not a command nor a valid link, it will be informed to the user.


## 📚 Dependencies

* [requests](https://docs.python-requests.org/en/master/): For communicating with the site's API.
* [psycopg2](https://www.psycopg.org/): For connecting with the PostgreSQL database.
* [openpyxl](https://openpyxl.readthedocs.io/en/stable/): For creating the Excel files.
* [python-telegram-bot](https://python-telegram-bot.org/): For everything telegram related.