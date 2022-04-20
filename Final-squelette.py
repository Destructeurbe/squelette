# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 13:53:25 2022

@author: Bastien
Jerome support
"""



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

        return self.life > 0

    def get_hit(self, damages):
        self.life -= damages
        return self.life

    def __str__(self):
        return f"{self.name}: {self.life} pv et {self.money}" + u"\u20AC"

    def new_character(self):                                                                            #fait pop un nouveau caractére 

        line = input(f"{self.name}: Wich line would you place the new one (0-{self.game.nb_lines-1}) ? (enter if none) ")
        if line != "":
            line = int(line)
            if 0<=line<=self.game.nb_lines-1 :
                if self.money >= Character.base_price :
                    column = 0 if self.direction == +1 else self.game.nb_columns-1
                    Character(self,(line,column))


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
        return self.players[self.player_turn % len(self.players)]

    @property
    def oponent(self):
        return self.players[self.player_turn % len(self.players)-1]

    @property
    def all_characters(self):
        list_character = []
        for player in self.players:
            list_character += player.team
        return list_character


    def get_character_at(self, position):
        for character in self.all_characters:
            if character.position == position :
                return character

        return None

    def place_character(self, character, position):

        if 0 <= position[0] < self.nb_lines and 0 <= position[1] < self.nb_columns and self.get_character_at(position) == None:
            character.position = position
            return True
        return False

    def draw(self):

        print(f"{self.players[0].life:<4}{'  '*self.nb_columns}{self.players[1].life:>4}")

        print("----"+self.nb_columns*"--"+"----")

        for line in range(self.nb_lines):
            print(f"|{line:>2}|", end="")
            for col in range(self.nb_columns):
                if self.get_character_at((line,col)) == None :
                    print (".", end=" ")
                else :
                    
                    print (self.get_character_at((line,col)).design, end=" ") 
                    
                
            print(f"|{line:<2}|")

        print("----"+self.nb_columns*"--"+"----")

        print(f"{self.players[0].money:<3}${'  '*self.nb_columns}${self.players[1].money:>3}")
        



    def play_turn(self):
        self.current_player.new_character ()
        for character in self.current_player.team:
            character.play_turn()
        
        for character in self.oponent.team :
            character.play_turn ()
            
        self.draw()

    def play(self):
        
        while self.current_player.is_alive == True :                  #attribus dérivable  = pas de ()
            self.play_turn()
            self.player_turn += 1







### PERSONNAGES ###
class Character :

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
        # TODO
        return self.player.direction

    @property
    def game(self):
        # TODO
        return self.player.game

    @property
    def enemy(self):

        number_joueur = 0
        if self.direction == 1:
            number_joueur = -1
        return self.game.players[number_joueur]

    @property
    def design(self):
        if self.player.direction >= 1 :
            design = ">"
        else :
            design = "<"
        return design
    @property
    def pos_front (self):
        return (self.position[0],self.position[1] + self.direction)

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
        

    


    



if __name__ == "__main__" :
    joueurs1 = Player("Michel", 10, 15)
    joueurs2 = Player("Jack",10,15)
    Tournoi = Game(joueurs1, joueurs2)
    Tournoi.play ()


    