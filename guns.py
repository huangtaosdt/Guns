
# coding: utf-8

# In[1]:

'''
读入数据
提取表头--处理缺失值---提取年份，统计每年死亡人数

'''


# In[160]:

import csv
data=list(csv.reader(open('./data/guns.csv','r')))
headers=data[:1]
data=data[1:]
print(headers)
print(data[:5])


# In[15]:

#每个月的死亡人数
from datetime import datetime
date=[datetime(int(row[1]),int(row[2]),1) for row in data]

date_counts={}
for row in date:
    if row in date_counts:
        date_counts[row]+=1
    else:
        date_counts[row]=1
print(date_counts)


# In[192]:

#counting guns-death,group by year,race and sex respectively.
def count_column(data,col):
    col_counts={}
    for row in data:
        if row[col] in col_counts:
            col_counts[row[col]]+=1
        else:
            col_counts[row[col]]=1
    return col_counts
year_counts={}
race_counts={}
sex_counts={}
year_counts=count_column(data,1)
race_counts=count_column(data,7)
sex_counts=count_column(data,5)


#Plotting bar plot
import matplotlib.pyplot as plt
from numpy import arange
import numpy as np
bar_positions = arange(len(sex_counts))


fig=plt.figure(figsize=(6,10))
ax1=fig.add_subplot(2,1,1)
ax2=fig.add_subplot(2,1,2)
ax1.bar(bar_positions,sex_counts.values(),width=0.3)
ax1.set_xticks(bar_positions)
ax1.set_xticklabels(sex_counts.keys())
ax1.set_xlabel('Sex')
ax1.set_ylabel('Numbers')
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)

race_counts=sorted(race_counts.items(), key=lambda x: x[1],reverse=True)
race_counts=dict(race_counts)
ax2.bar(arange(len(race_counts)),race_counts.values(),width=0.5,color='orange')
ax2.set_xticks(arange(len(race_counts)))
ax2.set_xticklabels(race_counts.keys(),rotation=-80)
ax2.set_xlabel('Race')
ax2.set_ylabel('Numbers')
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)

plt.show()





# In[91]:

census=list(csv.reader(open('./data/census.csv','r')))
print(census)
# In[93]:
#统计种族死亡率
#种族分类：
#Asian/Pacific Islander, Black, Native American/Native Alaskan, Hispanic, and White
race_total={"Asian/Pacific Islander":15159516+674625, "Black":40250635, "Native American/Native Alaskan":3739506, "Hispanic":44618105,"White":197318956}
race_per_hundredk={}
for row in race_total:
    race_per_hundredk[row]=race_counts[row]/race_total[row]*1e5
print(race_per_hundredk)


# In[193]:

#统计种族他杀率
intents=[row[3] for row in data]
races=[row[7] for row in data]
homicide_race_per_hundredk={}
for i,intent in enumerate(intents):
    if intent=='Homicide':
        if races[i] in homicide_race_per_hundredk:
            homicide_race_per_hundredk[races[i]]+=1
        else:
            homicide_race_per_hundredk[races[i]]=1
for race in homicide_race_per_hundredk:
    homicide_race_per_hundredk[race]=homicide_race_per_hundredk[race]/race_total[race]*1e5
print(homicide_race_per_hundredk)

#display
sorted_dict=sorted(homicide_race_per_hundredk.items(), key=lambda x: x[1],reverse=True)
sorted_dict=dict(sorted_dict)
fig,ax=plt.subplots()
ax.barh(arange(len(homicide_race_per_hundredk)),sorted_dict.values())
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_yticks(arange(len(sorted_dict)))
ax.set_yticklabels(sorted_dict.keys())
ax.set_xlabel('homicide_race_per_hundredk')
plt.show()

