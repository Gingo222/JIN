import os

pwd = os.getcwd()
y = []
with open('./files/6.txt', 'r') as file_six:
    a = file_six.readlines()
    for x in a:
        x = x.replace('\n', ',\n')
        y.append(x)

os.remove('./files/66.txt')

for j in y:
    with open('./files/66.txt', 'a+') as file_six2:
        file_six2.write(j)