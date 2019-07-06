import requests, smtplib, time
from bs4 import BeautifulSoup

def sendMail():
    mail = 'pepcio3320@gmail.com'
    passw = 'wjxmmjvunxmkihgc'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('pepcio3320@gmail.com', passw)
    subject = "Price update on an item you want to check."
    body = "The price on " + nameOfProduct + " fell down. Check it on " + url + "\n\nPowered by literally a fucking genius. Penis."
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(mail,mail,msg)
    print("Price has changed. Email has been sent.")
    server.quit()

def checkItem():
    global url
    global nameOfProduct
    old_price = 409.0

    url = 'https://www.morele.net/monitor-acer-kg221qbmix-um-wx1ee-005-4585406/'
    headers = {"User_agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content,'html.parser')

    nameOfProduct = soup.find('h1',{'class':'prod-name'}).get_text()
    price = float(soup.find("div",{'class':"price-new"}).get_text().strip(' zł'))

    if(price < old_price):
        sendMail()
    
    old_price = price

while(True):
    checkItem()
    time.sleep(86400)