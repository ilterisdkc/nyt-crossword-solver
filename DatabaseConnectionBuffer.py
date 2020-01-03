# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 22:26:08 2020

@author: ilteriscivelek
"""

import pickle 
 
class PuzzleSerializationHandler() :       
    file_name = "Crossword_Puzzle_Database.spo" 
    def __init__(self, file_name) :        
        self.file_name = file_name        
        self.load_puzzle = [] 
 
    def dumpPuzzleSerialized(self) :         
        write_file = open(self.file_name, 'wb')         
        for i in range(0, len(self.load_puzzle)) :             
            pickle.dump(self.load_puzzle[i], write_file)         
            write_file.close()       
    def loadSerializedPuzzle(self) :         
        read_file = open(self.file_name, 'rb')         
        print("Loading previous puzzle objects from database...")         
        while True :             
            try :                 
                self.load_puzzle.append(pickle.load(read_file))             
            except :                 
                break         
            print("All puzzles loaded")         
            read_file.close() 