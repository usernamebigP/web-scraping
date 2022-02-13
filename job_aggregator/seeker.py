from bs4 import BeautifulSoup
from urllib.request import urlopen,Request
import csv
import re
import requests

urls=[{"url_name":"indeed","url":"https://www.indeed.co.in/jobs?q={}&l={}&start={}","class_tag":"div","class":"jobsearch-SerpJobCard unifiedRow row result clickcard","encoding":True,"start_range":10},
      {"url_name":"linkedin","url":"https://in.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={}&location={}&start={}","class_tag":"li","class":"result-card job-result-card result-card--with-hover-state","encoding":False,"start_range":20},
      ]
      
f1="engineer";f2="Delhi"

for url in urls:
    with open("data_"+url["url_name"]+".csv","a") as dataFile:
        writer=csv.writer(dataFile)
        try:
            print(url["url_name"]+" jobs")
            for start in range(0,100,url["start_range"]):
                html_doc=requests.get(url["url"].format(f1,f2,start),headers=headers).content
                soup=BeautifulSoup(html_doc,'html.parser')
                #to deal with encoding error
                if(url['encoding']==True):
                    with open("x.html","w",encoding="utf-8") as f:
                        f.write(str(soup))

                    with open("x.html","r") as f:
                        new_html=f.read()
                        new_soup=BeautifulSoup(new_html,"html.parser")
                        soup=new_soup        

                #extracting the job blocks    
                blocks=soup.find_all(url["class_tag"],class_=url["class"].split(' '))

                for block in blocks:
                    #print(block)
                    title=block.select_one("[class*=title]").text.strip()
                    company=(block.select_one("[class*=subtitle]") or block.select_one("[class*=company]")).text.strip()
                    location=block.select_one("[class*=location]").text.strip()
                    salary=block.select_one("[class*=salary]")
                    link=block.select_one("a")['href']

                    #url issues 
                    if(url["url_name"] not in link):
                        link="https://www."+url["url_name"]+".com"+link

                    #if salary not present
                    if(not salary == None):
                        salary=salary.text.strip()
                    else:
                        salary=""
                    data=[title,company,location,salary,link]
                    writer.writerow(data)
            print(url["url_name"]+"done")
        except Exception as e:
            print(e)