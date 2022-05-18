import sqlite3 
from sqlite3 import Error
import re
import matplotlib.pyplot as plt

def sql_connection():
    return sqlite3.connect('oscar_winners.sqlite')

conn = sql_connection()
cursor = conn.cursor()

#for filter inputed name and surname and insert them into one string to display full name 
def fixName(name,surname):
    name_lst = []
    surname_lst = []
    #remove spaces from name and surname
    for words in name.split():
        name_lst.append(words)
    for words in surname.split():
        surname_lst.append(words)

    new_name_str = ''
    new_surname_str = ''
    counter = 0
    
    #first loop for name(check if character is string and not other something symbol)
    for x in name_lst:
        new_name_str = ''.join(filter(str.isalnum,name_lst[counter]))
        name_lst[counter] = new_name_str
        counter += 1
        new_name_str = ''
    counter = 0
    
    #second loop for surname(check if character is string and not other something symbol)
    for x in surname_lst:
        new_surname_str = ''.join(filter(str.isalnum,surname_lst[counter]))
        surname_lst[counter] = new_surname_str
        counter += 1
        new_surname_str = ''
    last_name_lst = []
    last_surname_lst = []
    
    #second for name
    for x in name_lst:
        if len(x) > 1:
            for i in range(len(x)):
                last_name_lst.append(x[i])
        else:
            last_name_lst.append(x)
            
    #second for surname
    for x in surname_lst:
        if len(x) > 1:
            for i in range(len(x)):
                last_surname_lst.append(x[i])
        else:
            last_surname_lst.append(x)
            
    last_name = ''.join(a for a in last_name_lst)
    last_surname = ''.join(a for a in last_surname_lst)
    last_full_name = last_name.capitalize()+' '+last_surname.capitalize()
    
    return last_full_name

def display_info_by(inp,value):
    cursor.execute("SELECT * FROM oscar WHERE {}={}".format(inp,value))
    data = cursor.fetchall()
    for x in range(len(data)):
        print("section{}\nyear: {}, winner's name: '{}', winner's age: {}, winner's gender: '{}', movie name: '{}'\n".format(x+1,data[x][1],data[x][3],data[x][2],data[x][4],data[x][5]))
    
def display_info():
    print('you entered to the information displaying mode.')
    stop = False
    while not stop:
        user_input = 200
        try:
            user_input = int(input('Enter number: (1)display by years. (2) display by winners age. (3) display by winners name. (4) display by movie name. (0)Exit:'))
        except ValueError:
            print('error occured. enter integer.')
            
        if user_input == 1:
            #ask user to enter year
            user_ask = True
            while user_ask:
                by_year = 0
                try:
                    by_year = int(input('Enter year:'))
                except ValueError:
                    print('enter integer.')
                if by_year not in [x for x in range(1926,2017)]:
                    print('Invalid year')
                else: 
                    display_info_by('year',by_year)
                    if_continue=2
                    while True:
                        try:
                            if_continue = int(input('do u want to enter other year? enter 1 for home page, enter 0 for year entering section:')) 
                        except ValueError as e:
                            print('error uccured. ')

                        if if_continue == 1:
                            print('you will return to home page.')
                            user_ask = False
                            break
                        elif if_continue == 0:
                            print('you will return year entering section.')
                            break
                    
        elif user_input == 2:
            user_ask = True
            while user_ask:
                by_age = 300
                try:
                    by_age = int(input('Enter age:'))
                except ValueError:
                    print('error occured. enter integer.')
                cursor.execute('SELECT age FROM oscar')
                res = cursor.fetchall()
                
                if by_age not in [a[0] for a in res]:
                    print('age did not found.')
                else:
                    display_info_by('age',by_age)
                    if_continue = 222
                    while True:
                        try:
                            if_continue = int(input('do u want to search other age? enter 0 for yes, enter 1 for no:')) 
                        except ValueError as e:
                            print('error uccured. ')

                        if if_continue == 1:
                            print('you will return to home page.')
                            user_ask = False
                            break
                        elif if_continue == 0:
                            print('you will return to age entering section.')
                            break
                        else:
                            print('enter valid number.')
                            
        elif user_input == 3:
            first_while = True
            while first_while:
                cursor.execute('SELECT name FROM oscar')
                fetched_name = cursor.fetchall()
                by_name = input('enter name:')
                by_surname = input('enter surname:')
                fixed_fullName = fixName(by_name,by_surname)
                matched = False
                
                for x in range(len(fetched_name)):
                    if fetched_name[x][0] == fixed_fullName:
                        matched = True
                check_spell = True
                while check_spell:
                    if_continue = 2
                    if matched == False:
                        print('name not found. check your spelling.')
                          
                    elif matched == True:
                        print('name was found. see info below.')
                        cursor.execute('SELECT * FROM oscar WHERE name=:val',{'val':fixed_fullName})
                        data = cursor.fetchall()
                        for x in range(len(data)):
                            print("section{}\nyear: {}, winner's name: '{}', winner's age: {}, winner's gender: '{}', movie name: '{}'\n".format(x+1,data[x][1],data[x][3],data[x][2],data[x][4],data[x][5]))
                    
                    while True:
                        try:
                            if_continue = int(input('do u want to search name again? enter 1 for yes, enter 0 for no:')) 
                        except ValueError:
                            print('error uccured. ')

                        if if_continue == 1:
                            print('you will return to name entering section.')
                            check_spell = False
                            break
                        elif if_continue == 0:
                            print('you will return to home page')
                            check_spell = False
                            first_while = False
                            break
                        else:
                            print('enter valid number.')
        
        elif user_input == 4:
            first_loop = True 
            movie_name = ''
            ask_user = ''
            while first_loop:
                try:
                    movie_name = input('enter movie name:')
                except ValueError:
                    print('error occured. check your spelling.')
                
                cursor.execute('SELECT * FROM oscar WHERE movie=:inp',{'inp':movie_name})
                fetched_name = cursor.fetchall()
                if len(fetched_name) == 0:
                    print('movie with this name not found.')
                elif fetched_name != 0:
                    counter = 0
                    print("section{}\nyear: {}, winner's name: '{}', winner's age: {}, winner's gender: '{}', movie name: '{}'\n".format(counter+1,fetched_name[counter][1],fetched_name[counter][3],fetched_name[counter][2],fetched_name[counter][4],fetched_name[counter][5]))
                ask_user_bool = True
                while ask_user_bool:
                    try:    
                        ask_user = int(input('do you want to search again? enter 1 to go to search section. enter 0 to go to home page:'))
                    except ValueError:
                        print('error occured. pls enter valid number.')
                    
                    if ask_user == 1:
                        break
                    elif ask_user == 0:
                        first_loop = False
                        print('you will return to home page.')
                        break
                    else:
                        print('try again')
        elif user_input == 0:
            print('operation canceled. ')
            break
                    
