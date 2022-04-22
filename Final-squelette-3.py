# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 13:53:25 2022

@author: Bastien
Jerome support
"""

AVAILABLE_CHARACTERS = {}                                                       #création d'une liste vide ou mettre plusieurs type de character

class Player :

    def __init__(self, name, life, money):
        self.name = name
        self.life = life
        self.money = money
        self.team = [ ]
        self.game = None
        self.direction = None

    @property
    def is_alive(self):

        return self.life > 0                                                    #retourne un true si la vie d'un personnage est supérieur a zéro (false si non)

    def get_hit(self, damages):
        self.life -= damages
        return self.life

    def __str__(self):
        return f"{self.name}: {self.life} pv et {self.money}" + u"\u20AC"

    def new_character(self):                                                    #Nouveau "sbires"
        for key,val in AVAILABLE_CHARACTERS.items() :
            print ("-",key,"->",val)
        character_chose = input (f"{self.name} : choisis un sbires !")
        
        line = input(f"{self.name}: Wich line would you place the new one (0-{self.game.nb_lines-1}) ? (enter if none) ")
        
        if line != "":
            line = int(line)
            if 0<=line<=self.game.nb_lines-1 :
                if self.money >= Character.base_price :
                    column = 0 if self.direction == +1 else self.game.nb_columns-1
                    if character_chose == "C" :
                        Character(self,(line,column))
                    elif character_chose == "F" : 
                        Fighter(self,(line,column))
                    elif character_chose == "T" : 
                        Tank(self,(line,column))
                        
                    
                    


class Game :

    def __init__(self,player0, player1, nb_lines=6,nb_columns=15):

        if player1 == None or player0 == None or player0 == player1:
            raise ValueError ("Il faut 2 joueurs différents")
        self.players = [player0, player1]
        self.nb_lines = nb_lines
        self.nb_columns = nb_columns
        self.player_turn = 0
        player1.game = self
        player0.game = self
        player0.direction = 1
        player1.direction = -1
    @property
    def current_player(self):
        return self.players[self.player_turn % len(self.players)]               #le len transforme la liste en nombre (le player1 devient 1 et player 2 devient 2)

    @property
    def oponent(self):
        return self.players[self.player_turn % len(self.players)-1]             #on retire -1

    @property
    def all_characters(self):
        list_character = []
        for player in self.players:
            list_character += player.team
        return list_character


    def get_character_at(self, position):                                        #mets le sbires a une position donné 
        for character in self.all_characters:
            if character.position == position :
                return character

        return None

    def place_character(self, character, position):

        if 0 <= position[0] < self.nb_lines and 0 <= position[1] < self.nb_columns and self.get_character_at(position) == None:
            character.position = position
            return True
        return False

    def draw(self):                         #dessine le plateau 

        print(f"{self.players[0].life:<4}{'  '*self.nb_columns}{self.players[1].life:>4}")

        print("----"+self.nb_columns*"--"+"----")

        for line in range(self.nb_lines):
            print(f"|{line:>2}|", end="")
            for col in range(self.nb_columns):
                if self.get_character_at((line,col)) == None :                  #mets le sbires a un 
                    print (".", end=" ")
                else :
                    
                    print (self.get_character_at((line,col)).design, end=" ") 
                    
                
            print(f"|{line:<2}|")

        print("----"+self.nb_columns*"--"+"----")

        print(f"{self.players[0].money:<3}${'  '*self.nb_columns}${self.players[1].money:>3}")
        



    def play_turn(self):                                                        #la commande fait avancé tout les "sbires" de tout les les joeurs et les dessines via draw
        self.current_player.new_character ()
        for character in self.current_player.team:
            character.play_turn()                                               #fait avancé les "sbires" d'une case (sbires du joeurs qui joue)
        
        for character in self.oponent.team :                                    #fait avancé les "sbires" du joeurs ennemis 
            character.play_turn ()
            
        self.draw()                                                             #dessine le tableau;place les sbires,demande de placer les sbires 

    def play(self):
        
        while self.current_player.is_alive == True :                            #attribus dérivable  = pas de ()
            self.play_turn()
            self.player_turn += 1                                               #ajoute 1 a player_turn







### PERSONNAGES ###
class Character () :                                                            #class mére

    base_price = 1
    base_life = 5
    base_strength = 1


    def __init__(self, player, position):

        self.player = player
        self.life = self.base_life
        self.strength = self.base_strength
        self.price = self.base_price

        ok = self.game.place_character(self, position)
        if ok :
            self.player.team.append(self)
            self.player.money -= self.price


    @property
    def direction(self):
        return self.player.direction

    @property
    def game(self):
        return self.player.game

    @property
    def enemy(self):

        number_joueur = 0
        if self.direction == 1:
            number_joueur = -1
        return self.game.players[number_joueur]

    @property
    def design(self):                                                           #designe le dessin du sbires
        if self.player.direction >= 1 :
            design = ">"                                                        #sbires adjuvant
        else :
            design = "<"                                                        #sbires oposants 
        return design
    @property
    def pos_front (self):
        return (self.position[0],self.position[1] + self.direction)             #definis la position des "sbires"

    def move(self):
        self.game.place_character(self,self.pos_front)


    def get_hit(self, damages):

        self.life -= damages
        if self.life <= 0:
            self.player.team.remove(self)           
            return self.price/2
        return 0

    def attack(self):


        if self.position[1] == 0 and self.direction == -1 or self.position[1] == self.game.nb_columns - 1 and self.direction == 1:
            self.enemy.get_hit(self.strength)
        else:
            personnage = self.game.get_character_at(self.pos_front)
            if personnage != None:
                self.player.money += personnage.get_hit(self.strength)


    def play_turn(self):
        
        self.move()
        self.attack()
    def __str__(self):
        return "Personnage",self.base_price,"vie : ",self.base_life,"force :",self.base_strength 
  
class Fighter (Character):                                                      #class Fighter

    base_price = 2
    base_strength = 2
    @property
    def design(self):                                                           #dessin du sbires "Fighter"
        if self.player.direction >= 1 :
            design = "("                                                        #sbires adjuvant
        else :
            design = ")"                                                        #sbires oposants 
        return design
class Tank (Character) :                                                        #class Tank

    base_price = 3
    base_life = 10
    def __init__(self,player,position): 
        self.turn_to_move = False
        super().__init__(player,position)                                       #Récupération de l'init de la classe mére
        
    @property 
    def design(self):                                                           #dessin du sbires "Tank"
        if self.player.direction >= 1 :
            design = "{"                                                        #sbires adjuvant
        else :
            design = "}"                                                        #sbires oposants 
        return design
    def move (self): 
        if self.turn_to_move == True :
            super().move()
            self.turn_to_move = False
        else :
            self.turn_to_move = True 
AVAILABLE_CHARACTERS ["T"] = Tank                                               #on rajoute Tank a la liste des "sbires" et "T" = Tank
AVAILABLE_CHARACTERS ["F"] = Fighter                                            #On rajoute Fighter a la liste des "sbires" et "F" = Fighter
AVAILABLE_CHARACTERS ["C"] = Character                                          #On rajoute Fighter a la liste des "sbires" et "C" = Fighter  
        

    


    



if __name__ == "__main__" :
  
    joueurs1 = Player("Michel", 10, 15)
    joueurs2 = Player("Jack",10,15)
    
    Tournoi = Game(joueurs1, joueurs2)
    Tournoi.play ()

