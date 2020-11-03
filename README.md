# netflix_quality_control

A simple bot to get some stuff done for a friend.
Oddly specific.

## Install & Run

- You will need [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/home) also available via `brew cask install chromedriver`
- Then the usual dance:
```bash

$ git clone git@github.com:patillacode/netflix_quality_control.git && cd netflix_quality_control
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```
- Duplicate the `secrets.sample.py` file and rename it into `secrets.py` while setting your credentials in it.
- Run it: `python bot.py`
- Profit
