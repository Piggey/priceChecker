import requests, smtplib, time, os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler
load_dotenv()
sched = BlockingScheduler()

def sendMail():
    try:
        email = os.getenv("EMAIL_LOGIN")
        password = os.getenv("EMAIL_PASSWORD")
    except:
        print("Loading email essentials FAILED!")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(email, password)
    subject = "Price update on an item you want to check."
    body = "The price on " + nameOfProduct + " has changed. Check it on " + url + "\n\nPenis."
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(email, email, msg)
    print("Price has changed. Email has been sent.")
    server.quit()

def checkItem(item_url):
    headers = {"User_agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    global url
    global nameOfProduct
    url = item_url
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    old_price = Items[url]

    nameOfProduct = soup.find('h1', {'class':'prod-name'}).get_text()
    price = float(soup.find("div", {'class':"price-new"}).get_text().strip(' zł').replace(" ", ""))

    print("Item currently being checked: " + nameOfProduct)
    print("Checking...")
    print("Old price: " + str(old_price))
    print("New price: " + str(price))
    
    if(price < old_price):
        print("Price has changed. Sending an email...")
        sendMail()
        print("Email sent!\n")
    else:
        print("Price has not changed. Trying again in 12 hours.\n")

    Items[url] = price

itemList = open("item_list.txt", 'r')
Items = {}
for line in itemList:
    x = line.split(";")
    a = x[0]
    b = float(x[1].strip("\n"))
    Items[a] = b

@sched.scheduled_job('interval', hours=24)
def scheduled_job():
    for url in Items:
        checkItem(url)

sched.start()