def add_info():
    first_loop = True
    print('you entered to the information adding mode.')
    while first_loop:
        cursor.execute('SELECT id FROM oscar')
        ids = cursor.fetchall()
        last_id = ids[-1][0]
        info_id = 0
        year = 0
        winner_name,winner_surname = '',''
        winner_full_name = ''
        winner_age = 0
        gender = ''
        movie = ''
        ask = ''
        print('information inserting mode.\n')
        while True:
            try:
                info_id = int(input('enter id.'))
            except ValueError:
                print('try again.')
            if info_id == last_id + 1:
                print('id will be inserted to the table.')
                break
            else:
                print('id must be {}.'.format(last_id+1))
                
        while True:
            try:
                year = int(input('enter year'))
            except ValueError:
                pass
            if year >= 1928 and year <= 2022:
                print('year will be inserted to the table.')
                break
            else:
                print('error occured. enter valid year between 1928 and 2022.')
                
        while True:
            try:
                winner_age = int(input('enter age of a winner.'))
            except ValueError:
                print('enter integer.')
            if isinstance(winner_age,int):
                print('age will be inserted to the table.')
                break      
    
        while True:
            winner_name = input('enter name of winner.')
            winner_surname = input('enter surname of winner.')
            winner_full_name = fixName(winner_name,winner_surname)
            print('name will be inserted to the table.')
            break

        while True:
            try:
                gender = str(input('enter gender.("F" or "M")'))
            except ValueError:
                pass
            if gender.upper() == 'F' or gender.upper() == 'M':
                print('gender will be inserted to the table.')  
                break   
            else:
                print('enter F or M !')
        while True:
            movie_name = input('enter movie name.')
            print('movie name will be inserted to the table.')
            break
        cursor.execute('INSERT INTO oscar(id,year,age,name,gender,movie) VALUES(?,?,?,?,?,?)',(info_id,year,winner_age,winner_full_name,gender.upper(),movie_name.title()))
        conn.commit()
        print('information was successfully inserted to the base.\n')
        
        while True:
            try:
                ask = int(input('do you want to insert another information? for yes enter 1, for no enter 0.'))
            except ValueError:
                pass
            if ask == 1:
                print('you will be return to information inserting mode.')
                break
            elif ask == 0:
                print('you will return to home page.')
                first_loop = False
                break
            else:
                print('enter only 1 or 0! ')
                
