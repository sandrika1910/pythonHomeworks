import requests, json, keyboard, sqlite3
from time import sleep

phone_number = str(input('ჩაწერეთ ტელეფონის ნომერი: '))
payload = {
    'api_key':'6e5810406d5142ce83ed05b10f518778',
    'phone':phone_number
}
url = 'https://phonevalidation.abstractapi.com/v1/'

file_saved = False 

def request_data(url,param):
    r = requests.get(url,params=param)
    res_json = r.json()
    print('მოთხოვნა გაგზავნილია, დაელოდეთ...')
    sleep(1)
    if r.status_code != 200:
        print('ოპერაცია ვერ განხორციელდა, იხილეთ მიზეზი ---> ',r.reason)
    else:
        print('ოპერაცია განხორციელდა წარმატებით. ოპერაციის შესრულების დრო: ',r.elapsed)
        global file_saved
        if file_saved is False:
            with open('response.json','w',encoding='UTF-8') as f:
                json.dump(res_json,f,indent=4)
                print('ინფორმაცია შენახულია json ფორმატის ფაილში. ')
                file_saved = True 
                f.close() 
    r.close()
    return res_json   

choices = ['international','local','name','prefix','location']

''' ფუნქცია გამოიძახება მთავარ ფუნქციაში და გვიბრუნებს შედეგს იმის შესაბამისად თუ რომელ ღილაკს დააჭერს მომხმარებელი '''

json_f = open('response.json')
json_data = json.load(json_f)

def display_info(n,arg):
    if n == 1:
        return json_data['format'][str(arg)]
    elif n == 2:
        return json_data['country'][str(arg)]
    elif n == 3:
        return json_data[str(arg)]
    else:
        return display_info(n,arg)

def main_func():
    ''' ციკლი რომ მოხმარებელს გამოვუტანოთ სასურველი შედეგი '''
    wh_loop = True
    menu = True
    menu_info = 'რა მონაცემის გამოტანა გსურთ ეკრანზე?\n(1) საერთაშორისო მისამართი. (2) ადგილობრივი მისამართი. (3) ქვეყნის სახელი. (4) ნომრის პრეფიქსი. (5) მდებარეობა. (0) გასვლა'
    while wh_loop:
        if menu: 
            print(menu_info)
            menu = False
        try:
            if json_data['valid'] is True:
                while True:
                    if keyboard.is_pressed('1'):
                        print('საერთაშორისო მისამართი: ',display_info(1,'international'))
                        break
                    elif keyboard.is_pressed('2'):
                        print('ლოკალური მისამარ: ',display_info(1,'local'))
                        break
                    elif keyboard.is_pressed('3'):
                        print('ქვეყნის სახელი: ',display_info(2,'name'))
                        break
                    elif keyboard.is_pressed('4'):
                        print('ნომრის პრეფიქსი: ',display_info(2,'prefix'))
                        break
                    elif keyboard.is_pressed('5'):
                        print('მდებარეობა: ',display_info(3,'location'))
                        break
                    elif keyboard.is_pressed('0'):
                        print('თქვენ გადიხართ სისტემიდან...')
                        sleep(1)
                        wh_loop = False 
                        break
            else:
                print('ინფორმაცია ვერ მოიძებნა.')   
                break 
        except StopIteration:
            keyboard.write('დააჭირეთ ციფრს!\n')
        break # საბოლოოდ პროგრამა ეშვება მხოლოდ ერთხელ. აქ ვაილ ციკლის გამოყენება არც იყო საჭირო
        #       თუმცა სულ სხვა გზით დავიწყე კეთება და მერე გადავაკეთე კოდი და ვაილ ციკლიც დავტოვე 


# ბაზაში შესატანი ინფორმაცია
to_save_data = (payload['phone'],json_data['format']['international'],json_data['format']['local'],json_data['country']['name'],json_data['country']['prefix'],json_data['location'])

''' შევინახოთ ინფორმაცია ცხრილში '''
def save_info():
    print('მიმდინარეობს ბაზასთან დაკავშირება...')
    conn = sqlite3.connect('phone_number.sqlite')
    sleep(1)
    print('ბაზასთან კავშირი დამყარებულია. ')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS info 
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             phone INT,
             international_address CHAR,
             local_address INT,
             country_name CHAR,
             prefix CHAR,
             phone_location CHAR
            )
        ''')
    
    if json_data['valid'] is True:
        print('მიმდინარეობს ინფორმაციის შენახვა ბაზაში...')
        sleep(1)
        cursor.execute('INSERT INTO info (phone,international_address,local_address,country_name,prefix,phone_location) VALUES(?,?,?,?,?,?)',to_save_data)
        conn.commit()
        print('ოპერაცია დასრულდა წარმატებით. ')
    else:
        print('ინფორმაციის შენახვა ვერ მოხერხდა. ')
        
    conn.close()

def main():
    while True:
        inpt = int(input('შეიტანეთ შესაბამისი ციფრი.(1) ინფორმაციის გამოტანის სექცია. (2) მონაცემების შენახვის სექცია. გასვლა (0) : ') )
        request_data(url,payload)
        if inpt==1:
            main_func()
        elif inpt==2:
            save_info()
        elif inpt==0:
            break
    json_f.close()
main()