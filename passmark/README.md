# cpu_gpu_passmark
用python采集pasmark的cpu和gpu跑分

```
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
f=open('cpu2.csv','a',newline='',encoding='GB18030')
csv_writer=csv.writer(f)
#CPU
#html=urlopen('https://www.cpubenchmark.net/high_end_cpus.html')
html=urlopen('https://www.videocardbenchmark.net/high_end_gpus.html')
bs=BeautifulSoup(html.read(),"html.parser")
nameList=bs.findAll("span",{"class":"prdname"})
countList=bs.findAll("span",{"class":"count"})
priceList=bs.findAll("span",{"class":"price-neww"})
csv_writer.writerow(["GPU","跑分","价格"])

for i in range(1,len(nameList)):
    msg1 = nameList[i].string
    msg2 = countList[i].string
    msg3 = priceList[i].string
    if(msg3=='NA'):
            msg3='暂无价格'
    csv_writer.writerow([msg1,msg2,msg3])
f.close()

```
