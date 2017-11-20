# -*- coding:utf-8 -*-
import csv
import urllib2
import json


if __name__== '__main__':
    reader = open('file', 'rb')
    title = ""
    info1 = []
    info2 = ""
    olist = []
    for line in reader:
        line = line.replace("\n", "")
        if not title:
            title = line
        else:
            if not info1:
                info1 = line.split(" ")
                info1[0] = info1[0].split(".")[1]
            elif not info2:
                info2 = line
                olist.append((title, info1[0], info1[1], info2, info1[2]))
                print (title, info1[0], info1[1], info2, info1[2])
                info1 = []
                info2 = ""
            else:
                print "error!"

    csvfile = file("wx.csv", "wb")
    writer = csv.writer(csvfile)
    writer.writerows(olist)
    csvfile.close()
