from selenium import webdriver
from pyvirtualdisplay import Display
import re
from html.parser import HTMLParser
import lxml.html
import json
from datetime import date
import sys
sys.path.append('/usr/local/bin/')
if len(sys.argv)  < 4:
    print('Use arguments: python3 afbs.py $botusername $botpassword $mailrecipient1 [$mailrecipient2]')
    exit(1)

user = sys.argv[1]
pwd = sys.argv[2]

if len(sys.argv) == 5:
    recipient = [sys.argv[3], sys.argv[4]]
else:
    recipient = sys.argv[3]

def hashy(item):
    return ';'.join([str(item[k]) for k in sorted(item.keys())])

print('Looking for a new home')

display = Display(visible=0, size=(800, 600))
display.start()

driver = webdriver.PhantomJS()
driver.get("https://www.afbostader.se/lediga-bostader/")
page = lxml.html.fromstring(str(driver.page_source))
xs = []
for vo in page.find_class('vacant-objects'):
    for hidden in vo.find_class('row'):
        d = {}
        for shortd in hidden.find_class('short-desc-sqrmtrs'):
            for x in shortd.xpath("div[@class]/h3/a[@href]/span[@class]/text()"):
                try:
                    xx = float(x)
                    if xx < 10:
                        d['rooms'] = int(xx)
                    else:
                        d['sqrmtrs'] = xx
                except:
                    d['desc'] = str(x)
            for x in shortd.xpath("div[@class]/h4/span[@class]/text()"):
                d['location'] = str(x)
        for dt in hidden.find_class('move-in-date-reserve-until-date'):
            for x in dt.xpath("div[@class]/div[@class]/div[@class]/h6[@class]/text()"):
                d['inflytt'] = str(x)
            for x in dt.xpath("div[@class]/div[@class]/div[@class]/h5/text()"):
                d['ansokan'] = str(x)

        if d: 
            xs.append(d)
good = { hashy(d): d for d in xs if 'sqrmtrs' in d and d['sqrmtrs'] >= 60.0}

def update_cache(good):
    if not good:
        return (False, [])
    current_objects = {}
    today = str(date.today())
    filename = 'ignore.txt'
    changed = False
    try:
        with open(filename, 'r+') as of:    
            json_str = of.read()
            old = json.loads(json_str)
            for old_key in old:
                old_item = old[old_key]
                if old_item['ansokan'] >= today:
                    current_objects[old_key] = old_item
            for item in good:  #keys     
                if item not in old:
                    current_objects[item] = good[item]
                    changed = True
            
    except FileNotFoundError:
        current_objects = good
        changed = True
    with open(filename, 'w+') as f:
        json.dump(current_objects, f)
    return changed, current_objects

def send_email(user, pwd, recipient, subject, body):
    import smtplib

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(FROM, ", ".join(TO), SUBJECT, TEXT).encode('utf-8')
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()   
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail')
    except:
        print("failed to send mail")


def pretty_print(apt):
    return "There's an {}-m2 apartment at {} with {} rooms with move in date {} and last day to apply: {}.".format(
	str(apt['sqrmtrs']),
	str(apt['location']),
	str(apt['rooms']),
	str(apt['inflytt']),
	str(apt['ansokan']))

def write_mail(apt_list):
    return '\n'.join(pretty_print(a) for a in apt_list.values())


changed, current = update_cache(good)

if changed:
    subject = "Bo i Lund"
    body = write_mail(current)
                
    send_email(user, pwd, recipient, subject, body)

else: 
    print('Same old, same old')

driver.close()
