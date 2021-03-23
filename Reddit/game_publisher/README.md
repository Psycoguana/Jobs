# Game Publisher

This script will scrape rugby games from [BBC](https://www.bbc.com/sport/rugby-union/scores-fixtures) and post them on [Reddit](https://www.reddit.com/r/rugbystreams/). After a couple days, they will get automatically removed.

## 📦 Requirements
```
- Python 3
- Pip
```

## 🔧 Installation

You just need to install the dependencies, you can do that by running: `pip install -r requirements.txt`

## 🖥️ Usage

It's super easy, just run `python3.8 main.py` and the script will do the rest.


## 📚 Dependencies

* [PRAW](https://github.com/praw-dev/praw): For handling the reddit API.
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/): For scraping the BBC page.
