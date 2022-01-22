import requests
from requests_html import HTMLSession
import re
import json
import time
import csv
import urllib.request
import sys
import os
   
# START CONFIGURATION PARAMS

# Url to csv database in your Google Drive folder
FILENAME_URL = "https://drive.google.com/file/DATABASE_template.csv"

# Full server route to last post Id filename
DATABASE_FILENAME = "/home/ubuntu/id_aliexpress.txt"

# Your Telegram API Token
TELEGRAM_API_TOKEN = ""

# YOur Telegram ChatID (Ej: 111111111  o '@sales_channel')
TELEGRAM_CHATID = ""



# END CONFIGURATION PARAMS

#------------------------- FUNCTIONS --------------------------#

def read_csv_url(url):
    file_id = url.split('/')[-2]
    dwn_url='https://drive.google.com/uc?export=download&id=' + file_id
    response = urllib.request.urlopen(dwn_url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    return csv.reader(lines, delimiter=';')

def read_db_file():
    if(os.path.exists(DATABASE_FILENAME)):
        f = open(DATABASE_FILENAME, 'r', encoding='utf-8')
        data = f.readline().strip()
        f.close()
        return data
    else:
        return False

def write_db_file(data):
     f = open(DATABASE_FILENAME, 'w', encoding='utf-8')
     f.write(str(data))
     f.close()
     return True

def get_aliexpress(url):
    try:
        dopost = False
        session = HTMLSession()
        r = session.get(url[0])
        title_price = re.search('<meta property="og:title" content="(.*?)" />', r.text)
        image = re.search('<meta property="og:image" content="(.*?)"/>', r.text)
        if ( (title_price is not None) and (image is not None)): 
            title_price = title_price[1].split("|")
            if "US $" in title_price[0]:
                title_price[0] = title_price[0].replace(" de DESCUENTO", " OFF")
            if "DESCUENTO" in title_price[0]:
                price_discount = title_price[0].replace(" de DESCUENTO", "")
                price_discount = price_discount.split(" ")
                original_price = round( (float(price_discount[0].replace("€", "")))*100/(100-int(price_discount[1].replace("%", ""))), 2)
                str_original_price = '\nAntes: '+str(original_price)+'€'
                str_discount = ' (*'+price_discount[1]+'* descuento)\U0001F525'
            elif "OFF" in title_price[0]:
                price_discount = title_price[0].replace(" OFF", "").replace(" $", "")
                price_discount = price_discount.split(" ")
                original_price = round( (float(price_discount[0].replace("US", "")))*100/(100-int(price_discount[1].replace("%", ""))), 2)
                str_original_price = '\nAntes: $'+str(original_price)+' USD'
                str_discount = ' (*'+price_discount[1]+'* descuento)\U0001F525'
            else:
                price_discount = []
                price_discount.append(title_price[0]+'\U0001F525')
                str_discount = ''
                str_original_price = ''
            if(url[1] is not None and image[1] is not None and title_price[0] is not None and title_price[1] is not None and price_discount[0] is not None and str_discount is not None and str_original_price is not None):
                print(title_price[0])
                print(title_price[1])
                print(image[1])
                dopost = True
            else:
                print("Offer not posted in Telegram because title, price or image was not found.")
            print("----------------------------------------------------------------")
            # Post to Telegram
            url2 = "https://api.telegram.org/bot"+TELEGRAM_API_TOKEN+"/sendMessage"
            reply = json.dumps(
                {
                    'inline_keyboard': [
                        [{'text': '\U00002b50 Ver oferta \U00002b50', 'url': url[1]}],
                        [{'text': '\U00002728 Más canales con ofertas \U00002728', 'url': 'https://yourweb.com/directory/'}],
                        [
                            {'text': 'Instagram', 'url': 'https://instagram.com/youraccount'}, 
                            {'text': 'Facebook',  'url': 'https://facebook.com/youraccount'},
                            {'text': 'Blog',      'url': 'https://yourweb.com'},
                            {'text': 'Pinterest', 'url': 'https://pinterest.com/youraccount'}
                        ]
                    ]
                }
            )
            if(dopost):
                params = {
                    'chat_id': TELEGRAM_CHATID, 
                    'photo': image[1],
                    'parse_mode' : 'Markdown',
                    'text' : '[​​​​​​​​​​​]('+image[1]+')'+title_price[1]+'\n\n\U0001F525*'+price_discount[0]+'*'+str_discount+''+str_original_price,
                    'reply_markup' : reply
                } 
                r = requests.post(url2, params=params)
    except requests.exceptions.RequestException as e:
        print(e)




def main():
    iddatabase = read_db_file()
    if(iddatabase==False):
        write_db_file("1")
    data = read_csv_url(FILENAME_URL)
    data_list = list(data)
    total_links = len(data_list)-1
    if ((total_links % int(iddatabase) == 0) and (int(iddatabase)!=1)):
        print("**** Last row in csv proccesed. Starting from first row... ****")
        write_db_file("1")
    else:
        print("**** READING ROW ID:" +iddatabase+" of .csv  ****")
        write_db_file(int(iddatabase)+1)
    if len(data_list)>1:
        if 'https://es.aliexpress.com/item/' in data_list[int(iddatabase)][0]:
            get_aliexpress(data_list[int(iddatabase)])
        else:
            print("CSV empty")


#----------------------- MAIN PROGRAM -------------------------#

data_list = []

if __name__ == "__main__":

    main()



