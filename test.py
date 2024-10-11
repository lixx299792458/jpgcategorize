# dic = { 'andy':{ 'age': 23, 'city': 'beijing', 'skill': 'python' },
#         'william': { 'age': 25, 'city': 'shanghai', 'skill': 'js' }
#         }
# fw = open("test.txt",'w+')
# fw.write(str(dic)) #把字典转化为str
# fw.close()

fr = open("coordinate_dict.txt",'r+',encoding='utf-8')
dic = eval(fr.read())   #读取的str转换为字典
print(dic)
fr.close()