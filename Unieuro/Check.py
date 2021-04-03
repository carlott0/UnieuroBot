def get_form_details(form):
    """Returns the HTML details of a form,
    including action, method and list of form controls (inputs, etc)"""
    details = {}
    # get the form action (requested URL)id="paypal-prepare"
    action = form.attrs.get("action").lower()
    # get the form method (POST, GET, DELETE, etc)
    # if not specified, GET is the default in HTML
    method = form.attrs.get("method", "get").lower()
    # get all form inputs
    inputs = []
    forms= form.find_all("input") or form.find_all("button")
    for input_tag in forms:
        # get type of input form control
        input_type = input_tag.attrs.get("type", "text")
        # get name attribute
        input_name = input_tag.attrs.get("name")
        # get the default value of that input tag
        input_value =input_tag.attrs.get("value", "")
        # add everything to that list
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    # put everything to the resulting dictionary
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

#budget, link, mail di unieuro, pwd di unieuro, mail con cui inviare, pwd di essa, gmail a cui inviare
def check_price(budget,link, email, pwd, gMailF, pwdMail, gMailT):

  # import required files and modules
  import requests
  import random
  from bs4 import BeautifulSoup
  import pyautogui as pag
  from urllib.parse import urljoin
  from requests_html import HTMLSession
  from email import encoders
  from email.mime.base import MIMEBase
  from email.mime.multipart import MIMEMultipart
  from email.mime.text import MIMEText
  import smtplib
  import sys
  
  user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36']
  url = 'https://httpbin.org/headers'
  

  #Pick a random user agent
  user_agent = random.choice(user_agent_list)
  #Set the headers 
  headers = {'User-Agent': user_agent}
  # send a request to fetch HTML of the page
  response=(requests.get(link, headers=headers))

  # create the soup object
  soup=(BeautifulSoup(response.content, 'html.parser'))

  # change the encoding to utf-8
  soup.encode('utf-8')

  # function to check if the price has dropped
  product_title = soup.find(class_= "subtitle")
  if product_title is not None:
    title = product_title.get_text()
  else:
    title = "Nome non trovato"

  product_price = soup.find(class_="price")
  
  if product_price is not None:
    price = product_price.get_text().replace(',', '.').replace('€', '').replace(' ', '').strip()
  else:
    price= "999999"


  print(title.strip())
  print(price)
  available=soup.find('div', class_='product-availability-mobile')

  if available.text.strip() == "Non Disponibile":
      print("Prodotto non disponibile ")
      return "no"

  #converting the string amount to float
  converted_price = float(price[0:5])
  if(converted_price < budget):
    print("sceso di prezzo")
    if True == True:
        #if pag.confirm(text="sceso di prezzo, aggiungere al carrello?", title=title, buttons=['Si', 'No'])=='Si':
        #decommentare la riga sopra e commentare l'if True==True se si vuole chiedere la conferma di inserire nel carrello
        session = HTMLSession()
        
        #accedo a unieuro
        link3="https://www.unieuro.it/online/login"
        response=(requests.get(link3, headers=headers))
        soup=(BeautifulSoup(response.content, 'html.parser'))
        formRis=get_form_details(soup.find('form', id='loginForm'))

        data = {}
        count=0
        for input_tag in formRis["inputs"]:
            if input_tag["type"] == "hidden":
                # if it's hidden, use the default value
                data[input_tag["name"]] = input_tag["value"]
            elif input_tag["type"] != "submit":
                # all others except submit, prompt the user to set it
                #value = input(f"Enter the value of the field '{input_tag['name']}' (type: {input_tag['type']}): ")
              
                if input_tag["name"] == "j_username":
                    data[input_tag["name"]] = email.strip()
                
                if input_tag["name"] == "j_password":
                    data[input_tag["name"]] = pwd.strip()
                if input_tag["name"] == "_spring_security_remember_me":

                    data[input_tag["name"]]= ""
         
        
        urll = urljoin(link3, formRis["action"])
        if formRis["method"] == "post":
            res = session.post(urll, data=data)
        elif formRis["method"] == "get":
            res = session.get(urll, params=data)
           

        if res.status_code==200:
            print("Acceduto con successo a unieuro")
        else:
            print("Errore nell'accesso a unieuro")
            return "no"
        code=""
        response=(requests.get(link, headers=headers))
        soup=(BeautifulSoup(response.content, 'html.parser'))
        formRis=get_form_details(soup.find('form', id='inStockNotification'))
        if soup.find('a', class_='btn btn-orange-normal js--warranty-btn mobile-hide') is not None:
            code=soup.find('a', class_='btn btn-orange-normal js--warranty-btn mobile-hide')['data-sku']
        elif soup.find('a', class_='btn btn-orange-normal addtocart addToCartClick') is not None:
            code=soup.find('a', class_='btn btn-orange-normal addtocart addToCartClick')['data-sku']
        data = {}
        
        for input_tag in formRis["inputs"]:
            if input_tag["type"] == "hidden":
                # if it's hidden, use the default value
                #data[input_tag["name"]] = input_tag["value"]
                #value = input(f"Enter the value of the field '{input_tag['name']}' (type: {input_tag['type']}): ")
                data[input_tag["name"]] = code or ""
            elif input_tag["type"] != "submit":
                # all others except submit, prompt the user to set it
                #value = input(f"Enter the value of the field '{input_tag['name']}' (type: {input_tag['type']}): ")
                data[input_tag["name"]] = ""

        
        urll = urljoin(link, "/online/precart/producttile/add")
        if formRis["method"] == "post":
            res = session.post(urll, data=data)
        elif formRis["method"] == "get":
            res = session.get(urll, params=data)
        
        if res.status_code==200:
            print("Elemento aggiunto con successo al carrello!")
            

            #Le righe sucessive servono per uno sviluppo futuro per acquistare direttamente tramite paypal
            """
           

            formRis=get_form_details(soup.find('form'))	
            data = {}

            for input_tag in formRis["inputs"]:
                if input_tag["type"] == "hidden":
                    # if it's hidden, use the default value
                    data[input_tag["name"]] = input_tag["value"]
                elif input_tag["type"] != "submit":
                    # all others except submit, prompt the user to set it
                    value = input(f"Enter the value of the field '{input_tag['name']}' (type: {input_tag['type']}): ")
                    data[input_tag["name"]] = value
            print(formRis)
            print(data)
            urll = urljoin(res.url, "/online/precart/paypalec/prepare")
            if formRis["method"] == "post":
                res = session.post(urll, data=data, proxies=proxy)
            elif formRis["method"] == "get":
                res = session.get(urll, params=data, proxies=proxy)
                
            print(res.status_code)

            
            
            """
        else:
            print("Errore, non sono riuscito ad aggiungere al carrello.")
            return "no"
       
        conn = smtplib.SMTP('smtp.gmail.com', 587) # smtp address and port
        conn.ehlo() # call this to start the connection
        conn.starttls() # starts tls encryption. When we send our password it will be encrypted.
        conn.login(gMailF,pwdMail)#email e pwd di gmail
        body="Aggiunto al carrello \n" +title.strip()+ " "+str(converted_price)
        message = MIMEMultipart()
        message = MIMEMultipart()
        message["From"] = gMailF
        message["To"] = gMailT
        message["Subject"] = "Aggiunto elemento al carrello!!"
        message.attach(MIMEText(body, "plain"))
        text = message.as_string()
        conn.sendmail(gMailF, gMailT, text )
        conn.quit()
        print("inviata mail di conferma di aggiunta al carrello"  )

        
        
        if pag.confirm(text="Continuare con gli acqisti? ",  title="Attenzione", buttons=['Continua','Cancel'])=="Cancel":
            return "ok"
        
  else:
    print("Non è sceso di prezzo")
    return "no"
  print("\n")
  return "no"
