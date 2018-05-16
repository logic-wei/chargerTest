#-*- coding: UTF-8 -*-

import matplotlib.pyplot as plt
import re
import tkFileDialog

log_path = r"/home/weipeng/mytemp/m1871/log-chargeProfile/chargingProcess.txt" # default path
pattern_all=r"^timeCount=(.*)\s+boardTemp=(.*)\s+batteryTemp=(.*)\s+batteryCurrent=(.*)\s+soc=(.*)\s+"
title=("timeCount","boardTemp","batteryTemp","batteryCurrent","soc")
re_all=re.compile(pattern_all)

#log_path=tkFileDialog.askopenfilename()


# parse data
keyWordLenth=len(title)
x=[]
y=[]
for i in range(0,keyWordLenth):
    y.append([])

file=open(log_path)
line=file.readline()
while line:
    match=re_all.match(line)
    if match :
        for i in range(0,keyWordLenth):
            y[i].append(int(match.group(i+1)))
    line = file.readline()
x=range(len(y[0]))

# draw data
fig,axes=plt.subplots(nrows=len(y))
for i in range(0,keyWordLenth):
    axes[i].plot(x,y[i])
    axes[i].set_title(title[i])
    axes[i].spines['right'].set_visible(False)
    axes[i].spines['top'].set_visible(False)
    print(i)
fig.suptitle("file:"+log_path)

plt.subplots_adjust(hspace=1)
plt.show()