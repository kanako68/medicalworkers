import subprocess as sp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys,os

if os.path.exists('./data.csv'):
  df = pd.read_csv('data.csv')
else:
  # sp.call("wget https://raw.githubusercontent.com/kanako68/medicalworkers/main/data.csv")
  df = pd.read_csv('https://raw.githubusercontent.com/kanako68/medicalworkers/main/data.csv')
  
df = df[["Location","Period","FactValueNumeric"]]

#国リストに国入れる
countries=[]
for i in df.Location:
  if i not in countries :
    countries.append(i)
# print(len(countries),': ',countries)
print(len(countries))

kari=sys.argv
# kari=['unti','Japan','Yemen','New Zealand','India']
no=len(kari)-1
print(kari)

#ナンバーリスト
no=len(kari)-1
cnt=[]
print(no)
#国リストに入力値があったらプリントして、gropbyしてcntリストに入れる

for i in range(no):
  if kari[i+1] in countries:
    print(kari[i+1])
    # cnt.append(df.loc[df.Location==kari[i+1]])
    cnt.append(df.groupby('Location').get_group(kari[i+1]))
    # print(cnt)
  else: 
    print('correct the name of ',kari[i+1])

# print(cnt)

#リストに変換・欠損地埋める
newdata=[]
for j in range(len(cnt)):
  df=cnt[j]
  df=df.loc[: , ['Period','FactValueNumeric']]
  print(df)
  new = sorted(df.values.tolist())
  cntry=[]
  no=0
  

  for i in range(2010,2021):
    if no >= len(new) or i not in new[no]:
      cntry.append(0)
    else:
      cntry.append(new[no][1])  
      no+=1    
  newdata.append(cntry)

# print(newdata)
print(len(newdata))

df_ = pd.DataFrame(newdata).replace([0], np.nan).T
# print(df_)
pltdata=sum((df_.fillna(method='ffill').fillna(method='bfill').T).values.tolist(), [])
print(pltdata)
print(len(pltdata))

x=[]
for i in range(2010,2021):
  x.append(i)

if len(cnt)==1:
  plt.plot(x,pltdata,'k-',label=kari[1])
if len(cnt)==2:
  plt.plot(x,pltdata[0:11],'k-',label=kari[1])
  plt.plot(x,pltdata[11:22],'k--',label=kari[2])
if len(cnt)==3:
  plt.plot(x,pltdata[0:11],'k-',label=kari[1])
  plt.plot(x,pltdata[11:22],'k--',label=kari[2])
  plt.plot(x,pltdata[22:33],'k:',label=kari[3])
if len(cnt)==4:
  plt.plot(x,pltdata[0:11],'k-',label=kari[1])
  plt.plot(x,pltdata[11:22],'k--',label=kari[2])
  plt.plot(x,pltdata[22:33],'k:',label=kari[3])
  plt.plot(x,pltdata[33:44],'k-.',label=kari[4])


def main():
  plt.legend()
  plt.savefig('result.png')
  plt.yticks( np.arange(min(pltdata), max(pltdata),  (max(pltdata)-min(pltdata))/10))
  plt.show()
  
if __name__ == "__main__":
  main()