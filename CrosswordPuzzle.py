# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 21:45:45 2020

@author: ilteriscivelek
"""

import datetime 
class Clue : 
    def __init__(self, text) :         
        self.text = text 
class Answer : 
    def __init__(self, wordAnswer) :         
        self.wordAnswer = wordAnswer 
    def __len__(self) :         
        return len(self.wordAnswer) 
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"] 

class Puzzle : 

    MAX_LENGTH = 5 
 
    def __init__(self, *args, **kwargs) :         
        super().__init__(*args, **kwargs)         
        self.cluesAcross = []         
        self.cluesDown = []         
        self.answersAcross = []         
        self.answersDown = []         
        self.date = datetime.date(1900, 1, 1) 
    
    def setClueAcross(self, index, alternate_clue) :         
        insert = Clue(alternate_clue)         
        if index < Puzzle.MAX_LENGTH and index > -1:             
            self.cluesAcross[index] = insert 
 
    def setClueDown(self, index, alternate_clue) :         
        insert = Clue(alternate_clue)         
        if index < Puzzle.MAX_LENGTH and index > -1:             
            self.cluesDown[index] = insert 
 
    def insertClueAcross(self, clue) :         
        insert = Clue(clue)         
        if len(self.cluesAcross) < Puzzle.MAX_LENGTH :             
            self.cluesAcross.append(insert)
            return True 
        else:
            return False 
        
    def insertClueDown(self, clue) :         
        insert = Clue(clue)         
        if len(self.cluesDown) < Puzzle.MAX_LENGTH :             
            self.cluesDown.append(insert)             
            return True         
        else :             
            return False 
 
    def insertAnswerAcross(self, wordAnswer) :         
        insert = Answer(wordAnswer)         
        if len(self.answersAcross) < Puzzle.MAX_LENGTH :             
            self.answersAcross.append(insert)             
            return True         
        else :             
            return False 
 
    def insertAnswerDown(self, wordAnswer) :         
        insert = Answer(wordAnswer)         
        if len(self.answersDown) < Puzzle.MAX_LENGTH :             
            self.answersDown.append(insert)             
            return True         
        else :             
            return False
        
    def arrangeDateProperty(self, year, month, day) :         
        month_number = 0         
        for count, item in enumerate(MONTHS) :             
            if item.lower() == month.lower() :                 
                month_number = count + 1                 
                break         
            try :             
                self.date = self.date.replace(year=int(year), month=month_number, day=int(day))         
            except :             
                print("Invalid Date Input!!!") 
 
    def printPuzzle(self) :         
        print("The Puzzle with the date " + str(self.date))         
        for i in range(0, len(self.cluesAcross)) :             
            print(self.cluesAcross[i].text + " : " + self.answersAcross[i].wordAnswer)         
        for i in range(0, len(self.cluesDown)) :             
            print(self.cluesDown[i].text + " : " + self.answersDown[i].wordAnswer) 
 
    def isSameDate(self, other_puzzle) :         
        return self.date == other_puzzle.date 
 
    def copy(self) :         
        copy = Puzzle()         
        copy.date = self.date         
        for i in range(0, Puzzle.MAX_LENGTH) :             
            copy.answersAcross.append(Answer(self.answersAcross[i].wordAnswer))             
            copy.answersDown.append(Answer(self.answersDown[i].wordAnswer))             
            copy.cluesAcross.append(Clue(self.cluesAcross[i].text))             
            copy.cluesDown.append(Clue(self.cluesDown[i].text))         
        return copy