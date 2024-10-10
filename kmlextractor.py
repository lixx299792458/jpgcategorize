import os
import re
# 从kml文件中提取，小号侧塔头的，shootingPointCoordinates
# 最终制作成杆塔坐标词典
dir_name = "德城区\学德线10kV-大疆格式-精灵 PHANTOM 4 RTK(2023-03-18-11-11-22)"
cable_name = "10kV学德线七里庄支线"
dir_files = []
for root,dirs,files in os.walk(dir_name):
    for f in files:
        dir_files.append(os.path.join(root,f))

# print(dir_files)
for dir_file in dir_files:
    # 逐个打开文件，先正则得到航线数组，再逐个查找关键词，再正则得到数据
    file = open(dir_file,'r',encoding='utf-8')
    file_text = file.read()
    waypoints = re.findall('<Placemark>(.*?)</Placemark>',file_text,re.S)
    # print(len(waypoints))
    for waypoint in waypoints:
        if "小号侧塔头" in waypoint:
            coordinate = re.findall('<mis:shootingPointCoordinates>(.*?)</mis:shootingPointCoordinates>',waypoint,re.S)[0]
            # print(coordinate)
            #得到数据后，添加到字典
            dict_item = "\"" + cable_name + dir_file.split('\\')[2].split('.')[0] + "杆" +"\":(" + coordinate.split(',')[0] + "," +coordinate.split(',')[1] + "),"
            print(dict_item)