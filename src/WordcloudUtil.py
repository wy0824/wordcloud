import jieba
import wordcloud
import pymysql
from pyecharts import Geo
from langconv import *

class WordcloudUtil:

    def __init__(self):
        self.db = pymysql.connect('localhost','root','winter','keep',charset='utf8')

    def fetchData(self,start,len):
        try:
            with self.db.cursor() as cursor:
                sql = 'select content from keephot_new_copy limit %d,%d' % (start,len)
                cursor.execute(sql)
                result = cursor.fetchall()
                # print(result)
            return result
        except Exception as e:
            print("获取数据库数据失败"+str(e))
            self.db.rollback()
            return ""

    def getDataLen(self):
        try:
            with self.db.cursor() as cursor:
                sql = 'select count(*) from keephot_new_copy '
                cursor.execute(sql)
                result = cursor.fetchone()
                # print(result)
            return result
        except Exception as e:
            print("获取数据长度失败"+str(e))
            self.db.rollback()
            return 0

    def word_split(self,text,stopwords):

        seg_list = jieba.cut(text, cut_all=False)
        # result = []
        # for word in seg_list:
        #     if word.encode("utf-8") not in stopwords:
        #         result.append(word)
        return " ".join(seg_list)

    def get_map(self):
        map_info = []
        try:
            with self.db.cursor() as cursor:
                sql = 'select city,count(*) from user_info_copy where country="中国" group by city order by count(*) desc'
                cursor.execute(sql)
                result = cursor.fetchall()
                for item in result:
                    if item[0] != "" and item[0] != '地球' and item[0] != '台湾省':
                        cityname = item[0].replace("市","")
                        cityname = cityname.replace("特别行政区","")
                        cityname = Converter('zh-hans').convert(cityname)
                        value = (cityname,item[1])
                        map_info.append(value)
                # print(result)
                # print(map_info)
            return map_info
        except Exception as e:
            print("获取用户地理位置失败"+str(e))
            self.db.rollback()
            return ""

    def plot_map(self,data):
        geo = Geo("keep注册用户地理位置分布", "keepers in China", title_color="#fff",
                  title_pos="center", width=1200,
                  height=600, background_color='#404a59')
        attr, value = geo.cast(data)
        geo.add("", attr, value, visual_range=[0, 200], visual_text_color="#fff",
                symbol_size=15, is_visualmap=True)
        geo.render()




