import requests, smtplib, time, os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
load_dotenv()

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
    body = "The price on " + nameOfProduct + " fell down. Check it on " + url + "\n\nPenis."
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(email, email, msg)
    print("Price has changed. Email has been sent.")
    server.quit()

def checkItem(item_url):
    global url
    global nameOfProduct
    headers = {"User_agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    old_price = 0
    url = item_url
    
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content,'html.parser')

    nameOfProduct = soup.find('h1',{'class':'prod-name'}).get_text()
    price = float(soup.find("div",{'class':"price-new"}).get_text().strip(' zł').replace(" ", ""))


    print("Item currently being checked: " + nameOfProduct)
    print("Checking...")
    print("Old price: " + str(old_price))
    print("New price: " + str(price))
    
    if(price < old_price):
        print("Price has changed. Sending an email...")
        sendMail()
        print("Email sent!\n")
    else:
        print("Price has not changed. Trying again in 24 hours.\n")
    
    old_price = price



print("Starting up.")
itemList = open("item_list.txt", 'r').read().split("\n")
while(True):
    for item in itemList:
        checkItem(item)
    time.sleep(86400)