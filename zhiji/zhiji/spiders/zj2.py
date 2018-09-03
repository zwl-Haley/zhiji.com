# -*- coding: utf-8 -*-
import scrapy
import re
import json
# import requests
from zhiji.code import *
from zhiji.items import ZhijiItem
import pymysql
from scrapy.exceptions import CloseSpider

class ZjSpider(scrapy.Spider):
    name = 'zj2'

    def __init__(self):
        self.connect = pymysql.connect(
            host = '127.0.0.1',
            port = 3306,
            db = "video_data",
            user = "root",
            passwd = "wenliang960213",
            charset = "utf8",
            use_unicode = True
            )
        self.cursor = self.connect.cursor()

    def start_requests(self):
        for auto_id in range(25500,25729):
            sql = "SELECT member FROM zhiji_members WHERE auto_id = %d;"%(auto_id)
            self.cursor.execute(sql)
            members = self.cursor.fetchall()[0][0]
            print("-----------------------------")
            print("MySQL位置：",auto_id)
            print("-----------------------------")
            
            for i, member in enumerate(eval(members)):
                # cookies = {"JSESSIONID":self.get_cookie}
                url = "http://profile.zhiji.com/members/{}.html".format(member)
                yield scrapy.Request(url, meta={'cookiejar': i})

        self.cursor.close()
        self.connect.close()


    def parse(self, response):
        if len(response.text) > 100:
            member = response.url.split("members/")[1].split(".html")[0]
            date_page = re.findall(r"date_page:'(.*?)'", response.text)[0]
            url = "http://profile.zhiji.com/members/classes/mem_impl.jsp?impl_type=6&member_no_to={}&from=&fromUrl=&ad_province=&ad_new_date=&date_page={}".format(member,date_page)
            headers = {
                    'Referer': response.url,
                    'User-Agent': 'Mozilla/5.0',
                    }
            yield scrapy.Request(url, callback=self.parse_info, meta={'cookiejar': response.meta['cookiejar']})
        else:
            with open("error1.txt","a") as f:
                f.write(response.url+"\n")
            raise CloseSpider('返回为空')


    def parse_info(self ,response):
        item = ZhijiItem()
        if len(response.text) > 100:
            res_json = json.loads(response.text)
            #member为1表示真会员，0表示不是会员
            # member = res_json["purchased_products"]
            #1表示有微信，0表示无微信
            # weixin = res_json["wx_see_type"]
            user_id = res_json["member_no_to"]
            #头像
            head_img = res_json["default_photo_to"]
            #相册
            images = re.findall(r'"member_photo":"(.*?)"',response.text)

            sex = res_json["sex_str"]
            sex = "1" if sex == "女" else "0"

            age = res_json["age_to"]

            province = res_json["province_name_to"]
            city = res_json["city_name_to"]
            address = province + city

            income = res_json["earning_to"]
            income = "" if income == "" else income_d[income]

            introduction = res_json["brief_introduction"]

            height = res_json["height_to"]
            height = "" if height == "" else height_d[height]

            weight = res_json["bodily_form_to"]
            weight = "" if weight == "" else weight_d[weight]

            education = res_json["education_to"]
            education = "" if education == "" else education_d[education]

            marriage = res_json["stat_now_to"]
            marriage ="" if marriage == "" else marriage_d[marriage]

            qq = res_json["oicq_to2"]
            # weixin_num = self.get_wx(user_id) if weixin == "1" else ""


            item["user_id"] = user_id
            item["images"] = images
            item["sex"] = sex
            item["age"] = age
            item["income"] = income
            item["introduction"] = introduction
            item["height"] = height
            item["weight"] = weight
            item["education"] = education
            item["marriage"] = marriage
            item["qq"] = qq
            item["address"] = address
            item["head_img"] = head_img
            # item["weixin_num"] = weixin_num
            if not head_img == '':
                yield item
        else:
            with open("error2.txt","a") as f:
                f.write(response.url+"\n")


    # def get_cookie(self):
    #     headers={
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    #         "Referer": "http://zhanghu.zhiji.com/search_new/search_zj.asp?"
    #         }
    #     r = requests.post("http://www.zhiji.com/gmb_css_images_js/new_login_submit.asp",headers=headers,data={"login_name": "dodmk","password": "201323"},allow_redirects=True)
    #     cookie = r.cookies["JSESSIONID"].split(".node1")[0]
    #     return cookie
    # def get_wx(self, user_id):
    #     url = "http://app.zhiji.com/zhiji-mobile-web/oicq/pcseewx?callback=jQuery&member_no_from=M14014675&member_no_to={}&sex=1&is_vip_free=2&VIP=B&str=".format(user_id)
    #     r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    #     wx = re.findall(r'"msn":"(.*?)"',r.text)[0]
    #     return wx
