#!\urs\bin\env python3
# _*_ coding:utf-8 _*_

"""微信好友分析"""

import itchat
import re


class MyWeChat_Analysis(object):

    def __init__(self, pic='wechat.jpg'):
        # 登陆
        itchat.login()
        self.pic = pic
        # 获取好友列表
        self.friends = itchat.get_friends(update=True)[0:]

    # 统计性别比例
    def sexratio(self):
        male = female = other = 0
        for i in self.friends[1:]:
            sex = i['Sex']
            if sex == 1:
                male += 1
            elif sex == 2:
                female += 1
            else:
                other += 1

        total = len(self.friends[1:])

        male_ratio = float(male) / total * 100
        female_ratio = float(female) / total * 100
        other_ratio = float(other) / total * 100

        print(u"男性好友：%.2f%%" % male_ratio)
        print(u"女性好友：%.2f%%" % female_ratio)
        print(u"其他：%.2f%%" % other_ratio)

        # 使用echarts
        from echarts import Echart, Legend, Pie

        chart = Echart(u'%s的微信好友性别比例' % (self.friends[0]['NickName']), 'from WeChat')
        chart.use(Pie('WeChat',
                      [{'value': male, 'name': u'男性 %.2f%%' % male_ratio},
                       {'value': female, 'name': u'女性 %.2f%%' % female_ratio},
                       {'value': other, 'name': u'其他 %.2f%%' % other_ratio}], radius=["50%", "70%"]))
        chart.use(Legend(['male', 'female', 'other']))
        del chart.json['xAxis']
        del chart.json['yAxis']
        chart.plot()

        # 保存图表
        import os
        d = os.path.dirname(__file__)
        chart.save(os.path.dirname(__file__) + os.sep, '%s的好友性别比例' % (self.friends[0]['NickName']))

    def signcloud(self):
        t_list = []
        for i in self.friends:
            # 获取个性签名
            signature = i['Signature'].strip().replace('span', '').replace('class', '').replace('emoji', '')
            # 正则匹配过滤掉emoji表情，例如enmoji1f3c3等
            rep = re.compile('1f\d.+')
            signature = rep.sub('', signature)
            t_list.append(signature)

        # 拼接字符串
        text = ''.join(t_list)

        # jieba分词
        import jieba
        wordlist_jieba = jieba.cut(text, cut_all=True)
        wl_space_split = ' '.join(wordlist_jieba)

        # wordcloud词云
        import matplotlib.pyplot as plt
        from wordcloud import WordCloud, ImageColorGenerator
        import os
        import numpy as np
        import PIL.Image as Image

        d = os.path.dirname(__file__)
        alice_coloring = np.array(Image.open(os.path.join(d, self.pic)))

        # 这里要选择字体存放路径，win字体在windows/Fonts中
        my_wordcloud = WordCloud(background_color='black', max_words=2000, mask=alice_coloring,
                                 max_font_size=40, random_state=42,
                                 font_path=r'‪C:\Windows\Fonts\msyh.ttc').generate(wl_space_split)

        image_colors = ImageColorGenerator(alice_coloring)
        plt.imshow(my_wordcloud.recolor(color_func=image_colors))
        plt.imshow(my_wordcloud)
        plt.axis('off')
        plt.show()

        # 保存图片，并发送手机
        my_wordcloud.to_file(os.path.join(d, '%s好友的签名云.png') % (self.friends[0]['NickName']))

    def nicknamecloud(self):
        t_list = []
        for i in self.friends:
            # 获取个性签名
            nickname = i['NickName'].strip().replace('span', '').replace('class', '').replace('emoji', '')
            # 正则匹配过滤掉emoji表情，例如enmoji1f3c3等
            rep = re.compile('1f\d.+')
            nickname = rep.sub('', nickname)
            t_list.append(nickname)

        # 拼接字符串
        text = ''.join(t_list)

        # jieba分词
        import jieba
        wordlist_jieba = jieba.cut(text, cut_all=True)
        wl_space_split = ' '.join(wordlist_jieba)

        # wordcloud词云
        import matplotlib.pyplot as plt
        from wordcloud import WordCloud, ImageColorGenerator
        import os
        import numpy as np
        import PIL.Image as Image

        d = os.path.dirname(__file__)
        alice_coloring = np.array(Image.open(os.path.join(d, self.pic)))

        # 这里要选择字体存放路径，win字体在windows/Fonts中
        my_wordcloud = WordCloud(background_color='black', max_words=2000, mask=alice_coloring,
                                 max_font_size=40, random_state=42,
                                 font_path=r'‪C:\Windows\Fonts\msyh.ttc').generate(wl_space_split)

        image_colors = ImageColorGenerator(alice_coloring)
        plt.imshow(my_wordcloud.recolor(color_func=image_colors))
        plt.imshow(my_wordcloud)
        plt.axis('off')
        plt.show()

        # 保存图片，并发送手机
        my_wordcloud.to_file(os.path.join(d, '%s好友的名字云.png') % (self.friends[0]['NickName']))

    def city_ratio(self):
        c_list = []
        for i in self.friends:
            city = i['City']
            if city != '':
                c_list.append(city)

        from collections import Counter

        c_dict = dict(Counter(c_list))

        # 使用echarts
        from echarts import Echart, Legend, Pie

        chart = Echart(u'%s的微信各城市好友数量' % (self.friends[0]['NickName']), 'from WeChat')
        chart.use(Pie('WeChat', [{'value': value,
                                  'name': u'{0}-{1}'.format(name, value)} for name, value in c_dict.items()],
                      radius=["30%", "70%"]))
        chart.use(Legend(list(name for name, value in c_dict.items())))
        del chart.json['xAxis']
        del chart.json['yAxis']
        chart.plot()

        # 保存图表
        import os
        d = os.path.dirname(__file__)
        chart.save(os.path.dirname(__file__) + os.sep, '%s的好友城市人数' % (self.friends[0]['NickName']))

    def showall(self):
        self.sexratio()
        self.city_ratio()
        self.signcloud()
        self.nicknamecloud()

    # 退出微信
    itchat.logout()

if __name__ == '__main__':
    user = MyWeChat_Analysis('wechat.jpg')
    user.showall()