def update_info():
    first_loop = True 
    while first_loop:
        ask_id = 0
        cursor.execute('SELECT id FROM oscar')
        ids = [a[0] for a in cursor.fetchall()]
        
        user_answr = int(input('which information you want to update(enter equal number)? (1) id. (2) year. (3) movie name. (4) update by id. (0)exit')) 
        insert_year = 0
        insert_id = 0
        #update id
        if user_answr == 1:
            #id update loop
            second_loop = True
            while second_loop:
                try:
                    ask_id = int(input('enter id.'))
                except ValueError as e:
                    print(e)
                if ask_id not in ids:
                    print('no id found. try again.')
                elif ask_id in ids:
                    while True:
                        insert_id = 0
                        try:
                            insert_id = int(input('enter id, that should be inserted into the table.'))
                        except ValueError:
                            print('invalid number.')
                        #check if inputed id is valid
                        if ask_id != ids[-1] and ask_id != ids[0] and insert_id == ids.index(ask_id-1) + 2 and insert_id == ids.index(ask_id + 1):
                            print('id will be updated.')
                            break
                        elif ask_id == ids[-1] and insert_id == ids[-2] + 1:
                            print('id will be updated.')
                            break
                        elif ask_id == ids[0] and insert_id == ids[1] - 1:
                            print('id will be updated.')
                            break
                        else:
                            print('first {}, second {}\n'.format(ids.index(ask_id-1),ids.index(ask_id + 1)))
                            print('enter valid id. that id can not be inserted.')
                    break
        #update year
        #anu aq roca siashi 2021 weli weria 3jer , 3ves chaanacvlebs axali wlit, romelsac iuzeri shemoikvans.
        if user_answr == 2:
            ask_usr = 0
            cursor.execute('SELECT year FROM oscar')
            years = [a[0] for a in cursor.fetchall()]
            year_first_loop = True
            while year_first_loop:
                try:
                    ask_user = int(input('enter year you want to be updated.'))
                except ValueError:
                    pass
                if ask_user in years:
                    insert_year = 0
                    while True:
                        try:
                            insert_year = int(input('enter year that you want to be placed.'))
                        except ValueError:
                            pass
                        if insert_year not in range(1928,2023):
                            print('enter valid year. ')
                        else:
                            print('year will be updated. ')
                            year_first_loop = False
                            break
                        
                else:
                    print('enter valid year.') 
        #update movie name
        if user_answr == 6:
            ask_usr = ''
            cursor.execute('SELECT movie FROM oscar')
            movie_data = [a[0] for a in cursor.fetchall()]
            movie_loop = True
            while movie_loop:
                ask_usr = input('enter movie name that you want to update.')
                if ask_usr in movie_data:
                    insert_movie = input('enter movie name that will be placed.')
                    cursor.execute('UPDATE oscar SET movie =? WHERE movie = ?',(insert_movie,ask_usr))
                    conn.commit()
                    print('movie name updated successfully\nreturned to home page.')
                    break
                    #cursor.execute('UPDATE oscar SET movie=? WHERE movie=? ',(insert_movie)) 
                else:
                    print('movie not found. try again.')           
                    
        elif user_answr == 4:
            print('update information by id.')
            user_inpt = 0
            second_while_loop = True
            ask_user,ask_user_loop = '',True
            while True:
                while second_while_loop:
                    try:
                        user_inpt = int(input('enter id of row.'))
                    except ValueError:
                        pass
                    cursor.execute('SELECT id FROM oscar')
                    if user_inpt not in [a[0] for a in cursor.fetchall()]:
                        print('id not found. try again.')
                    else:
                        second_while_loop = False
                
                while ask_user_loop:
                    try:
                        ask_user = int(input('(1)update year, (2)update age, (3)update gender,(4)update name of the winner, (0)exit'))   
                    except ValueError:
                        pass
                    if ask_user == 1:
                        cursor.execute("UPDATE oscar SET year=? WHERE id=?",(input('enter new year.'),user_inpt))
                        conn.commit()
                        print('information updated successfully.')
                        break
                    if ask_user == 2:
                        cursor.execute("UPDATE oscar SET age=? WHERE id=?",(input('enter new age for winner.'),user_inpt))
                        conn.commit()
                        print('information updated successfully.')
                        break
                    if ask_user == 3:
                        cursor.execute("UPDATE oscar SET age=? WHERE id=?",(input('enter new age for winner.'),user_inpt))
                        conn.commit()
                        print('information updated successfully.')
                        break
                    if ask_user == 4:
                        cursor.execute('UPDATE oscar SET name=? WHERE id=?',(input('enter new name for winner.'),user_inpt))
                        conn.commit()
                        print('information updated successfully')
                    elif ask_user == 0:
                        print('operation canceled.')
                        break

def make_plot():
    #makes plot that show parcentage of how many people was less than 50 years old and more than 50 years old when they hade become oscar's winner
     
    labels = 'less than 50years old', 'more than 50years old'
    cursor.execute('SELECT age FROM oscar')
    ages = cursor.fetchall()
    lt_50 = [a[0] for a in ages if a[0] <= 50]
    mt_50 = [a[0] for a in ages if a[0] > 50]
    lt_prcntg = round(100*len(lt_50)/len(ages),2)
    mt_prcntg = round(100-lt_prcntg)
    sizes = [lt_prcntg,mt_prcntg]
    
    #explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels,shadow=True,autopct='%1.1f%%',)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    #plt.savefig('oscar_age.png')
    plt.show()
    
def main():
    inpt = 0
    while True:
        try:
            inpt = int(input('(1) display info. (2) add info. (3) update info. (4) show plot. (0)exit: '))
        except ValueError:
            pass
        if inpt == 1:
            display_info()
        elif inpt == 2:
            add_info()
        elif inpt == 3:
            update_info()
        elif inpt == 4:
            make_plot()
        elif inpt == 0:
            break
        else:
            print('enter equal number please.')
    conn.close()

if __name__ == "__main__":
    main()