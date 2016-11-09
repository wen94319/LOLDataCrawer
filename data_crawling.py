'''
拿到全英雄的id=https://na.api.pvp.net/api/lol/na/v1.2/champion?api_key=RGAPI-090e5155-b82f-4f5a-bb4a-99facb7699d0
(state_data)利用id來查到該英雄的資訊= https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/<id>?champData=all&api_key=RGAPI-090e5155-b82f-4f5a-bb4a-99facb7699d0
菁英階級 來找名稱 = https://kr.api.pvp.net/api/lol/kr/v2.5/league/challenger?type=RANKED_SOLO_5x5&api_key=RGAPI-090e5155-b82f-4f5a-bb4a-99facb7699d0
由召喚師名稱找到該玩家id https://kr.api.pvp.net/api/lol/kr/v1.4/summoner/by-name/fw maple?api_key=RGAPI-090e5155-b82f-4f5a-bb4a-99facb7699d0
由玩家id 找到積分常用英雄資訊(可算出勝綠)
 https://kr.api.pvp.net/api/lol/kr/v1.3/stats/by-summoner/3458580/ranked?season=SEASON2016&api_key=RGAPI-090e5155-b82f-4f5a-bb4a-99facb7699d0
玩家id 找他的專精
某一隻英雄 再勝場數300以上 勝率最高的出裝方法 天賦(masteries)
'''
from collections import OrderedDict
from operator import itemgetter
import requests
import json
import time
api_key = "RGAPI-090e5155-b82f-4f5a-bb4a-99facb7699d0"
Region = "na";

def Challenger_list_orderedByleaguePoints(Region):
    Challenger_na_info = requests.get("https://"+Region+".api.pvp.net/api/lol/"+Region+"/v2.5/league/challenger?type=RANKED_SOLO_5x5&api_key="+api_key)
    Challenger_na_info_json = json.loads(Challenger_na_info.text)
    return_array={}
    for data in Challenger_na_info_json['entries']:
        return_array[data['playerOrTeamId']] = data
    return return_array

def Challenger_Champions(Region,id):
    Challenger_na_info = requests.get("https://"+Region+".api.pvp.net/api/lol/"+Region+"/v1.3/stats/by-summoner/"+id+"/ranked?season=SEASON2016&api_key="+api_key)
    Challenger_na_info_json = json.loads(Challenger_na_info.text)
    Champions_info = {}
    # print(Challenger_na_info_json)
    #print(len(Challenger_na_info_json))
    if len(Challenger_na_info_json)==3:
        for data in Challenger_na_info_json['champions']:
            tmp = {}
            win_rate = (data['stats']['totalSessionsWon'])/(data['stats']['totalSessionsLost']+data['stats']['totalSessionsWon'])
            tmp['win_rate']=win_rate
            tmp['total_games']= (data['stats']['totalSessionsLost']+data['stats']['totalSessionsWon'])
            if(tmp['total_games']>=25 and win_rate>=0.5):
                Champions_info[data['id']] = tmp
    elif len(Challenger_na_info_json)==1:
        print("Rate limit Exeed")
        time.sleep( 10 )
    return Champions_info

#no use
def Challenger_Id(challenger_name,Region):
    Challenger_na_info = requests.get("https://"+Region+".api.pvp.net/api/lol/"+Region+"/v1.4/summoner/by-name/"+challenger_name+"?api_key="+api_key)
    Challenger_na_info_json = json.loads(Challenger_na_info.text)
    for data in Challenger_na_info_json:
        return Challenger_na_info_json[data]['id']
'''
    Challenger_ordered_list 取得na裡solo game 的精英名稱id，
'''
Challenger_ordered_list = Challenger_list_orderedByleaguePoints("na")
# for data in Challenger_ordered_list:
#     print(Challenger_ordered_list[data])

'''
    用Challenger_ordered_list的精英名稱id，去查他常使用的英雄（勝率50％以上，且場數大於25場次），回傳用該菁英的名字當key，value就是英雄的使用率
'''
Challenger_Champions_List={}
for data in Challenger_ordered_list:
    temp = Challenger_Champions("na",str(data))
    Challenger_Champions_List[data] = temp
    print(temp)
#
#
# for data in Challenger_Champions_List:
#     print(data)
#     print("\n")
