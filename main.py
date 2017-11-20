# -*- coding:utf-8 -*-

import csv
import urllib2
import json
from h2d_ycd import H2dYcd

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

def get_company(oid):
    url = "http://dh.cx/query/guess/{}".format(
        oid.replace(" ", "")
    )
    data = {}
    try:
        data = json.loads(urllib2.urlopen(url, timeout=1).read())
    except:
        print "F:{}".format(url)
    if data.get("status") == True:
        return data.get("data")[0].get("name")
    else:
        return ""


if __name__== '__main__':
    reader = csv.reader(open('orders.csv', 'rb'))
    data = []
    # read order info
    for line in reader:
        data.append((line[1], line[3], line[4], line[5], line[6]))

    # write csv1
    csvfile = file('csv1.csv', 'wb')
    writer = csv.writer(csvfile)
    writer.writerows(data)
    csvfile.close()

    # get kuaididan number from http://kd.dh.cx/a5aeb/13303192267/0
    csvfile2 = file("csv3.csv", "wb")
    writer = csv.writer(csvfile2)
    ret = []

    mobile_list = set([])
    for line in data:
        mobile_list.add(line[1])
    for mob in mobile_list:
        for i in range(0, 30):
            url = "http://kd.dh.cx/a5aeb/{mobile}/{i}".format(
                mobile=mob,
                i=i
            )
            html = ""
            try:
                html = urllib2.urlopen(url, timeout=1).read()
            except:
                print "F:{}".format(url)
            if html:
                result = H2dYcd(html=html).h2d()
                if not result.get("date") or not result.get("content2"):
                    break
                str_date = result["date"][0:6]
                shoujianren = result.get("content2")[0].nextSibling.replace(" ", "").replace("\n", "")[1:]
                tel = result.get("content2")[1].nextSibling.replace(" ", "").replace("\n", "")[1:]
                #mobile = result.get("content2")[2].nextSibling.replace(" ", "").replace("\n", " ")[1:]
                mobile = mob
                address = result.get("content2")[3].nextSibling.replace(" ", "").replace("\n", "")[1:]
                info = result.get("content2")[4].nextSibling.replace(" ", "").replace("\n", "")[1:]
                orderid = result.get("content2")[5].nextSibling.replace(" ", "").replace("\n", "")[1:]
                company = get_company(orderid)
                print str_date, shoujianren, mobile, address, info, orderid, company, tel
                ret.append((str_date,
                            shoujianren, mobile,
                            address, info,
                            orderid, company, tel))
    writer.writerow([u"日期", u"收件人", u"手机", u"地址", u"发货信息", u"快递号", u"快递公司", u"电话"])
    writer.writerows(ret)
    csvfile2.close()

