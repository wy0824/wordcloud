import wordcloud
import jieba
import jieba.analyse
import os
from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


from WordcloudUtil import WordcloudUtil


test = WordcloudUtil()

map_info = test.get_map()
# print(map_info)
test.plot_map(map_info)

len = (test.getDataLen()[0])
print(len)
stopwords = []
for word in open("stopwords.txt","r",encoding="utf-8"):
    stopwords.append(word.strip())
# print(stopwords)

# for i in range(int(int(len)/100)):
#     f = open('hotcontent.txt','a',encoding='utf-8')
#     for item in test.fetchData(i*100,100):
#         content = item[0]
#         # for stopword in stopwords:
#         #     content = content.replace(stopword," ")
#         f.write(content+"\n")
#     f.close()

text =''
f = open('hotcontent.txt',encoding='UTF-8')
text=f.read()
f.close()

# word_list = jieba.cut(text, cut_all=False)
jieba.analyse.set_stop_words("stopwords.txt")
word_list = jieba.analyse.extract_tags(text, topK=1000,allowPOS=('ns', 'n', 'vn', 'v'))
result = " ".join(word_list)

# print(stopwords)
# word_list = test.word_split(text,stopwords)

d = path.dirname(__file__)

# read the mask / color image taken from
# http://jirkavinse.deviantart.com/art/quot-Real-Life-quot-Alice-282261010
alice_coloring = np.array(Image.open(path.join(d, "wukong.jpg")))

wc = wordcloud.WordCloud(background_color="white",
                         max_words=500,
                         mask=alice_coloring,
                         max_font_size=80,
                         random_state=42,
                         font_path='simhei.ttf')
# generate word cloud
my_wordcloud = wc.generate(result)

# create coloring from image
image_colors = wordcloud.ImageColorGenerator(alice_coloring)

# show
# plt.imshow(wc, interpolation="bilinear")
# plt.axis("off")
plt.figure()
# recolor wordcloud and show
# we could also give color_func=image_colors directly in the constructor
plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis("off")
# plt.figure()
# plt.imshow(alice_coloring, cmap=plt.cm.gray, interpolation="bilinear")
# plt.axis("off")
plt.show()
wc.to_file('wukong.png')


