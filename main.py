import exifread
import os
from geopy.distance import geodesic
import shutil
from tkinter import filedialog
from tkinter.messagebox import *

def jpgcategorize(pathin, pathout, coordinates_dict, threshold_distance):
    # 遍历所有文件，得到所有路径
    dir_name = pathin
    dir_files = []
    for root, dirs, files in os.walk(dir_name):
        for f in files:
            dir_files.append(os.path.join(root, f))
    # 逐个提取文件GPS信息，进行对比，符合要求的，重新命名。
    for dir_file in dir_files:
        try:
            # 打开图片并提取相关GPS信息
            f = open(dir_file, 'rb')
            contents = exifread.process_file(f)
            latitude_infos = contents['GPS GPSLatitude'].printable.replace('[', '').replace(']', '').replace(' ', '').split(',')
            longitude_infos = contents['GPS GPSLongitude'].printable.replace('[', '').replace(']', '').replace(' ', '').split(',')
            latitude = float(latitude_infos[0]) + float(latitude_infos[1]) / 60.0 + float(latitude_infos[2].split('/')[0]) / float(latitude_infos[2].split('/')[1]) / 3600.0
            longitude = float(longitude_infos[0]) + float(longitude_infos[1]) / 60.0 + float(longitude_infos[2].split('/')[0]) / float(longitude_infos[2].split('/')[1]) / 3600.0
            pic_coordinate = (latitude, longitude)
            # 获取时间戳
            pic_timestamp = contents['Image DateTime'].printable.replace(':','-')
            f.close()
        except:
            print('file type error,this is not a valid pictrue')
            continue
        # print(dir_file,pic_coordinate)
        # 遍历现有词典记性对比，如果满足距离要求，则建立文件夹并将照片剪切走。
        for key in coordinates_dict:
            dict_coordinate = coordinates_dict[key]
            distance = geodesic(pic_coordinate, dict_coordinate).meters
            if distance < threshold_distance:
                print(key, dir_file, distance, pic_coordinate, dict_coordinate)
                new_dir = pathout + '\\' + key
                if not os.path.exists(new_dir):
                    os.mkdir(new_dir)
                try:
                    new_file= pathout + '\\' + key + '\\' + dir_file.split('\\')[-1].split('.')[0] + '----' + pic_timestamp + '.' + dir_file.split('\\')[-1].split('.')[1]
                    if not os.path.exists(new_file):
                        shutil.move(dir_file, new_file)
                except:
                    print('file move error,check if the file already open in other app')


if __name__ == '__main__':
    # 直接试图读取txt文件，失败就报错
    pre_check = 0
    try:
        fr = open(os.getcwd() + "\\coordinate_dict.txt", 'r+', encoding='utf-8')
        coordinates_dict = eval(fr.read())
    except:
        pre_check = 1
        showinfo(title="错误提示", message="杆塔坐标字典不存在")
    # 直接试图读取设置文件，失败就报错
    try:
        fr = open(os.getcwd() + "\\threshold_distance.txt", 'r+', encoding='utf-8')
        threshold_distance_dict = eval(fr.read())
        threshold_distance = threshold_distance_dict['threshold_distance']
    except:
        pre_check = 1
        showinfo(title="错误提示", message="距离阈值字典不存在")

    if 0 == pre_check:
        jpgcategorize(filedialog.askdirectory(), os.getcwd(), coordinates_dict, threshold_distance)
