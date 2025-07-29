from flask import Flask, render_template,request
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import webbrowser
import threading
from selenium import webdriver
import time

app = Flask(__name__)


def cnbcscrap( datelimit):

    url = "https://www.cnbc.com/investing/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    # el eed eli hatdoos 3ala el load moer
    driver = webdriver.Chrome() 
    driver.get("https://www.cnbc.com/investing/")


    for _ in range(3):
      try:
        lm = driver.find_element("css selector", "button.LoadMoreButton-loadMore")
        lm.click()
        time.sleep(2)  
      except:
        break  

    html = driver.page_source

    
    soup = BeautifulSoup(html, 'lxml')

    articles=[]
    cards = soup.find_all("div", class_="Card-titleContainer")
    cards2 = soup.find_all("div", class_="Card-pro")

    
    

    for card in cards2:
        at = card.find('a',class_="Card-title")  
        if at and at.has_attr('href'):
           
            href = at['href']
            title = at.get_text(strip=True)

            try:
                parts = href.split('/')
                year, month, day = int(parts[3]), int(parts[4]), int(parts[5])
                articledate = datetime(year, month, day)

                if articledate >= datelimit:
                     articles.append({
                        'url': href,
                        'title': title,
                        'date': articledate.strftime('%Y-%m-%d')
                    })
            except (IndexError, ValueError):
                continue

            
   
    for card in cards:
        atag33 = card.find('a',class_="Card-title")  
        if atag33 and atag33.has_attr('href'):
           
            href = atag33['href']
            title = atag33.get_text(strip=True)

            try:
                parts = href.split('/')
                year, month, day = int(parts[3]), int(parts[4]), int(parts[5])
                articledate33 = datetime(year, month, day)

                if articledate33 >= datelimit:
                  articles.append({
                        'url': href,
                        'title': title,
                        'date': articledate33.strftime('%Y-%m-%d')
                    })
            except (IndexError, ValueError):
             
                continue

    return articles

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/articles", methods=["GET"])
def articles22():
    input_date = request.args.get("date") 
    datelimit = datetime.strptime(input_date, "%Y-%m-%d") 
    articles2 = cnbcscrap(datelimit) 
    return render_template("articles.html", articles=articles2)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    app.run(debug=True, use_reloader=False) 
