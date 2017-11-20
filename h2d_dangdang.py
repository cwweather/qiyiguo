# -*- coding:utf-8 -*-
import re
from mallhandlers.grandmas_fun.h2dict import H2Dict
from tools.helper import replace_matched_part

reg_cid = re.compile("http://category.dangdang.com/cid(\d+).html")
reg_brand = re.compile("http://www.dangdang.com/brands/(\d+).html")
reg_category = re.compile("__Breadcrumb_(\w+)")

class H2dDangdang(H2Dict):

    def set_props(self):
        self.props = {
            "title": "",
            "price": 0,
            "market_price": 0,
            "category": "",
            "cid1": "",
            "cid2": "",
            "cid3": "",
            "c1": "",
            "c2": "",
            "c3": "",
            "product_id": "",
            "images": [],
            "image_url": "",
            "brand": "",
            "brandid": "",
        }
        self.require_props = ["product_id", "images", "price", "market_price"]


    # title
    def grap1_title(self):
        return self.soup.findAll(name="section", attrs={"class": "name_box"})[0].contents[1].text
    def grap2_title(self):
        return self.soup.findAll(name="div", attrs={"name": "Title_pub"})[0].findAll(name="h1")[0].contents[0]

    # price
    def grap1_price(self):
        return self.soup.findAll(name="p", attrs={"id": "color_size_price"})[0].text[1:]
    def grap2_price(self):
        return self.soup.findAll(name="span", attrs={"id": "promo_price"})[0].attrs[1][1]
    def grap3_price(self):
        return self.soup.findAll(name="span", attrs={"id": "salePriceTag"})[0].contents[0]

    # market_price
    def grap1_market_price(self):
        return self.soup.findAll(name="section", attrs={"class": "name_box"})[0]\
            .contents[3].contents[2].contents[1].text[1:]
    def grap2_market_price(self):
        return str(self.soup.findAll(name="span", attrs={"id": "originalPriceTag"})[0].contents[0])
    def grap3_market_price(self):
        return self.soup.findAll(name="span", attrs={"class": "d_price"})[0].contents[1].text[1:]

    # category
    def grap1_category(self):
        return reg_category.findall(self.category.attrs[1][1])[0]

    # cid1
    def grap1_cid1(self):
        data = self.category.findAll(name="a", attrs={"class": "domain"})[0].attrs[0][1]
        return reg_cid.findall(data)[0]

    # c1
    def grap1_c1(self):
        return self.category.findAll(name="a", attrs={"class": "domain"})[0].contents[0].contents[0]

    # c2
    def grap1_c2(self):
        return self.category.contents[2].contents[0]

    # c3
    def grap1_c3(self):
        return self.category.contents[4].contents[0]

    # cid2
    def grap1_cid2(self):
        data = self.category.contents[2].attrs[0][1]
        return reg_cid.findall(data)[0]

    # cid3
    def grap1_cid3(self):
        data = self.category.contents[4].attrs[0][1]
        return reg_cid.findall(data)[0]
    def grap2_cid3(self):
        recommend_soup = self.soup.findAll(name="section", attrs={"id": "recommend"})[0]\
            .contents[1].contents[1].attrs[0][1]
        return re.compile("cid=(\d+)&*").findall(recommend_soup)[0]
    def grap3_cid3(self):
        pid_soup = self.soup.findAll(name="span", attrs={"id": "pid_span"})[0]
        for attr in pid_soup.attrs:
            if attr[0] == "category_id":
                return attr[1]

    #product_id
    def grap1_product_id(self):
        pid_soup = self.soup.findAll(name="span", attrs={"id": "pid_span"})[0]
        for attr in pid_soup.attrs:
            if attr[0] == "product_id":
                return attr[1]
    def grap2_product_id(self):
        recommend_soup = self.soup.findAll(name="section", attrs={"id": "recommend"})[0]\
            .contents[1].contents[1].attrs[0][1]
        return re.compile("pid=(\d+)&*").findall(recommend_soup)[0]

    #images
    def grap1_images(self):
        return self.get_images()
    def grap2_images(self):
        main_imgs_soup = self.soup.findAll(name="ul", attrs={"id": "scroller_ul"})[0].contents
        main_imgs = []
        for img_soup in main_imgs_soup:
            if hasattr(img_soup, "contents"):
                try:
                    img_url = img_soup.contents[0].contents[0].attrs[0][1]
                    main_imgs.append(replace_dang_imgurl(img_url))
                except:
                    pass
        return main_imgs

    # brand
    def grap1_brand(self):
        return self.category.contents[6].contents[0]

    # brandid
    def grap1_brandid(self):
        return reg_brand.findall(self.category.contents[6].attrs[0][1])[0]

    # 设置全局
    def grapinit(self):
        self.category = self.soup.findAll(name="div", attrs={"name": re.compile("__Breadcrumb_\w+")})[0]

    def grapall(self):
        if self.props["images"]:
            self.props["image_url"] = self.props["images"][0]

    def get_images(self):
        main_imgs = []
        main_imgs_soup = self.soup.findAll(name="div", attrs={"id": "mainimg_pic"})[0].contents[1].contents
        for img_soup in main_imgs_soup:
            if hasattr(img_soup, "contents"):
                try:
                    img_url = img_soup.contents[0].contents[0].attrs[0][1]
                    main_imgs.append(replace_dang_imgurl(img_url))
                except:
                    pass
        detail_imgs_soup = self.soup.findAll(name="div", attrs={"class": "right_content"})
        if not detail_imgs_soup:
            try:
                detail_imgs_soup = self.soup.findAll(name="span", attrs={"id": "attach_image_all"})[0].\
                    findAll(name="img")
            except:
                detail_imgs_soup = []
        else:
            try:
                detail_imgs_soup = detail_imgs_soup[0].findAll(name="img")
            except:
                detail_imgs_soup = []
        detail_imgs = []
        for img_soup in detail_imgs_soup:
            for img_attr in img_soup.attrs:
                try:
                    if img_attr[0] == "original":
                        detail_imgs.append(img_attr[1])
                        break
                    if img_attr[0] == "src" and img_attr[1] != "images/grey.gif":
                        detail_imgs.append(img_attr[1])
                        break
                except:
                    pass
        return main_imgs


