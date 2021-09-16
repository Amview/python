import pymysql


def insertsql(insertsql):
    db = pymysql.connect(host='', port=3306, user='', passwd='', db='', charset='utf8')
    cursor = db.cursor()
    cursor.execute(insertsql)
    db.commit()
    data = cursor.fetchone()
    print("插入数据中...")


def selectsql(userid, deviceName, userNick):
    db = pymysql.connect(host='', port=3306, user='', passwd='', db='')
    # , charset='utf8'
    cursor = db.cursor()
    sql = 'select userNick,deviceName from ithome where userid =' + str(userid)
    cursor.execute(sql)
    data1 = cursor.fetchall()
    # False：需要插入
    # True：跳过
    i = 0
    # 用户名
    j = 0
    if data1 == None:
        print("新数据"+str(userid))
        print(userNick)
        print(deviceName)
        # 未查到，需要插入
        return False
    else:
        for data in data1:
            print(data)
            # 用户名相同
            if userNick == data[0]:
                # 设备名相同
                print("设备名equ-")
                print(userNick)
                print(deviceName)
                # print(type(deviceName))
                # print(type(data[1]))
                if deviceName == data[1]:
                    # 跳过
                    return True
                elif deviceName is None and data[1] == 'None':
                    # 跳过
                    return True
                else:
                    # 设备名不同，插入
                    i=i+1

            else:
                # 用户名不同，插入
                print("用户名No-")
                print(userNick)
                print(deviceName)
                j = j+1
    if j == len(data1):
        return False
    if i != 0 :
        print("新设备i: "+str(i))
        return False



