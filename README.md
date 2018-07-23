# afbot
How 2 get a new apartment:

- Buy a raspberry pie
- Let afbot email you when a fitting appartment appears
- Sign up for the apartment

### Installation

#### Linux (with apt-get):
```bash
sudo apt-get install xvfb libxslt-dev phantomjs python3-dev python3-pip git
python3 -m pip install selenium pyvirtualdisplay html.parser lxml
git clone https://github.com/CookingMonsters/afbot.git
```
#### OsX (TODO: should be possible to get similar with brew)

#### Windows (TODO: idk yet)

### Run
```bash
python3 afbs.py $botusername $botpassword $mailrecipient1 [$mailrecipient2]
```

### Automaticly running this script once a day
Use a chronjob on a raspberry.
- install cron: `sudo apt-get install gnome-schedule`
- Add to crontab:
    + edit crontabe `crontab -e` (opens vi). If vi is not your friend and something goes wrong, you can exit and not save anything by pressing escape, then writing `:q!`. `:` on an american layoutis in the same spot as `shift + ö` on a swedish layout.
    + Type: "Go" to jump to the last line (G) and enter insert mode on a new line below with o.
    + Write the following line: `5 2 * * * python3 afbs.py $botusername $botpassword $mailrecipient1 [$mailrecipient2]`
    + Exit and save by doing escape followed by `:wq`.

