import exifread
import re
import os

# 遍历所有文件，得到所有路径
dir_name = "可见光"
dir_files = []
for root,dirs,files in os.walk(dir_name):
    for f in files:
        dir_files.append(os.path.join(root,f))

# 逐个提取文件GPS信息，进行对比，符合要求的，重新命名。
for dir_file in dir_files:
    # 打开图片并提取相关GPS信息
    f = open(dir_file,'rb')
    contents = exifread.process_file(f)
    latitude_infos = contents['GPS GPSLatitude'].printable.replace('[','').replace(']','').replace(' ','').split(',')
    longitude_infos = contents['GPS GPSLongitude'].printable.replace('[','').replace(']','').replace(' ','').split(',')
    latitude = float(latitude_infos[0]) + float(latitude_infos[1]) / 60.0 + float(latitude_infos[2].split('/')[0]) / float(latitude_infos[2].split('/')[1]) / 3600.0
    longitude = float(longitude_infos[0]) + float(longitude_infos[1]) / 60.0 + float(longitude_infos[2].split('/')[0]) / float(longitude_infos[2].split('/')[1]) / 3600.0
    coordinate = (longitude,latitude)
    print(dir_file,coordinate)
    # 遍历现有词典记性对比，如果满足距离要求，则建立文件夹并将照片剪切走。


