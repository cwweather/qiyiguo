# -*- coding:utf-8 -*-
import re
from mallhandlers.grandmas_fun.h2dict import H2Dict

class H2dYhd(H2Dict):
    def set_props(self):
        self.props = {
            "title": "",
            "subtitle": "",
            "price": 0,
            "market_price": 0,
            "images": [],
            "store_id": "",
            "page_store_id": "",
            "productId": "",
        }
        self.require_props = ["store_id", "page_store_id", "price", "market_price", "title", "images"]

    def grap1_title(self):
        return self.soup.findAll(name="h2", attrs={"id": "pd_product-title"})[0].text

    def grap1_subtitle(self):
        return self.soup.findAll(name="h3", attrs={"id": "pd_product-subtitle"})[0].text

    def grap1_price(self):
        num = self.soup.findAll(name="strong", attrs={"class": "pd_product-price-num"})[0].text
        decimal = self.soup.findAll(name="span", attrs={"class": "pd_product-price-decimal"})[0].text
        return float(num + decimal)

    def grap1_market_price(self):
        text_price = self.soup.findAll(name="del", attrs={"class": "pd_product-price-old"})[0].text
        return float(re.compile("\D*(\d+)").findall(text_price)[0])

    def grap1_images(self):
        images = []
        wrap = self.soup.findAll(name="div", attrs={"class": "public_com-swipeSlide"})[0].contents[1]
        for w in wrap:
            if hasattr(w, "contents"):
                images.append(w.contents[1].contents[1].attrs[0][1])
        return images
    def grap2_images(self):
        images = []
        pic_soup = self.soup.findAll(name="div", attrs={"class": "pd_product-bigpic-lists"})[0].contents
        for pic in pic_soup:
            if hasattr(pic, "attrs"):
                if len(pic.attrs) == 2:
                    pic_url = re.compile("url\(\"(.+\.jpg)").findall(pic.attrs[0][1])[0]
                else:
                    pic_url = pic.attrs[2][1]
                images.append(pic_url)
        return images
    def grap3_images(self):
        images = []
        pic_soup = self.soup.findAll(name="div", attrs={"class": "pd_product-bigpic-lists"})[0].contents
        for pic in pic_soup:
            if hasattr(pic, "attrs"):
                if len(pic.attrs) == 2:
                    for pic_attrs in pic.attrs:
                        if pic_attrs[0] == 'data-bgpic':
                            pic_url = pic_attrs[1]
                            break
                else:
                    pic_url = pic.attrs[2][1]
                images.append(pic_url)
        return images

    def grap1_store_id(self):
        for scr_soup in self.soup.findAll(name="script"):
            if scr_soup.attrs == []:
                detailparams = scr_soup.text
                return re.compile("pmId\:(\d+)").findall(detailparams)[0]

    def grap1_page_store_id(self):
        return re.compile("http:\/\/item\.m\.yhd\.com\/item\/(\d+)").\
            findall(self.soup.findAll(name="meta", attrs={"name": "h5"})[0].attrs[1][1])[0]

    def grap1_productId(self):
        for scr_soup in self.soup.findAll(name="script"):
            if scr_soup.attrs == []:
                detailparams = scr_soup.text
                return re.compile("productId\:(\d+)").findall(detailparams)[0]


if __name__== '__main__':
    import urllib2
    import random
    import datetime
    l = []
    ran = 5
    full = 5
    lives = full
    #p_id = 34928607
    p_id = 34928608
    for i in range(0, 10):
        if 1:
            url = "http://item.m.yhd.com/item/%s" % p_id
        else:
            url = "http://product.dangdang.com/%s.html" % p_id
        html = ""
        try:
            html = urllib2.urlopen(url, timeout=1).read()
        except:
            print "%s %s %s %s" % (datetime.datetime.now(), url, p_id, "F")
        if html:
            vv = H2dYhd(html=html).h2d()
            print "%s %s %s %s" % (datetime.datetime.now(), url, p_id, vv)
        p_id = p_id+1