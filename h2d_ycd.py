# -*- coding:utf-8 -*-
import re
from bin.h2dict import H2Dict


class H2dYcd(H2Dict):
    def set_props(self):
        self.props = {
            "date": "",
            "content": "",
            "content2": "",
        }

    def grap1_date(self):
        return self.soup.findAll(name="li", role="presentation", attrs={"class": "active"})[0].text

    def grap1_content(self):
        return self.soup.findAll(name="ul", attrs={"class": "list-inline"})[0].text

    def grap1_content2(self):
        return self.soup.findAll(name="strong")


if __name__== '__main__':
    import urllib2
    import random
    import datetime
    # http://kd.dh.cx/a5aeb/13303192267/0
    url = "http://kd.dh.cx/a5aeb/13303192267/0"
    html = ""
    try:
        html = urllib2.urlopen(url, timeout=1).read()
    except:
        print "F"
    if html:
        result = H2dYcd(html=html).h2d()
        str_date = result["date"].split(" ")[0]
        shoujianren = result.get("content2")[0].nextSibling.replace(" ", "").replace("\n", "")
        tel = result.get("content2")[1].nextSibling.replace(" ", "").replace("\n", "")
        mobile = result.get("content2")[2].nextSibling.replace(" ", "").replace("\n", "")
        address = result.get("content2")[3].nextSibling.replace(" ", "").replace("\n", "")
        info = result.get("content2")[4].nextSibling.replace(" ", "").replace("\n", "")
        orderid = result.get("content2")[5].nextSibling.replace(" ", "").replace("\n", "")

