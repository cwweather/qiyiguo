# -*- coding:utf-8 -*-
import re
from BeautifulSoup import BeautifulSoup


class H2Dict(object):
    def __init__(self, html=""):
        self.props = {}
        self.require_props = {}
        self.soup = BeautifulSoup(html)
        self.set_props()
        self.fail = False

    def set_props(self):
        """
        添加属性
        self.props = {
            "title": "",
            "price": 1,
        }
        """
        pass

    def h2d(self):
        """
        生成dict结果
        """
        ret = {}
        try:
            self.grapinit()
        except:
            pass
        for prop_name in self.props:
            ret.update({
                prop_name: self.grap_value(prop_name)
            })
            if self.fail:
                return {}
        try:
            self.grapall()
        except:
            pass
        return ret

    def grap_value(self, prop_name):
        all_func = dir(self)
        grap_func_check = re.compile("grap\d+_%s" % prop_name)
        # 使用重写后的check_{prop_name}方法，如果没有重写则使用默认check_value
        if hasattr(self, "check_%s" % prop_name):
            setattr(self, "check_value", getattr(self, "check_%s" % prop_name))
        else:
            setattr(self, "check_value", self.default_check_value)
        # 调用grap{number}_{prop_name}方法
        for grap_func in all_func:
            # 检查方法名格式
            if not grap_func_check.match(grap_func):
                continue
            try:
                value = getattr(self, grap_func)()
                if getattr(self, "check_value")(value):
                    return value
            except:
                continue
        if prop_name in self.require_props:
            self.fail = True
            return ""
        else:
            return self.props[prop_name]

    def default_check_value(self, value):
        if value:
            return True
        else:
            return False

    def grapinit(self):
        """
        抓去准备，可在此设置全局
        """
        pass

    def grapall(self):
        """
        直接抓取
        """
        pass


#example"
class h2d_example(H2Dict):

    def set_props(self):
        self.props = {
            "title": "",
            "price": 0
        }

    def grap1_title(self):
        return ""
    def grap2_title(self):
        return "aaaa"

    def grap1_price(self):
        return -10
    def grap2_price(self):
        raise Exception
    def grap3_price(self):
        return 563
    def check_price(self, value):
        if value < 0:
            return False
        else:
            return True


if __name__== '__main__':
    vv = h2d_example(html="").h2d()
    print vv