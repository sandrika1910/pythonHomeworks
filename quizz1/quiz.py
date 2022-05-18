class Ticket:
    
    def __init__(self,movie_name,price,tkt_amm,language="Geo"):
        self.movie_name = movie_name
        self.price = float(price)
        self.tkt_amm = tkt_amm
        self.language = language

    def __str__(self):
        return 'ფილმის დასახელება: {}\nენა: {}\nბილეთის ფასი: GEL{}\nდარჩენილი ბილეთების ოდენობა: {}\n'.format(self.movie_name,self.language,self.price,self.tkt_amm)
    
    def __gt__(self,other_obj):
        if isinstance(other_obj,Ticket):
            if self.tkt_amm > other_obj.tkt_amm:
                print('ფილმ "{}"–ზე დარჩენილი ბილეთების ოდენობა მეტია ფილმ "{}"–ზე დარჩენილი ბილეთების ოდენობაზე {}-ით\n'.format(self.movie_name,other_obj.movie_name,self.tkt_amm-other_obj.tkt_amm))
                return True 
            
            else:
                return False
            
        else:
            if self.tkt_amm > other_obj:
                print('ფილმ "{}"–ზე დარჩენილი ბილეთების ოდენობა მეტია {}–ზე\n'.format(self.movie_name,other_obj))
                return True
            
            else:
                return False
                
    def __eq__(self,other_obj):
        if isinstance(other_obj,Ticket):
            if self.tkt_amm == other_obj.tkt_amm:
                print('ფილმ "{}"–ზე დარჩენილი ბილეთების ოდენობა ტოლია ფილმ "{}"–ზე დარჩენილი ბილეთების ოდენობის\n'.format(self.movie_name,other_obj.movie_name))
                return True 
            
            else:
                return False
            
        else:
            if self.tkt_amm == other_obj:
                print('ფილმ "{}"–ზე დარჩენილი ბილეთების ოდენობა ტოლია {}-ის\n'.format(self.movie_name,other_obj))
                return True 
            
            else:
                return False
            
    def __lt__(self,other_obj):
        if isinstance(other_obj,Ticket):
            if self.tkt_amm < other_obj.tkt_amm:
                print('ფილმ "{}"–ზე დარჩენილი ბილეთების ოდენობა ნაკლებია ფილმ "{}"–ზე დარჩენილი ბილეთების ოდენობის\n'.format(self.movie_name,other_obj.movie_name))
                return True 
            
            else:
                return False
        else:
            if self.tkt_amm < other_obj:
                print('ფილმ "{}"–ზე დარჩენილი ბილეთების ოდენობა ნაკლებია {}–ის\n'.format(self.movie_name,other_obj))
                return True
            
            else:
                return False
class User:
    
    def __init__(self,buyer_name,balance):
        self.buyer_name = buyer_name
        self.balance = balance 
        self.balance = float(self.balance)
         
    def __str__(self):
        return 'მომხმარებლის სახელია: {}, თქვენს ანგარიშზე არსებული თანხა: {}{}\n'.format(self.buyer_name,'GEL',self.balance)
    
    def buy_ticket(self,tkt_class,ammountOfTickets):
        self.tkt_class = tkt_class
        self.tkt_amm = ammountOfTickets
        self.tkt_amm_on_acc = 0
        
        while True:
            self.user_input = int(input('\nშეიყვანეთ რიცხვი: 1) ბილეთ(ებ)ის ყიდვა 2) გამოსვლა '))
            
            if self.user_input == 1:
                if self.tkt_class.tkt_amm < self.tkt_amm:
                    print('\nარასაკმარისი ბილეთების რაოდენობა! \nდარჩენილია {} ბილეთი\n'.format(self.tkt_class.tkt_amm))
                
                elif self.tkt_class.price * self.tkt_amm > self.balance:
                    print('\nთქვენ არ გაქვთ ბალანსზე საკმარისი თანხა \nბილეთების შესაძენად საჭირო თანხა: GEL{} \nხელმისაწვდომი ბალანსი: GEL{}\n'.format(self.tkt_class.price * self.tkt_amm,self.balance))
                
                elif self.tkt_class.price * self.tkt_amm <= self.balance and self.tkt_amm <= self.tkt_class.tkt_amm:
                    self.balance -= self.tkt_class.price * self.tkt_amm
                    self.tkt_class.tkt_amm -= self.tkt_amm
                    self.tkt_amm_on_acc += self.tkt_amm
                    print('\nთქვენ შეისყიდეთ {} ბილეთი ფილმზე "{}" , ანგარიშზე ხელმისაწვდომი თანხის ოდენობაა GEL{}\n'.format(self.tkt_amm,self.tkt_class.movie_name,self.balance))
            
            if self.user_input == 2:
                print('თქვენ გახვედით სისტემიდან.\n')
                break
            
        if self.tkt_amm_on_acc != 0:    
            print('თქვენ ანგარიშზე გაქვთ ფილმ "{}"–ის {} ბილეთი\n'.format(self.tkt_class.movie_name,self.tkt_amm_on_acc))
        else:
            print('თქვენ არ შეგიძენიათ ბილეთი ფილმზე.\n')
            
    def deposit(self,dep):
        self.dep = dep
        self.dep = float(self.dep)
        self.balance += self.dep 
        print('ოპერაცია განხორციელდა წარმატებით, თქვენ ანგარიშზე შეიტანეთ GEL{}\n'.format(self.dep))       
        
t1 = Ticket('the notebook', 20, 4)
t2 = Ticket('Avangers ',40,47)        
u = User('Sandro', 300)
u.buy_ticket(t1,1)
#u.deposit(330)
#t1>5
#print(t1==t2)
#print(u,t1,t2)
