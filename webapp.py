import requests 
from bs4 import BeautifulSoup
import numpy as np
from flask import Flask,render_template,url_for,request,jsonify
import json
from werkzeug.exceptions import HTTPException
import random


app = Flask(__name__)

@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "error": "Something went wrong, check url again."
    })
    response.content_type = "application/json"
    return response



#-------user agents rotating---------#
def user_agents():
    uastrings = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
                "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",\
                "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"\
                ]


#-------Currency convert function---------#
def convert():
    url="https://www.google.com/search?q=aed+to+pkr+&sxsrf=ALeKk02To4yhBWpyI9HXCdFIBf4NCDTIXQ%3A1616665927504&ei=R11cYNSdHtOs1fAPidWquAk&oq=aed+to+pkr+&gs_lcp=Cgdnd3Mtd2l6EAMyBAgjECcyBAgjECcyBQgAEJECMgUIABCRAjIFCAAQsQMyCAgAEMkDEJECMgUIABCRAjICCAAyAggAMgIIADoHCAAQRxCwAzoGCAAQFhAeUMjTDlj54g5glOcOaAFwAngAgAGlA4gBhhWSAQgyLTEwLjAuMZgBAKABAaoBB2d3cy13aXrIAQjAAQE&sclient=gws-wiz&ved=0ahUKEwiU3dDylcvvAhVTVhUIHYmqCpcQ4dUDCA0&uact=5"
    headers=user_agents()
    headers={'User-Agent': headers}
    r = requests.get(url, headers=headers)
    soup=BeautifulSoup(r.text,"html.parser")
    a=soup.find("div",{"class":"BNeawe iBp4i AP7Wnd"})
    a=a.text
    a=a[:-16]
    a=float(a)
    return a

    
#-----------------For all Amazon categories ---------!
@app.route("/amazon/<int:page_no>",methods=['POST'])
def amazon(page_no):
    url = request.form.get('url')
    headers=user_agents()
    headers={'User-Agent': headers}
    #url = request.form.get('url')
    rate=convert() #currency conversion rate
    url1=url+str("&page={page}".format(page=page_no))
    str1=url1.find("11995849031")
    str2=url1.find("11995844031")
    str3=url1.find("15399111031")
    str4=url1.find("16566959031")
    str5=url1.find("15399096031")
    str6=url1.find("11497631031")
    if str1 !=-1 or str2 != -1 or str3 !=-1 or str4 !=-1 or str5 !=-1 or str6 !=-1 :
        class1="a-section a-spacing-medium a-text-center"
    else:
        class1="a-section a-spacing-medium"

    r = requests.get(url1, headers=headers)
    soup =  BeautifulSoup(r.text, 'html.parser')
    ab=[]
    b=[]
    a=[]
    s=[]
    for i in soup.find_all("li",{"class":"a-disabled"}):
        b=i.text
        a.append(b)  

    if b==[]:
        pages=1
        pages1={
        'total pages':pages
        }
    elif b=="←Previous":
        for i in soup.find_all("li",{"class","a-normal"}):
            b=i.text
            s.append(b)
        pages=s[-1]
        pages1={
        'total pages':pages
        }
    else:
        pages=int(b)
        pages1={
            'current_page':page_no,
            'pages_remaining':pages-page_no
        }
                
    for i in soup.find_all("div",{"class":class1}):
        info3=[]
        info2=[]
        images1=[]
        products=i.find("span",{"class":"a-color-base"})
        prices=i.find("span",{"class":"a-price-whole"})
        images=i.find('img').attrs['src']
        tag=i.find("i",{"class":"a-icon a-icon-prime a-icon-medium"})

        #--------------------------description 2nd page--------------------------------------------#
        link=i.find("a",{"class","a-link-normal s-no-outline"})
        link=str("https://www.amazon.ae"+link['href'])
        r = requests.get(link, headers=headers)
        soup=BeautifulSoup(r.content,"lxml")
        for i in soup.find_all("ul",{"class":"a-unordered-list a-vertical a-spacing-mini"}) :
            info=i.text
        for i in soup.find_all("table",{"class":"a-spacing-micro"}):
            info2=i.text
        for i in soup.find_all("ul",{"class":"a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list"}):
            info3.append(i.text)
            
        for i in soup.find_all("span",{"class":"a-button-text"}):
            images2=i.find_all('img')
            for image in images2:
                images1.append(image['src'])
        images1.pop()
        
        #------------------Price conversion--------------------------------------------#
        if tag is not None and prices is not None:
            products=products.text
            prices=[prices.text]
            images=images
            prices = [x[:-1] for x in prices]
            prices=([s.replace(',', '') for s in prices])
            prices = [int(i) for i in prices] 
            prices = [int(element *rate) for element in prices]
            prices1 = [int(element *2.5/100) for element in prices]
            arr1 = np.array(prices)
            arr2 = np.array(prices1)
            prices= int(arr1 + arr2)
            info=info.replace('\n','')
            info=info.replace('P.when(\"ReplacementPartsBulletLoader\").execute(function(module){ module.initializeDPX(); })','')
            info2=str(info2)
            info2=info2.replace('\n',' ')
            all_images=images1  
            if not info3:
                Asin="not available"
                item="not available"
                Dimensions="not available"
            else:
                info4=info3[0]
                info4=info4.replace('\n','')
                Dimensions=info4.split('Date')[0]
                #Manufacturer=info4.split('number')[1]
                #Manufacturer1=Manufacturer.replace(':','')
                ASIN=info4.split('ASIN')[1]
                ASIN1=ASIN.split('Item')[0]
                ASIN_Final=ASIN1.replace(':','')
                Asin=str("ASIN:")+ASIN_Final
                #item=str("Item model number:")+Manufacturer1
            INFO={
                'images':images,
                'title':products,
                'prices':prices,
                'info':info,
                'info2':info2,
                #'Dimensions':Dimensions,
                'Asin':Asin,
                #'item':item,
                'all_images':all_images
            }
            a=INFO['title'],INFO['prices'],INFO['images'],INFO['info'],INFO['info2'],INFO['Asin'],INFO['all_images']
            ab.append(a)
    for i in ab:
        return jsonify(pages1,ab)
    return jsonify(category_error="Something went wrong,make sure you're using correct endpoint for the category.")



if __name__ == "__main__":
    app.run(debug=True)

