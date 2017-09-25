from selenium import webdriver
import re
from html.parser import HTMLParser
import lxml.html
 
driver = webdriver.Chrome()
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
                    if int(xx) == xx:
                        d['rooms'] = int(xx)
                    else:
                        d['sqrmtrs'] = xx
                except:
                    d['desc'] = x
            for x in shortd.xpath("div[@class]/h4/span[@class]/text()"):
                d['location'] = x
        for date in hidden.find_class('move-in-date-reserve-until-date'):
            for x in date.xpath("div[@class]/div[@class]/div[@class]/h6[@class]/text()"):
                d['inflytt'] = x
            for x in date.xpath("div[@class]/div[@class]/div[@class]/h5/text()"):
                d['ansokan'] = x

        if d: 
            xs.append(d)
good = [d for d in xs if d['rooms']==4 and d['location'] == 'Kämnärsrätten']
print(good)

driver.close()
