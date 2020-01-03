# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 22:31:03 2020

@author: ilteriscivelek
"""

from CrosswordPuzzle import Puzzle 
from html.parser import HTMLParser 
from selenium import webdriver 
 
temp_puzzle = None 
extracted_text_inorder = [] 
extracted_span_numbertag_inorder = [] 
extracted_span_clues = [] 
 
def insertExtractedCluesIntoPuzzle(extracted_span_clues) :     
    if len(extracted_span_clues) == 2 * Puzzle.MAX_LENGTH :         
        for i in range(0, Puzzle.MAX_LENGTH) :             
            temp_puzzle.insertClueAcross(extracted_span_clues[i])             
            print("The clue inserted into puzzle : " + extracted_span_clues[i])             
            temp_puzzle.insertClueDown(extracted_span_clues[i + Puzzle.MAX_LENGTH])             
            print("The clue inserted into puzzle : " +  extracted_span_clues[i + Puzzle.MAX_LENGTH])         
            return True     
        else :         
            return False 
 
def deleteNumbersOnExtractedText(extracted_text_inorder) :     
    currIndex = 0     
    while currIndex < len(extracted_text_inorder) :         
        try : 
            int(extracted_text_inorder[currIndex])             
            del extracted_text_inorder[currIndex]         
        except :             
            currIndex += 1 
 
def insertExtractedTextIntoPuzzle(extracted_text_inorder, temp_puzzle) :     
    del extracted_text_inorder[-1]     
    deleteNumbersOnExtractedText(extracted_text_inorder)     
    print(extracted_text_inorder)     
    extracted_answer = ""     
    for currAnswer in range(0, len(extracted_text_inorder), Puzzle.MAX_LENGTH) :         
        for currIndex in range(currAnswer, currAnswer + Puzzle.MAX_LENGTH) :             
            if not extracted_text_inorder[currIndex] == "$" :                 
                extracted_answer += extracted_text_inorder[currIndex]         
        temp_puzzle.insertAnswerAcross(extracted_answer)         
        print("The Answer inserted into puzzle : " + extracted_answer)         
        extracted_answer = "" 
 
    answers_down = []     
    for currAnswer in range(0, Puzzle.MAX_LENGTH) :         
        for currIndex in range(currAnswer, len(extracted_text_inorder), Puzzle.MAX_LENGTH) :             
            if not extracted_text_inorder[currIndex] == "$" :                 
                extracted_answer += extracted_text_inorder[currIndex]         
        answers_down.append(extracted_answer)         
        extracted_answer = "" 
 
    inserted = []     
    for i in range(0, Puzzle.MAX_LENGTH) :         
        inserted.append(False)     
    remainder = Puzzle.MAX_LENGTH     
    for currIndex in range(0, len(extracted_text_inorder)) :         
        if not extracted_text_inorder[currIndex] == "$" :             
            if not inserted[currIndex % Puzzle.MAX_LENGTH] :                 
                temp_puzzle.insertAnswerDown(answers_down[currIndex % Puzzle.MAX_LENGTH])                 
                inserted[currIndex % Puzzle.MAX_LENGTH] = True                 
                print("The Answer inserted into puzzle : " + answers_down[currIndex % Puzzle.MAX_LENGTH])                 
                remainder -= 1                 
                if remainder == 0 :                     
                    break 
 
    class NYT_HTMLHandler(HTMLParser) : 
     
        def __init__(self):         
            super().__init__()         
            self.extract_date = False         
            self.extract_span = False         
            self.g_open = False         
            self.g_extract = False         
            self.black_square = False         
            self.extract_text = False         
            self.span_order = 0         
            self.clue_order = 0       
        
        ##These methods are hard-coded to implement data extraction for NYT_Crossword_Puzzle     
        def handle_starttag(self, tag, attrs) :         
            if tag == "span" :             
                if self.span_order == 2 :   #Date_Extraction Case 
                    self.extract_date = True                 
                    self.extract_span = True             
                elif self.span_order > 3 :  #Clue_Extraction Cases                 
                    self.extract_span = True             
                self.span_order += 1 
 
            if tag == "g" :                 #Tag identifier for Answers and Black Squares             
                self.g_open = True         
                if self.g_open and tag == "rect" :             
                    self.g_extract = True             
                    self.black_square = True         
                if tag == "text" :              #Answer_Extraction Cases             
                    self.extract_text = True       
        ##These methods are hard-coded to implement data extraction for NYT_Crossword_Puzzle     
        def handle_data(self, data) :         
            if self.extract_date :             
                if not self.extract_span :                 
                    print("The date_data extracted : " + data)                 
                    space_index = data.find(' ')                 
                    comma_index = data.find(',')                 
                    temp_puzzle.arrangeDateProperty(data[comma_index + 2 :], data[0 : space_index], 
data[space_index + 1 : comma_index])                 
                    self.extract_date = False             
                self.extract_span = False 
 
            if self.extract_span :             
                print("The span_data extracted : " + data)             
                if self.span_order % 2 == 1 :                 
                    extracted_span_numbertag_inorder.append(data)             
                else :                 
                    extracted_span_clues.append(data) 
     
            if self.g_extract :             
                if self.extract_text :  #Not Black Square                 
                    print("The text_data extracted : " + data)                 
                    extracted_text_inorder.append(data)                 
                    self.black_square = False         
        ##These methods are hard-coded to implement data extraction for NYT_Crossword_Puzzle     
        def handle_endtag(self, tag) :         
            if tag == "span" :             
                self.extract_span = False         
            if tag == "g" :             
                self.g_open = False             
                if self.g_extract and self.black_square :                 
                    extracted_text_inorder.append("$")             
                self.g_extract = False         
            if tag == "text" :             
                self.extract_text = False 
 
class PuzzleDataBuffer : 
 
    html_handler = NYT_HTMLHandler()     
    url_address = "https://www.nytimes.com/crosswords/game/mini"       
    
    def constructBufferedData() : #Not to call over the object but the class; static method 
        global temp_puzzle         
        driver = webdriver.Chrome()         
        try :            
            print("Connecting to server to extract daily puzzle...")             
            driver.get(PuzzleDataBuffer.url_address)             
            print("Connected to server")             
            driver.maximize_window()             
            driver.find_element_by_class_name("buttons-modalButtonContainer--35RTh").click()             
            driver.find_elements_by_tag_name("button")[5].click()             
            driver.find_elements_by_class_name("HelpMenu-item--1xl0_")[6].click()             
            driver.find_elements_by_class_name("buttons-modalButton--1REsR")[1].click()             
            driver.find_element_by_class_name("ModalBody-closeX--2Fmp7").click() 
 
            print("Extracting the puzzle data...")             
            temp_puzzle = Puzzle()             
            PuzzleDataBuffer.html_handler.feed(str(driver.page_source))             
            print("Puzzle data extracted")             
            print("Disconnected from server")             
            driver.quit()             
            print("Puzzle is being constructed...") 
 
            if insertExtractedCluesIntoPuzzle(extracted_span_clues) :                 
                insertExtractedTextIntoPuzzle(extracted_text_inorder, temp_puzzle)                 
                print("Puzzle constructed:")                 
                temp_puzzle.printPuzzle()                 
                return True             
            else :                 
                temp_puzzle = None                 
                print("The puzzle extracted from NYT Crossword Puzzle Mini is not in the compatible format")                 
                return False         
        except :             
            driver.quit()             
            temp_puzzle = None             
            print("A webdriver error occured!!!")             
            return False  
 