import requests
from bs4 import BeautifulSoup as bs
import smtplib
import csv

#function to send mail
def send_mail():
	server=smtplib.SMTP("smtp.gmail.com",587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login("prateek007.purohit@gmail.com","tiidyadwbxkdussb")

	subject=title[:10] + " price have fallen!!!"
	body="Check the link given: " + url

	msg="Subject:{0} \n\n{1}".format(subject,body)

	server.sendmail(
		"prateek007.purohit@gmail.com",
		"pprateek180@gmail.com",
		msg
	)

	server.quit()

#function to  check reduction in prices
def isReduced(latest_price,old_price):
	if(latest_price < old_price*0.9):
		return True
	return False

#function to check price
def check_price(soup,old_price):
	#check availability
	available=soup.find(id="availability").span.get_text().strip()

	if(available and not available == "Currently unavailable."):
		price=soup.find(id="priceblock_ourprice").get_text()
		price=float(price[0:5])
		
		if(isReduced(price,old_price):
			send_mail()
	return price		

#main
with open("urls.csv","r") as f:
	data=csv.reader(f)
	next(urls)
	headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0"}
	
	with open("urls.csv","w") as f2:
		new_data=csv.writer(f2)
		
	for url,old_price in data:
		html_doc=requests.get(url,headers=headers)
		soup=bs(html_doc.content,"html.parser")

		#title of the product
		title=soup.find(id="productTitle").get_text().strip()
		
		#check any major change in prices
		latest_price=check_price(soup,price)
		
		#update prices in csv file
		update=url+","+latest_price 
		new_data.write_row(update)
