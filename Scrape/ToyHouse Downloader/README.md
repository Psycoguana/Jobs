# ToyHouse Downloader

This script will login into [ToyHouse](https://toyhou.se/) using Selenium, grab the current cookies and start
downloading a certain user images using requests.

## 📦 Requirements
```
- Python 3
- Pip
- Chrome Browser
```

## 🔧 Setup

You just need to install the dependencies, you can do that by running: `pip install -r requirements.txt`
After that, open config.ini file and specify an output folder, your user and password, and the username
that you wish to scrape

## 🖥️ Usage

It's super easy, just run `python3.8 main.py` and the script will do the rest.
Once it's done, the output folder will look like this:

```
📁 images
├── 📁 character_1
│   ├── 🖼️ img_1.png
│   └── 🖼️ img_2.png
├── 📁 character_2
│   └── 🖼️ img_1.png
└── 📁 character_3
    ├── 🖼️ gif_1.gif
    └── 🖼️ img_1.png
```

## 📚 Dependencies

* [requests](https://docs.python-requests.org/en/master/): For getting album pages and downloading the images.
* [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/): For parsing HTML.
* [selenium](https://pypi.org/project/selenium/): For logging in and getting the login token.
* [webdriver-manager](https://pypi.org/project/webdriver-manager/): For downloading the correct Chrome Webdriver when necessary.