# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 22:54:58 2020

@author: ilteriscivelek
"""

from nltk.corpus import wordnet 
from nltk import word_tokenize 
from nltk import PorterStemmer 
import nltk 
import math 
import requests 
import urllib.request 
import time 
from bs4 import BeautifulSoup 
 
ps = PorterStemmer() 
 
focus_word = None 
alternate_string = None 
focus_word_synsets = None 
alternative_list = None 
focus_word_definition = None 
focus_word_synonm = None 
focus_word_antonym = None 
wiki_alternative = None 
most_relative_example = None 
transformed_alternate_string = None 
 
def setFocusWord(answer, clue) :     
    global focus_word, alternate_string, focus_word_synsets, focus_word_definition, focus_word_synonm     
    global focus_word_antonym, wiki_alternative, most_relative_example, transformed_alternate_string     
    focus_word = answer     
    alternate_string = clue     
    focus_word_synsets = wordnet.synsets(focus_word)     
    focus_word_definition = None     
    focus_word_synonm = None     
    focus_word_antonym = None     
    wiki_alternative = None     
    most_relative_example = None     
    transformed_alternate_string = None 
 
def constructDefinitionAlternative() :     
    global focus_word_synsets, focus_word_definition     
    print("Constructing wordnet-definition alternative...")     
    if len(focus_word_synsets) > 0 :         
        focus_word_definition = focus_word_synsets[0].definition()         
        print("Constructed wordnet-definition alternative: " + focus_word_definition)     
    else :         
        print("Not Constructed wordnet-definition alternative since any found") 
 
def constructSynonmAntonymAlternative() :     
    global focus_word_synsets, focus_word_synonm, focus_word_antonym     
    synonm_found = False     
    anonym_found = False     
    print("Constructing wordnet-synonm&antonym alternative...")     
    for synset in focus_word_synsets :         
        lemmas = synset.lemmas()         
        if not synonm_found and len(lemmas) > 0 :             
            focus_word_synonm = lemmas[0].name()             
            print("Constructed wordnet-synonm alternative: " + focus_word_synonm)             
            synonm_found = True         
        for lemma in lemmas :             
            lemma_antonyms = lemma.antonyms()             
            if len(lemma_antonyms) > 0 :                 
                focus_word_antonym = lemma_antonyms[0].name()                 
                print("Constructed wordnet-antonym alternative: " + focus_word_antonym)                 
                anonym_found = True                 
                break         
        if anonym_found :             
            break     
        if not synonm_found :         
            print("Not Constructed wordnet-synonm alternative since any found")     
        if not anonym_found :         
            print("Not Constructed wordnet-antonym alternative since any found")   
 
def constructWikiAlternative() :     
    global focus_word, wiki_alternative     
    url = "https://en.wikipedia.org/wiki/" + focus_word;     
    response = requests.get(url) 
    soup = BeautifulSoup(response.text, features="html.parser") 
 
    print("Constructing wiki alternative...")     
    if(soup.find("div",attrs={"class":"mw-parser-output"}) != None) :         
        if(soup.find("p").text.lower().find("refer to") == -1) :             
            offset = len(soup.findAll("p", attrs={"class":"mw-empty-elt"}))             
            sentence = soup.findAll('p')[offset:offset+1];         
        else :             
            offset = 0             
            if soup.find("div",attrs={"class":"toc"}) != None :                 
                offset = len(soup.find("div",attrs={"class":"toc"}).findAll("ul"))             
            sentence = soup.findAll("ul")[offset].find("li")             
            if sentence.find("ul") != None :                
                sentence = sentence.find("ul").find("li") 
 
        sentence = ''.join(map(str, sentence))         
        sentence = BeautifulSoup(sentence, features="html.parser").text         
        sentence = sentence.partition('.')[0] + '.'         
        if(sentence.lower().find(focus_word.lower()) != -1):             
            sentence = sentence.lower().replace(focus_word.lower(), "___");         
        wiki_alternative = sentence         
        print("Constructed wiki alternative: " + wiki_alternative)     
    else :         
        print("Not Constructed wiki alternative since any found") 
 
def constructMostRelativeAlternative() :     
    eliminates = ["DT", "CD", "IN", "PRP$", "PRP", "RP", "RB", ".", ",", "TO", "EX", "CC", "WRB", "MD", "POS", "$", "''", "``"]     
    global focus_word, focus_word_synsets, most_relative_example     
    print("Constructing most-relative alternative...")     
    most_relative = None     
    most_relatives = []     
    examples = []     
    for synset in focus_word_synsets :         
        examples.extend(synset.examples()) 
 
    if len(examples) > 0 :         
        print("Examples to look for most-relative:")         
        for example in examples :             
            print(example)     
    else :         
        print("Not found any example returning...")     
    default_relative = Relative(focus_word, focus_word, examples)     
    most_relatives.append(default_relative)     
    example_tokens = []     
    if len(examples) > 0 :          
        example_tokens = word_tokenize(examples.pop(0))         
        tagged = nltk.pos_tag(example_tokens)         
        decrease = 0         
        for i in range(0, len(tagged)):              
            eliminate = False             
            for eliminate_v in eliminates :                 
                if eliminate_v == tagged[i - decrease][1] :                     
                    eliminate = True                     
                    break             
            if eliminate :                 
                example_tokens.pop(i - decrease)                 
                tagged.pop(i - decrease) 
                decrease += 1         
            most_relatives[0].examples.pop(0)     
            while True :         
                if most_relatives[0].equals(default_relative) :             
                    if len(example_tokens) > 0 :                 
                        insert = Relative(example_tokens.pop(0), focus_word, examples)                 
                        insert_flag = True                 
                        for curr in most_relatives :                     
                            if insert.equals(curr) :                         
                                insert_flag = False                 
                        if insert_flag :                     
                            most_relatives.insert(0, insert)                     
                            print("New relative inserted into relatives list: " + insert.token)             
                    elif len(examples) > 0 :                 
                        example_tokens = word_tokenize(examples.pop(0))                 
                        tagged = nltk.pos_tag(example_tokens)                 
                        decrease = 0                 
                        for i in range(0, len(tagged)):                      
                            eliminate = False                     
                            for eliminate_v in eliminates :                         
                                if eliminate_v == tagged[i - decrease][1] :                             
                                    eliminate = True                             
                                    break                     
                            if eliminate :                         
                                example_tokens.pop(i - decrease)                         
                                tagged.pop(i - decrease)                         
                                decrease += 1                 
                        most_relatives[0].examples.pop(0)             
                    else :                 
                        if len(most_relatives) > 1 :                     
                            most_relative = most_relatives[1]                     
                            most_relatives[1] = most_relatives[0]                     
                            most_relatives[0] = most_relative                     
                            continue                 
                        else :                     
                            break         
                elif not most_relatives[0].checkFinished() :             
                    #print("Executing relative: " + most_relatives[0].token)             
                    most_relatives[0].execute()         
                else :             
                    print("Search terminated since a dominant relative found or possible tokens finished")             
                    most_relative = most_relatives[0]             
                    break         
                #print("Sorting relatives list")         
                most_relatives.sort(key=Relative.getHeuristicValue)       
                
            found_sentence = None     
            found = False     
            if not most_relative is None :         
                print("Most relative token: " + most_relative.token)         
                print("Looking its examples to find answer...")         
                most_relative_synsets = wordnet.synsets(most_relative.token)         
                for synset in most_relative_synsets :             
                    examples = synset.examples()             
                    for example in examples :                 
                        print("Looking into example: " + example)                 
                        tokens = word_tokenize(example)                 
                        for token in tokens : 
                            if token.lower() == focus_word.lower() :                         
                                print("Example including answer; transforming its form")                         
                                found_sentence = example                         
                                found = True                         
                                break                 
                        print("Not found any answer match")                 
                        if found :                     
                            break             
                    if found :                 
                        break         
                if not found_sentence is None :             
                    found_sentence = found_sentence.lower().replace(focus_word.lower(), "___")             
                    most_relative_example = found_sentence             
                    print("Constructed most-relative alternative: " + most_relative_example)         
                else :             
                    print("Not constructed most-relative alternative since any answer including example found")     
            else :         
                print("Not constructed most-relative alternative since any relative found") 
 
class Relative() : 
 
    eliminates = ["is", "'s", "was", "are", "'re", "were", "a", "an"]     
    def __init__(self, token, focusWord, examples) :         
        for elim in Relative.eliminates :             
            if token.lower() == elim :                 
                token = ""                 
                break         
        self.token = token         
        self.examples = []         
        for example in examples :             
            self.examples.append(example)         
        self.hit = 1         
        if not (self.token == focusWord or self.token == "") :             
            self.initializeHit(focusWord) 
 
    def initializeHit(self, focusWord) :         
        synsets = wordnet.synsets(self.token)         
        for synset in synsets :             
            examples = synset.examples()             
            for example in examples :                 
                tokens = word_tokenize(example)                 
                for token in tokens :                     
                    if ps.stem(token).lower() == ps.stem(focus_word).lower() :                         
                        self.hit += 1         
        #print("Initializing relation score of relative: " + str(self.hit)) 
 
    def checkSimilar(self, check) :         
        if ps.stem(check).lower() == ps.stem(self.token).lower() :             
            return True         
        return False 
 
    def checkFinished(self) :         
        return len(self.examples) == 0 
 
    def execute(self):         
        if not self.checkFinished() :             
            example = self.examples.pop(-1)             
            tokens = word_tokenize(example) 
            for token in tokens :                 
                if self.checkSimilar(token) :                     
                    self.hit += 1                     
                    #print("Relation score increased since other match found; score: " + str(self.hit)) 
 
    def getHeuristicValue(self) :         
        return 1 / (self.hit * (len(self.examples) + 1)) 
 
    def equals(self, check) :         
        if ps.stem(self.token).lower() == ps.stem(check.token).lower() :             
            return True         
        return False 
 
    def toString(self) :         
        return self.token 
 
def constructTransformedAlternateString() :     
    eliminates = ["DT", "CD", "IN", "PRP$", "PRP", "RP", "RB", ".", ",", "TO", "EX", "CC", "WRB", "MD", "POS", "$", "''", "``"]     
    eliminate_tokens = ["is", "'s", "was", "are", "'re", "were", "a", "an"]     
    global focus_word, alternate_string, transformed_alternate_string     
    print("Constructing transform-clue alternative") 
 
    tkns = word_tokenize(alternate_string)     
    tagged = nltk.pos_tag(tkns)     
    decrease = 0     
    for i in range(0, len(tagged)):          
        eliminate = False         
        for eliminate_v in eliminates :             
            if eliminate_v == tagged[i - decrease][1] :                 
                eliminate = True                 
                break         
        if eliminate :             
            tkns.pop(i - decrease)             
            tagged.pop(i - decrease)             
            decrease += 1      
    for tkn in tkns :         
        for elim in eliminate_tokens :             
            if tkn.lower() == elim :                 
                tkns.remove(tkn)                 
                break 
 
    default_transform = Transform(tkns)     
    print("Initial clue inserted into transform list: " + str(default_transform.tokens))     
    transforms = []     
    transforms.append(default_transform)     
    while True :         
        execute_transform = transforms[0]         
        print("Executing transform: " + str(execute_transform.tokens))         
        executes = execute_transform.execute(focus_word)         
        if not executes is None :             
            for execute in executes :                 
                for transform in transforms :                     
                    if execute.equals(transform) :                         
                        executes.remove(execute)                         
                        break             
            transforms.extend(executes)             
            for tr in executes : 
                print("New transform inserted into list: " + str(tr.tokens))             
            print("Sorting transform list...")             
            transforms.sort(key=Transform.getHeuristicValue)         
        if transforms[0].checkFinished() :             
            print("Transform-clue search terminated since no reasonable transform left")             
            break     
    if not transforms[0].equals(default_transform) :          
        transformed_alternate_string = ""         
        tokens = word_tokenize(alternate_string)         
        transformed_index = 0         
        for i in range(0, len(tokens)) :             
            if not len(tkns) > i :                 
                transformed_alternate_string += tokens[i] + " "             
            elif not tkns[transformed_index] == tokens[i] :                 
                transformed_alternate_string += tokens[i] + " "             
            else :                 
                transformed_alternate_string += transforms[0].tokens[transformed_index] + " "                 
                transformed_index += 1         
        print("Constructed transform-clue alternative: " + transformed_alternate_string)     
    else :         
        print("Not constructed transform-clue alternative since any reasonable transform found") 
 
class Transform() : 
 
    def __init__(self, tokens, default_transform=True) :         
        global focus_word         
        self.tokens = []         
        for token in tokens :             
            self.tokens.append(token)         
        self.curr_execute_index = 0         
        self.index_transform_count = []         
        self.relation_scores = []         
        if default_transform :             
            for token in self.tokens :                 
                self.index_transform_count.append(0)             
            self.initializeRelationScore(focus_word) 
 
    def checkFinished(self) :         
        return not (len(self.tokens) - self.curr_execute_index > 0) 
 
    def initializeRelationScore(self, related_word) :         
        for i in range(0, len(self.tokens)) :             
            self.relation_scores.append(0)         
        synsets = wordnet.synsets(related_word)         
        for synset in synsets :             
            for example in synset.examples() :                 
                example_tokens = word_tokenize(example)                 
                for i in range(0, len(self.tokens)) :                     
                    for token in example_tokens :                         
                        if ps.stem(self.tokens[i]).lower() == ps.stem(token).lower() :                             
                            self.relation_scores[i] += 1         
        for i in range(0, len(self.tokens)) :             
            synsets = wordnet.synsets(self.tokens[i])             
            for synset in synsets :                 
                for example in synset.examples() :                     
                    example_tokens = word_tokenize(example)                     
                    for token in example_tokens :                         
                        if ps.stem(token).lower() == ps.stem(related_word).lower() : 
                            self.relation_scores[i] += 1 
 
    def execute(self, related_word) :         
        if self.curr_execute_index < len(self.tokens) :             
            execute_token = self.tokens[self.curr_execute_index]             
            synsets = wordnet.synsets(execute_token)             
            synonms = []             
            for synset in synsets :                 
                for synonm in synset.lemma_names() :                     
                    insert = True                     
                    for curr in synonms :                         
                        if curr == synonm :                             
                            insert = False                             
                            break                     
                        if insert :                         
                            synonms.append(synonm)             
            for synonm in synonms :                 
                if ps.stem(synonm).lower() == ps.stem(execute_token).lower() :                     
                    synonms.remove(synonm)             
            transforms = []             
            for i in range(0, len(synonms)) :                 
                transforms.append(Transform(self.tokens, False))                 
                transforms[i].tokens[self.curr_execute_index] = synonms[i]                 
                for n in range(0, len(self.index_transform_count)) :                     
                    transforms[i].index_transform_count.append(self.index_transform_count[n])                 
                transforms[i].index_transform_count[self.curr_execute_index] += 1                 
                for n in range(0, len(self.relation_scores)) :                     
                    transforms[i].relation_scores.append(self.relation_scores[n])                 
                transforms[i].relation_scores[self.curr_execute_index] = 0                 
                synsets = wordnet.synsets(related_word)                 
                for synset in synsets :                     
                    for example in synset.examples() :                         
                        example_tokens = word_tokenize(example)                         
                        for token in example_tokens :                             
                            if ps.stem(transforms[i].tokens[self.curr_execute_index]).lower() == ps.stem(token).lower() :                                 
                                transforms[i].relation_scores[self.curr_execute_index] += 1                 
                synsets = wordnet.synsets(transforms[i].tokens[self.curr_execute_index])                 
                for synset in synsets :                     
                    for example in synset.examples() :                         
                        example_tokens = word_tokenize(example)                         
                        for token in example_tokens :                             
                            if ps.stem(related_word).lower() == ps.stem(token).lower() :                                 
                                transforms[i].relation_scores[self.curr_execute_index] += 1             
            self.curr_execute_index += 1             
            return transforms         
        return None       
    
    def equals(self, check) :         
        equals = True         
        for i in range(0, len(self.tokens)) :             
            if not ps.stem(self.tokens[i]).lower() == ps.stem(check.tokens[i]).lower() :                 
                equals = False                 
                break         
        return equals         
        
    def getHeuristicValue(self) : 
        transform_score = 0         
        for transform in self.index_transform_count :             
            if not transform == 0 :                 
                transform_score += 1         
        deviation_score = 0         
        for transform in self.index_transform_count :             
            deviation_score += transform         
        relation_score = 0         
        for score in self.relation_scores :             
            relation_score += score         
        return (deviation_score + 1) / (math.pow(transform_score + 1, 3) * math.pow(relation_score + 1, 2)) 
 
    def extractDefinitionAlternative() :     
        return focus_word_definition 
 
    def extractSynonmAlternative() :     
        if not focus_word_synonm is None:         
            return "The synonm of " + focus_word_synonm     
        return None 
 
    def extractAntonymAlternative() :     
        if not focus_word_antonym is None:         
            return "The antonym of " + focus_word_antonym     
        return None 
 
    def extractWikiAlternative() :     
        return wiki_alternative 
 
    def extractMostRelativeAlternative() :     
        return most_relative_example 
 
    def extractTransformedAlternateString() :     
        return transformed_alternate_string 
 
    def reconstructAlternativeList() :     
        global alternative_list, focus_word_definition, focus_word_synonm, focus_word_antonym, wiki_alternative, most_relative_example, transformed_alternate_string     
        constructDefinitionAlternative()     
        constructWikiAlternative()     
        constructSynonmAntonymAlternative()     
        constructMostRelativeAlternative()     
        constructTransformedAlternateString()     
        print("Alternative list for answer&clue: " + focus_word + ", " + alternate_string)     
        alternative_list = []     
        if not focus_word_definition is None :         
            alternative_list.append(extractDefinitionAlternative())         
            print("Inserted wordnet-definition alternative into alternative list: " + focus_word_definition)     
        if not wiki_alternative is None :         
            alternative_list.append(extractWikiAlternative())         
            print("Inserted wiki alternative into alternative list: " + wiki_alternative)     
        if not focus_word_synonm is None :         
            alternative_list.append(extractSynonmAlternative())         
            print("Inserted wordnet-synonm alternative into alternative list: " + focus_word_synonm)     
        if not focus_word_antonym is None :         
            alternative_list.append(extractAntonymAlternative())         
            print("Inserted wordnet-antonym alternative into alternative list: " + focus_word_antonym)     
        if not most_relative_example is None : 
            alternative_list.append(extractMostRelativeAlternative())         
            print("Inserted most-relative alternative into alternative list: " + most_relative_example)     
        if not transformed_alternate_string is None :         
            alternative_list.append(extractTransformedAlternateString())         
            print("Inserted transform-clue alternative into alternative list: " + transformed_alternate_string)     
        #eliminateAlternative()     
        if len(alternative_list) > 0 :         
            print("Ordering alternative list through checking difference from origin clue")         
            orderAlternativeList()         
            print("Ordered alternative list:")         
            for alternative in alternative_list :             
                print(alternative)     
        else :         
            print("Not any alternative found") 
 
    def eliminateAlternative() :     
        global focus_word, alternative_list     
        for alternative in alternative_list :         
            tokenized = word_tokenize(alternative)         
            for token in tokenized :              
                if token.lower() == focus_word.lower() :                 
                    alternative_list.remove(alternative) 
 
    def orderAlternativeList() :     
        global alternate_string, alternative_list     
        alternatives = []     
        for alternative in alternative_list :         
            alternatives.append(Alternative(alternative))     
        alternatives.sort(key=Alternative.getHeuristicValue)     
        while not alternatives[0].checkfinished() :         
            alternatives[0].execute(alternate_string)         
            alternatives.sort(key=Alternative.getHeuristicValue)     
        alternative_list = []     
        for alternative in alternatives :         
            alternative_list.append(alternative.string) 
 
class Alternative() : 
 
    def __init__(self, string) :         
        global focus_word         
        self.string = string         
        self.related_word = focus_word         
        eliminates = ["DT", "CD", "IN", "PRP$", "PRP", "RP", "RB", ".", ",", "TO", "EX", "CC", "WRB", "MD", "POS", "$", "''", "``"]         
        eliminate_tokens = ["is", "'s", "was", "are", "'re", "were", "a", "an", "___"]         
        self.tokens = word_tokenize(string)         
        tagged = nltk.pos_tag(self.tokens)         
        decrease = 0         
        for i in range(0, len(tagged)):              
            eliminate = False             
            for eliminate_v in eliminates :                 
                if eliminate_v == tagged[i - decrease][1] :                     
                    eliminate = True                     
                    break             
                if eliminate :                 
                    self.tokens.pop(i - decrease)                 
                    tagged.pop(i - decrease)                 
                    decrease += 1  
        for tkn in self.tokens :             
            for elim in eliminate_tokens :                 
                if tkn.lower() == elim :                     
                    self.tokens.remove(tkn)                     
                    break         
        self.execute_index = 0         
        self.alternative_score = 0 
 
    def checkfinished(self) :         
        return not len(self.tokens) > self.execute_index 
 
    def execute(self, execute_string) :          
        if not self.checkfinished() :             
            execute_token = self.tokens[self.execute_index]             
            if ps.stem(execute_token).lower() == ps.stem(self.related_word).lower() :                 
                self.alternative_score += 1000             
            else :                 
                check_tokens = word_tokenize(execute_string)                 
                for token in check_tokens :                     
                    for synset in wordnet.synsets(token) :                         
                        for example in synset.examples() :                             
                            for example_token in word_tokenize(example) :                                 
                                if ps.stem(example_token).lower() == ps.stem(execute_token).lower() :                                     
                                    self.alternative_score += 1                 
                for synset in wordnet.synsets(execute_token) :                     
                    for example in synset.examples() :                         
                        for example_token in word_tokenize(example) :                             
                            for token in check_tokens :                                 
                                if ps.stem(example_token).lower() == ps.stem(token).lower() :                                     
                                    self.alternative_score += 1             
            self.execute_index += 1 
 
    def getHeuristicValue(self) :         
        length = len(self.tokens)         
        remaining_rate = (length - self.execute_index) / (length + 1)         
        return math.pow(self.alternative_score + 1, 0.5) / ((remaining_rate * 10 + 1) * math.pow(length + 1, 2))