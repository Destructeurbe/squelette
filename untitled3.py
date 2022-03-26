# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 16:32:36 2022

@author: Bastien
"""
class Player :
    def __init__ (self,name, life, money) :
        
        self.name = name    #le nom du joueur
        self.life = life    #point de vie
        self.money = money  #argent
        #exemple : human = Player("richar",5,3) 
        
        self.team =[]
        self.game = None
        self.direction = None
        
    @property #propriété
    
    def is_alive (self) :  #def qui permet de savoir si le perso est en vie
        return self.life > 0 #un True (supérieur a 1) or False (infér a 0 ou =0)
    
    
    def get_hit (self, damages) : #retire la vie du personnage
        if (damagees > 0) : #on verifie si les degats sont supérieurs a 0
            self.life -= damages # on retire les dégats de ça vie
        
        return self.life  #on retourne les points de vie du personnag
    
    def __str__(self):
        return f"{self.name}: {self.pv} pv et {self.money}" + u"\u20AC"
    
    def new_character(self):
    
        line = input(f"{self.name}: Wich line would you place the new one (0-{self.game.nb_lines-1}) ? (enter if none) ")
        if line != "":
            line = int(line)
            if 0<=line<=self.game.nb_lines-1 : 
                if self.money >= Character.base_price : # on verifie si la monaie est suffisante
                    column = 0 if self.direction == +1 else self.game.nb_columns-1 # si le joueur est en +1 le personnage çe dirigera en +1 et l'autre en -1
                    Character(self,(line,column)) #affiche ou est le personnage 

if __name__ == "__main__" :
    Human = Player ("richard",4,2) #test des 3 para en class player
    
    print (Human.__dict__) #affiche tout çe qui est dans le def __init__
    
    print(Human.is_alive) #test la fonction is_alive
    
    
    