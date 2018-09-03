# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql
import datetime

class ZhijiPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host = "127.0.0.1",
            port = 3306,
            db = "video_data",
            user = "root",
            passwd = "",
            charset = 'utf8',
            use_unicode = True
            )
        self.cursor = self.connect.cursor()
    print("连接数据库成功，正在存入数据库...")

    def process_item(self, item, spider):
        self.cursor.execute(
            """replace into zhiji(create_time, head_img, sex, age, address, income, introduction, height, weight, education, qq, marriage, images, user_id)
            value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            item["head_img"],
            item["sex"],
            item["age"],
            item["address"],
            item["income"],
            item["introduction"],
            item["height"],
            item["weight"],
            item["education"],
            item["qq"],
            item["marriage"],
            str(item["images"]),
            item["user_id"]
             ))
        self.connect.commit()
        return item

    def close_spider(self,spider):
        self.connect.close()


# CREATE TABLE zhiji (
#     auto_id INT NOT NULL primary key AUTO_INCREMENT,
#     create_time DateTime NOT NULL,
#     head_img VARCHAR(100),
#     sex VARCHAR(2),
#     age VARCHAR(10),
#     address VARCHAR(20),
#     income VARCHAR(20),
#     introduction text,
#     height VARCHAR(20),
#     weight VARCHAR(20),
#     education VARCHAR(20),
#     qq VARCHAR(50),
#     marriage VARCHAR(20),
#     images text,
#     user_id VARCHAR(50));
# ALTER TABLE `zhiji` ADD unique(`user_id`);

# class ZhijiPipeline2(object):
#     def __init__(self):
#         self.connect = pymysql.connect(
#             host = "127.0.0.1",
#             port = 3306,
#             db = "video_data",
#             user = "root",
#             passwd = "wenliang960213",
#             charset = 'utf8',
#             use_unicode = True
#             )
#         self.cursor = self.connect.cursor()
#     print("连接数据库成功，正在存入数据库...")

#     def process_item(self, item, spider):
#         self.cursor.execute("""replace into zhiji_members(member) value (%s)""",(str(item["member"])))
#         self.connect.commit()
#         return item

#     def close_spider(self,spider):
#         self.connect.close()

# CREATE TABLE zhiji_members (
#     auto_id INT NOT NULL primary key AUTO_INCREMENT,
#     member VARCHAR(255));
