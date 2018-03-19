#coding:utf-8
#爬取steam评论
import sys
import re
import urllib2
import time
import datetime

reload(sys)
sys.setdefaultencoding('utf8')

# # 参数
# start_offset=0 用不到
# day_range=30 用不到
# start_date:起始时间戳
# end_date:结束时间戳
# date_range_type: include 取start_date与end_date之间发布的评论；exclude 排除指定时间之间的评论
# filter:评论筛选 summary funny recent all summary最多
# language: 评论所用文字 schinese简体中文 all所有语言
# l:评论者区域 schinese
# review_type:评论类型 all positive negative
# purchase_type:购买类型 all steam non_steam_purchase
# review_beta_enabled=1 是否启用测试版价值分数
# summary_num_positive_reviews=272159 好评数
# summary_num_reviews=478080 总评论数
# 以编号578080的游戏为例，下面两个结果是一样的
# http://store.steampowered.com/appreviews/578080?start_date=1511395200&end_date=1511395260&date_range_type=include&filter=summary&language=schinese&l=schinese&review_type=all&purchase_type=steam&review_beta_enabled=1
# http://store.steampowered.com/appreviews/578080?start_offset=0&day_range=30&start_date=1511395200&end_date=1511395260&date_range_type=include&filter=summary&language=schinese&l=schinese&review_type=all&purchase_type=steam&review_beta_enabled=1&summary_num_positive_reviews=272159&summary_num_reviews=478080

# 以2017/3/23 23:00:00为开始，时间戳1490281200
# 以2018/1/1 00:00:00为结束，时间戳1514736000
START=1490281200
END=1514736000

starttime=1506528000 #1505232000 #1490281200 #每次获取的开始时间
timestep=60 #每次获取一分钟内的评论
endtime=starttime+timestep #每次获取的结束时间

f_t=datetime.datetime.fromtimestamp(starttime).strftime('%Y-%m-%d')
filename=f_t+".txt"
fp=open(filename,'w')

while(starttime<END):
    D=datetime.datetime.fromtimestamp(starttime)
    f_ttemp=D.strftime('%Y-%m-%d')
    if(f_t!=f_ttemp):
        fp.close()
        f_t=f_ttemp
        filename=f_t+".txt"
        fp=open(filename,'w')
    url="http://store.steampowered.com/appreviews/578080?start_date="\
        +str(starttime)\
        +"&end_date="\
        +str(endtime)\
        +"&date_range_type=include&filter=summary&language=schinese&l=schinese&" \
         "review_type=all&purchase_type=steam&review_beta_enabled=1"
    printtime=str(D)
    try:
        request=urllib2.Request(url)
        reponse=urllib2.urlopen(request)
    except urllib2.HTTPError, e:
        print "在时间："+printtime+" 出错" + str(e.reason) +"\n"
    except urllib2.URLError, e:
        print "在时间："+printtime+" 出错" + str(e.reason) +"\n"
    else:
        pattren_noReviews=re.compile(r'{"success":1,"html":".*?"noReviewsYetTitle">(.*?)<.*?',re.S)
        pagehtml = reponse.read().decode("unicode-escape")
        item=re.findall(pattren_noReviews,pagehtml)
        fp.write('Time: ' + printtime + '\n')
        if item :
            pattren_Reviewsnum=re.compile(ur"<span>正在显示与上方筛选条件匹配的.*?>(.*?)<.*?",re.S)
            pattren_Reviews=re.compile(ur'发布于：.*?<.*?"content">(.*?)<div class="gradient">',re.S)
            R_n=re.findall(pattren_Reviewsnum,pagehtml)
            if(R_n!=[]):
                Reviewsnum=int(R_n[0])
                result=re.findall(pattren_Reviews,pagehtml)
                for i in result:
                    fp.write('content: ' + i.strip() + '\n')
            else:
                print "在时间："+printtime+" Reviewsnum获取失败" 
    finally:
        starttime+=timestep
        endtime+=timestep
        time.sleep(0.1)
print "end"
fp.close()
