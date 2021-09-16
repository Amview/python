import json
from time import sleep

import RRquest
import mmysql

while True:
    url = 'https://qapi.ithome.com/api/home/getnewmenufeeds?pageId=2000000004&menuId=2000000002&page=1&pageSize=20&appver=786&platform=ithome_android'
    res = RRquest.request(url)
    js = json.loads(res.text)
    mesList = js.get('data').get('list')
    i = 1
    pageidList = []
    for list in mesList:
        userid = list.get('feedContent').get('user').get('id')
        userNick = list.get('feedContent').get('user').get('userNick')
        userAvatar = list.get('feedContent').get('user').get('userAvatar')
        level = list.get('feedContent').get('user').get('level')
        deviceName = list.get('feedContent').get('deviceName')
        contents = list.get('feedContent').get('contents')[0].get('content')
        Qlink = list.get('feedContent').get('link')
        pageid = list.get('feedContent').get('id')
        pageidList.append(pageid)
        insertsql = 'insert into ithome(id, userid,pageid,level,deviceName,userNick,userAvatar,Qlink) values(null,' + str(
            userid) + ',' + str(pageid) + ',' + str(level) + ',"' + str(deviceName) + '","' + str(
            userNick) + '","' + str(userAvatar) + '","' + str(Qlink) + '")'
        print("-----")
        j = mmysql.selectsql(userid, deviceName, userNick)

        if j is False:
            mmysql.insertsql(insertsql)
            print("未重复"+ str(userid))
        else:
            print("重复值" + str(userid))
        print("圈子" + str(i))
        i = i + 1
    for itemid in pageidList:
        url2 = 'https://qapi.ithome.com/api/comment/getcomments?contentId=' + str(
            itemid) + '&filterType=0&sortType=0&page=1&pageSize=20&appver=786&platform=ithome_android'
        res2 = RRquest.request(url2)
        js2 = json.loads(res2.text)
        mesList2 = js2.get('data').get('list')
        for list2 in mesList2:
            userid = list2.get('user').get('id')
            userNick = list2.get('user').get('userNick')
            userAvatar = list2.get('user').get('userAvatar')
            level = list2.get('user').get('level')
            deviceName = list2.get('deviceName')
            insertsql = 'insert into ithome(id, userid,level,deviceName,userNick,userAvatar) values(null,' + str(
                userid) + ',' + str(level) + ',"' + str(deviceName) + '","' + str(
                userNick) + '","' + str(userAvatar) + '")'
            print("-----")
            j = mmysql.selectsql(userid, deviceName, userNick)
            if j is False:
                mmysql.insertsql(insertsql)
            else:
                print("重复值" + str(userid))
            print("主楼" + str(i))
            i = i + 1
    for t in range(0, 1000):
        sleep(1)
        print("请等待" + str(t))
