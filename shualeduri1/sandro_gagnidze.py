class Health:
    def __init__(self,age,gender,pulse):
        self.age = age
        self.gender = gender
        self.pulse = pulse 
    
    def __str__(self):
        return 'თქვენი ასაკია: {}. თქვენი სქესია: {}. თქვენი გულისცემა წუთში: {}/n'.format(self.age,self.gender,self.pulse)   
        
    def avg_life(self):
        self.used_impulse = self.age * 365 * 24 * 60 * self.pulse  
        self.left_impulse = 10**8*26 - self.used_impulse
        self.left_life = self.left_impulse/self.pulse/60/24/365
        
        return 'თქვენი სიცოცხლის საშუალო ხანგრძლივობაა: {} წელი\n'.format(self.left_life + self.age)
        
    def max_pulse(self):
        if self.gender == 'მამრობითი':
            return 'თქვენი მაქსიმალური გულისცემის რაოდენობაა {}\n'.format( 226-0.9*self.age) 
        
        elif self.gender == 'მდედრობითი':
            return 'თქვენი მაქსიმალური გულისცემის რაოდენობაა {}\n'.format(223-0.9*self.age) 
    
    def max_beat(self,factor):
        self.factor = factor      
        return 'თქვენი მაქსიმალური გულისცემა წუთში {}'.format((226-0.9*self.age-60)*self.factor + 60)
             
        
person1 = Health(20,'მამრობითი',70)
print(person1) 
print(person1.avg_life())
print(person1.max_pulse())
print(person1.max_beat(0.8))