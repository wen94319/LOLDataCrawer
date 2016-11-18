# -*- coding: utf-8 -*-
from collections import OrderedDict
from operator import itemgetter
import requests
import json
import time
import csv
from json import dumps, load
import sys
print(len(sys.argv))
if len(sys.argv) !=2:
    print('Usage: python3 [].py <Region>')
    sys.exit()
else:
    #print(sys.argv[1])
    Region  = sys.argv[1]
api_key = "RGAPI-090e5155-b82f-4f5a-bb4a-99facb7699d0"
#Region = "kr";
champions_Id_Info={}

#
# 輸入區域（na,kr,...）可以得到該區域的菁英名稱
#
def Challenger_list_orderedByleaguePoints(Region):
    Challenger_na_info = requests.get("https://"+Region+".api.pvp.net/api/lol/"+Region+"/v2.5/league/challenger?type=RANKED_SOLO_5x5&api_key="+api_key)
    Challenger_na_info_json = json.loads(Challenger_na_info.text)
    return_array={}
    for data in Challenger_na_info_json['entries']:
        return_array[data['playerOrTeamId']] = data
    return return_array
#
# 由英雄ID來找到該英雄的英文名稱
#
def Get_Champions_Name_By_id(id):
    #print(id)
    if(id!=0):
        Champions_Name_By_id = requests.get("https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/"+str(id)+"?api_key="+api_key)
        Champions_Name_By_id_json = json.loads(Champions_Name_By_id.text)
        #print(Champions_Name_By_id_json['name'])
        return Champions_Name_By_id_json['name']
    else:
        return "unKnown"

#
# 輸入玩家的ID，可以找到他常用的英雄，並且回傳遊戲場數大於25場且勝率大於5成的英雄
#
def Challenger_Champions(Region,id):
    Challenger_na_info = requests.get("https://"+Region+".api.pvp.net/api/lol/"+Region+"/v1.3/stats/by-summoner/"+id+"/ranked?season=SEASON2016&api_key="+api_key)
    Challenger_na_info_json = json.loads(Challenger_na_info.text)
    Champions_info = {}
    # print(Challenger_na_info_json)
    #print(len(Challenger_na_info_json))
    if len(Challenger_na_info_json)==3:
        for data in Challenger_na_info_json['champions']:
            tmp = {}
            if(data['id']!=0):
                win_rate = (data['stats']['totalSessionsWon'])/(data['stats']['totalSessionsLost']+data['stats']['totalSessionsWon'])
                if((data['stats']['totalDeathsPerSession'])==0):
                    tmp['kda']= (data['stats']['totalChampionKills']+data['stats']['totalAssists'])/1
                else:
                    tmp['kda']= (data['stats']['totalChampionKills']+data['stats']['totalAssists'])/(data['stats']['totalDeathsPerSession'])

                tmp['win_rate']=win_rate
                tmp['total_games']= (data['stats']['totalSessionsLost']+data['stats']['totalSessionsWon'])
                if(tmp['total_games']>=25 and win_rate>=0.5):
                    Champions_name = Get_Champions_Name_By_id(data['id'])
                    Champions_info[Champions_name] = tmp
    elif len(Challenger_na_info_json)==1:
        print("Rate limit Exeed")
        time.sleep( 10 )
    return Champions_info

#
# 由玩家id來找到該玩家的名稱
#
def Get_Challenger_Name_ById(id,Region):
    Challenger_info = requests.get("https://"+Region+".api.pvp.net/api/lol/"+Region+"/v1.4/summoner/"+str(id)+"?api_key="+api_key)
    Challenger_info_json = json.loads(Challenger_info.text)
    for data in Challenger_info_json:
        #print(Challenger_info_json[data])
        if(Challenger_info_json[data]['name']):
            #print(Challenger_info_json[data]['name'])
            return Challenger_info_json[data]['name']
        else:
            print("unknown")
            return "unknown"

'''
    Challenger_ordered_list 取得na裡solo game 的精英名稱id，
'''
Challenger_ordered_list = Challenger_list_orderedByleaguePoints(Region)

'''
    用Challenger_ordered_list的精英名稱id，去查他常使用的英雄（勝率50％以上，且場數大於25場次），回傳用該菁英的名字當key，value就是英雄的使用率
'''
Challenger_Champions_List={}
for data in Challenger_ordered_list:
    ChallengerName = Get_Challenger_Name_ById(data,Region)
    temp = Challenger_Champions(Region,str(data))
    Challenger_Champions_List[ChallengerName] = temp


'''
    將資料寫進json檔
'''
file_name = "Challenger_info_"+Region+".json"
# with open(file_name, mode='w', encoding='utf-8') as f:
#     json.dump(Challenger_Champions_List, f)
with open(file_name, 'w',encoding='utf-8') as f:
     json.dump(Challenger_Champions_List, f, ensure_ascii=False)
#Get_Champions_Name_By_id(1)