def replace_dang_imgurl(img_url):
    pattern = '.*?_(?P<char>\w)_\d+\.\w+$'
    repl_str = 'u'
    group_name = 'char'
    return replace_matched_part(pattern, img_url, repl_str, group_name)

if __name__== '__main__':
    import urllib2
    import random
    import datetime
    l = []
    for i in range(0, 0):
        p_id = random.randint(286420, 248061406)
        try:
            url = "http://product.dangdang.com/%s.html" % p_id
            html = urllib2.urlopen(url, timeout=5).read()
        except:
            continue
        l.append(p_id)
        print p_id

    #print "len(l)=%s" % len(l)
    ran = 5000
    full = 5
    lives = full
    p_id = random.randint(1, 1+ran)
    for i in range(0, 5000000):
        if lives <= 0:
            p_id = random.randint(p_id + ran, p_id + ran*4)
            lives = full
        else:
            p_id = random.randint(p_id, p_id+ran)
        #if random.randint(0,1):
        if 0:
            url = "http://m.dangdang.com/h5product/product.php?pid=%s" % p_id
        else:
            url = "http://product.dangdang.com/%s.html" % p_id
        html = ""
        try:
            html = urllib2.urlopen(url, timeout=5).read()
        except:
            #print "%s %s %s %s" % (datetime.datetime.now(), url, p_id, "F")
            lives = lives -1
        if html:
            vv = H2dDangdang(html=html).h2d()
            print "%s %s %s %s" % (datetime.datetime.now(), url, p_id, vv)