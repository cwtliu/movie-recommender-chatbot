#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Oishi Banerjee and Christopher Liu -
# INCLUDED PORTERSTEMMER below
#
# We completed most of the Starter code early on, prior to clarification about dates being included in the titles.
# The TA during office hours told us to just ask the user to remove dates in our intro.
#
#
#
#STARTER COMPLETES:
# Identifying movies in quotation marks, with correct capitalization (2)
# Speaking reasonably fluently (6)
# Failing gracefully (8)
# Extracting sentiment from simple inputs (10)
# Making reasonable movie recommendation (4)
#
#
#CREATIVE COMPLETES:
# Identifying movies without Quotation Marks or perfect capitalization (4)
# Fine-grained Sentiment Extraction (4)
# Spell-checking Movie Titles (4) 
# 	- They can miscapitalize words and it is still fine
# Disambiguating movie titles for series and year ambiguities (4?)
#   - can handle general cases like Harry Potter and Pirates of the Caribbean
# Responding to arbitrary input (4)
# Speaking fluently (4)
# Alternate/foreign titles - does not handle accented letters, but does handle alternate words (4?)
# Other features: 
# Returns a descriptor of the movie recommendation based on its genre (+)
# 
#
# PA6, CS124, Stanford, Winter 2016
# v.1.0.2
# Original Python code by Ignacio Cases (@cases)
# Ported to Java by Raghav Gupta (@rgupta93) and Jennifer Lu (@jenylu)
######################################################################
import csv
import math
import re
import sys
import numpy
import random

from movielens import ratings
from random import randint

class Chatbot:
    """Simple class to implement the chatbot for PA 6."""

    #############################################################################
    # `moviebot` is the default chatbot. Change it to your chatbot's name       #
    #############################################################################
    def __init__(self, is_turbo=False):
      self.name = 'J.A.R.V.I.S.'
      self.is_turbo = is_turbo
      self.user_movies = []
      self.read_data()
      self.b = ""  # buffer for word to be stemmed
      self.k = 0
      self.k0 = 0
      self.j = 0   # j is a general offset into the string
      self.recs=[]
      self.recommendedMovies = []
      self.inRecMode = False
      self.ALPHABET = 'abcdefghijklmnopqrstuvwxyz '

    #############################################################################
    # 1. WARM UP REPL
    #############################################################################

    def greeting(self):
      """chatbot greeting message"""
      #############################################################################
      # TODO: Write a short greeting message                                      #
      #############################################################################

      greeting_message = 'Tell me about a movie that you\'ve seen. Please do not include the date when telling me about the movie. For example, if you want to tell me about "Toy Story (1995)", only type in "Toy Story".'

      #############################################################################
      #                             END OF YOUR CODE                              #
      #############################################################################

      return greeting_message

    def goodbye(self):
      """chatbot goodbye message"""
      #############################################################################
      # TODO: Write a short farewell message                                      #
      #############################################################################

      goodbye_message = 'Have a nice day!'

      #############################################################################
      #                             END OF YOUR CODE                              #
      #############################################################################

      return goodbye_message


    #############################################################################
    # 2. Modules 2 and 3: extraction and transformation                         #
    #############################################################################
    
    #def stemmed(self,word):
    #	#if word.endswith(
    #	if word[-1] == 's':
    #		word = word[:len(word)-1]
    #		return word
    #	return word
    def fullStem(self, word):
    	newWord=""
    	for char in word:
    		if char>='A' and char<='Z':
    			newWord+=char
    		elif char>='a' and char<='z':
    			newWord+=char
    	return self.stem(newWord)
    def isInUserMovies(self, title_index):
    	for user_movie in self.user_movies:
    		if user_movie[0]==title_index:
    			return True
    	return False
    def detectSentiment(self, review):
    	portions = review.split('"')
    	pos = 0
    	neg = 0
    	afterNegation = False
    	afterIntensifier = False
    	reallygoodwords = ["favorite", "love", "amazing", "awesome", "enjoy","great", "good"]
    	for index in range(0,len(reallygoodwords)):
    		reallygoodwords[index] = self.fullStem(reallygoodwords[index])
    	reallybadwords = ["bad", "hate", "horrible","awful","terrible","dreadful","boring"]
    	for index in range(0,len(reallybadwords)):
    		reallybadwords[index] = self.fullStem(reallybadwords[index])
    	for word in portions[0].split():
    		#print "SENTIMENT"+self.sentiment[word]
    		#if word not in self.sentiment:
    		#	word = self.stemmed(word)
    		stemmedWord = self.fullStem(word)
    		word.lower()
	    	if self.stemmedSentiment.get(stemmedWord,'')=='pos' and not afterNegation:
    			pos+=2
    			if afterIntensifier or "!!" in word:
    				pos+=3
    			if word in reallygoodwords:
    				pos+=2
    		elif self.stemmedSentiment.get(stemmedWord,'')=='neg' and not afterNegation:
    			neg+=2
    			if afterIntensifier or "!!" in word:
    				neg+=3
    			if word in reallybadwords:
    				neg+=2
    		elif self.stemmedSentiment.get(stemmedWord,'')=='pos' and afterNegation:
    			neg+=1
    		elif self.stemmedSentiment.get(stemmedWord,'')=='neg' and afterNegation:
    			pos+=1
    		
    		if word == "not" or word == "neither" or word == "nor" or "n\'t" in word:
    			afterNegation = True
    		elif "." in word or "," in word or "!" in word or "?" in word or word == "but":
    			afterNegation = False
    		if word == "really" or word == "very" or word == "totally" or word == "extremely" or word == "most" or word == "completely":
    			afterIntensifier = True
    		else:
    			afterIntensifier=False
    		
    		
    	for word in portions[2].split():
    		#print "SENTIMENT"+self.sentiment[word]
    		stemmedWord = self.fullStem(word)
    		if self.stemmedSentiment.get(stemmedWord,'')=='pos' and not afterNegation:
    			pos+=2
    			if afterIntensifier or "!!" in word:
    			  	#print word
    				pos+=3
    			if word in reallygoodwords:
    				pos+=2
    		elif self.stemmedSentiment.get(stemmedWord,'')=='neg' and not afterNegation:
    			neg+=2
    			if afterIntensifier or "!!" in word:
    				neg+=3
    			if word in reallybadwords:
    				neg+=2
    		elif self.stemmedSentiment.get(stemmedWord,'')=='pos' and afterNegation:
    			neg+=1
    		elif self.stemmedSentiment.get(stemmedWord,'')=='neg' and afterNegation:
    			pos+=1
    		if word == "not" or word == "neither" or word == "nor" or "n\'t" in word:
    			afterNegation = True
    		elif "." in word or "," in word or "!" in word or "?" in word or word == "but":
    			afterNegation = False
    		if word == "really" or word == "very" or word == "totally" or word == "extremely" or word == "most" or word == "completely":
    			afterIntensifier = True
    		else:
    			afterIntensifier=False
    	if neg == 0 and pos == 0:
    		return 0
    	elif neg == 0:
    		return 1
    	elif pos == 0:
    		return -1
    	thresholdRatio = 3.1
    	if float(pos)/neg >= thresholdRatio:
    		return 1
    	elif float(neg)/pos >= thresholdRatio:
    		return -1
    	
    	return 0
    def startsWithArticle(self, movietitle):
   	 	movietitle_words= movietitle.split()
   	 	if len(movietitle_words)>0 and (movietitle_words[0].lower() == "the" or movietitle_words[0].lower() == "an" or movietitle_words[0].lower() == "a" or movietitle_words[0].lower() == "la" or movietitle_words[0].lower() == "le"):
			return True
		return False
    
    
    def combinations(self, wordedits, prefix, possibleedits):
    	if len(wordedits)==0:
    		possibleedits.add(prefix.strip())
    		return
    	for wordedit in wordedits[0]:
    		self.combinations(wordedits[1:], prefix+" "+wordedit, possibleedits)
    def deleteEdits(self,word):
    	if len(word) <= 0:
    		return []
    	#word = "<" + word #Append start character
    	ret = set()
    	for i in xrange(0, len(word)):
    		correction = "%s%s" % (word[0:i], word[i+1:])
    		
    		correction_words = correction.split() #handles cases where multiple words were passed in
    		isValidPhrase = True
    		for correction_word in correction_words:
    			if correction_word not in self.titleWords:
    				isValidPhrase = False
    		if isValidPhrase:
    			ret.add(correction)
    	return ret
    def phraseStartsMovie(self, phrase):
    	for title in self.titles:
    		if re.match(phrase, title[0])!=None:
    			return True
    	return False
    def findMovieWithoutQuotations(self, sentence):
    	sentence_words = sentence.split()
    	for index in range(0, len(sentence_words)):
    		sentence_word=sentence_words[index]
    		if sentence_word[0]>="A" and sentence_word[0]<="Z":
    			possible_title = ""
    			for inner_index in range(index, len(sentence_words)):
    				possible_title+=sentence_words[inner_index]+" "
    			#	print possible_title
    			#	print self.checkmovie(possible_title)
    				#if not self.phraseStartsMovie(possible_title):
    			#		print "no movie starts with "+possible_title
    		#			break
    				if self.checkspecificmovie(possible_title)>=0:
    				 rtn = ""
    				 for start_index in range(0, index):
    				 	rtn+=sentence_words[start_index]+" "
    				 rtn+='"'
    				 for title_index in range(index, inner_index+1):
    				 	rtn+=sentence_words[title_index]+" "
    				 rtn=rtn.strip()
    				 rtn+='" '
    				 for end_index in range (inner_index+1, len(sentence_words)):
    				 	rtn+=sentence_words[end_index]+" "
    				 rtn=rtn.strip()
    				 #print "Added quotation marks: "+rtn
    				 return rtn
    	#print "couldn't find movie"
    	return sentence
    		
    	
    def insertEdits(self,word):    
    	ret = set()
    	for before in range(-1,len(word)):
        	for c in self.ALPHABET:
        		correction = "%s%s%s" % (word[0:before+1],c+"",word[before+1:])
        		correction_words = correction.split() #handles cases where multiple words were passed in
    			isValidPhrase = True
    			for correction_word in correction_words:
    				if correction_word not in self.titleWords:
    					isValidPhrase = False
    			if isValidPhrase:
    				ret.add(correction)
    	return ret
    def transposeEdits(self, word):
    	ret = set()
    	for first in range(0,len(word)-1):
        	second = first+1
        	firstCharacter = word[first]
        	secondCharacter = word[second]
        	if firstCharacter!=secondCharacter:
        		firstChunk = word[:first]
        		secondChunk = word[second+1:]
        		correction = "%s%s%s%s" % (firstChunk, secondCharacter, firstCharacter, secondChunk)
        		correction_words = correction.split() #handles cases where multiple words were passed in
        		isValidPhrase = True
    			for correction_word in correction_words:
    				if correction_word not in self.titleWords:
    					isValidPhrase = False
    			if isValidPhrase:
    				ret.add(correction)
    	return ret
    	
    def replaceEdits(self, word):
    	ret = set()
    	for curr in range(0,len(word)):
    		for c in self.ALPHABET:
    			if c != word[curr]:
    				correction = "%s%s%s" % (word[0:curr],c,word[curr+1:])
    				correction_words = correction.split() #handles cases where multiple words were passed in
        			isValidPhrase = True
    				for correction_word in correction_words:
    					if correction_word not in self.titleWords:
    						isValidPhrase = False
    				if isValidPhrase:
    					ret.add(correction)
    	return ret
    def edits(self, word):
    	rtn = set()
    	rtn.add(word)
    	rtn=rtn.union(self.deleteEdits(word))
    	rtn=rtn.union(self.insertEdits(word))
    	rtn=rtn.union(self.transposeEdits(word))
    	rtn=rtn.union(self.replaceEdits(word))
    	if len(rtn) > 10:
    		rtn = set()
    		rtn.add (word)
    		return rtn
    	return rtn
    	
    def generateAlternateSpellings(self, movietitle):
    	possibleedits = self.edits(movietitle)
    	
    	
    	titlewords = movietitle.split()
    	wordedits = []
    	for word_index in range(0, len(titlewords)):
    		 wordedits.append(self.edits(titlewords[word_index]))    	
    	self.combinations(wordedits, "", possibleedits)
    	return (possibleedits)
    	
    def deleteStartingArticle(self, movietitle):
    	movietitle_words= movietitle.split()
    	article = movietitle_words[0]
    	del movietitle_words[0]
    	rtn = ""
    	for movietitle_word in movietitle_words:
    		rtn+=movietitle_word
    		rtn+=" "
    	return rtn.strip()
    def moveArticleToBack(self, movietitle):
    	movietitle=movietitle.lower()
    	#print "first two letters = "+movietitle[0:1]
    	if self.startsWithArticle(movietitle):
    		movietitle_words=movietitle.split()
    		article=movietitle_words[0]
    		del movietitle_words[0]
    		rtn=""
    		for movietitle_word in movietitle_words:
    			rtn+=movietitle_word
    			rtn+=" "
    		rtn=rtn.strip()
    		rtn+=", "+article
    		return rtn
    	elif len(movietitle)>=3 and movietitle[0:2]=="l'":
    		#print "l' case"
    		movietitle = movietitle[3:]+", l'"
    		return movietitle
    	else:
    		return movietitle
    def checkspecificmovie(self, movietitle):
    	if movietitle.strip()=="":
    		return -1
    	#print movietitle.lower()

    	for index in range(0,len(self.titles)):
    		#matches = re.match(movietitle+r' \(\d\d\d\d\)', self.titles[index][0])
    		#if matches!=None:
    		#	return index
    		movietitle = movietitle.lower().strip()
    		movietitle = movietitle.replace('(', '').replace(')', '')
    		movietitle = movietitle.replace('[', '').replace(']', '')
    		matches = re.match(r'(the |an |a |la |le |l\')?'+movietitle+r'(, the|, an|, a|, la|, le|, l\')? (\(.*\) )*\(\d\d\d\d\)', self.titles[index][0].lower())
    		if matches!=None:
    			return index
    		matches = re.findall(r'\((a\.k\.a\. )?(the |an |a |la |le |l\')?'+movietitle.lower()+r'(, the|, an|, a|, la|, le|, l\')?\) (\(.*\) )*\(\d\d\d\d\)', self.titles[index][0].lower())
    		if len(matches)==1:
    			return index
    	#if self.startsWithArticle(movietitle) and movietitle.lower()!="the" and movietitle.lower()!="an" and movietitle.lower()!="a":
    #		print('cool')
   # 		return self.checkmovie(self.deleteStartingArticle(movietitle))
   		movedArticleToBack = self.moveArticleToBack(movietitle)
    	if movietitle!=movedArticleToBack:
    		return self.checkspecificmovie(movedArticleToBack)
    	return -1
    def checkmovie(self, movietitle):
    	movietitle=movietitle.lower()
    	index_of_movie = self.checkspecificmovie(movietitle)
    	if index_of_movie>-1:
    		#print "here it is"
    		#print index_of_movie
    		return index_of_movie
    	if len(movietitle) != 1:
    		alternateSpellings = self.generateAlternateSpellings(movietitle)
    		#print alternateSpellings
    		for alternateSpelling in alternateSpellings:
    			index_of_movie = self.checkspecificmovie(alternateSpelling)
    			if index_of_movie>-1:
    				return index_of_movie
    	#print "here it is"
    	#print index_of_movie
    	return index_of_movie
    	
    def dotproduct(self, array1, array2):
    	sum = 0
    	for user in range (0, len(array1)):
    		if array1[user] != 0 and array2[user]!=0:
    			sum+=array1[user]*array2[user]
    	return sum
    	
    def cosinesim(self, array1, array2):
    	divisor = numpy.linalg.norm(array1)*numpy.linalg.norm(array2)
    	if divisor ==0:
    		return -1.0
    	return numpy.dot(array1, array2)/divisor
    	
    def remove_repeat_movies(self, usermovies, final_movie_scores):
    	filtered_movie_scores = []
    	for final_movie_score in final_movie_scores:
    		isNewMovie = True
    		if final_movie_score[1] in self.recommendedMovies:
    			isNewMovie = False
    		for usermovie in usermovies:
    			if self.titles[final_movie_score[1]][0]==self.titles[usermovie[0]][0]:
    				#print "removing "+self.titles[final_movie_score[1]][0]
    				isNewMovie=False
    		if isNewMovie:
    			filtered_movie_scores.append(final_movie_score)
    	return filtered_movie_scores
   # def get_highest_scoring_movie(self, usermovies, final_movie_scores):
   # 	rtn = ""
   # 	final_movie_scores.sort()
   # 	for final_movie_score_index in range (1, len(final_movie_scores)+1):
   # 		final_movie_score = final_movie_scores[-final_movie_score_index]
   # 		isNewMovie = True
   # 		for usermovie in usermovies:
   # 			if self.titles[final_movie_score[1]][0]==usermovie[0]:
   # 				isNewMovie=False
   # 		if isNewMovie:
   # 			return self.titles[final_movie_score[1]][0]
    	#highest_score = -11111111
    	#for index in range(0, len(final_movie_scores)):
    ###		if final_movie_scores[index]>highest_score:
    	#		isNewMovie = True
    #			for usermovie in usermovies:
   # 				#print "Usermovie " + usermovie[0]
   # 				#print self.titles[index] 
   # 				if usermovie[0]== self.titles[index][0]:
   # 					isNewMovie = False
   # 			if isNewMovie:
   # 				highest_score = final_movie_scores[index]
   # 				rtn = self.titles[index][0]
    #	return ""
    def recommendation(self, usermovies):
    #	usermovies = ([8708, 1], [6944, 1], [7890,1], [4688,1], [7790,1], [8637,1], [8786,1], [6695,1])
    	final_movie_scores = []
    	for movie_index in range (0, len(self.titles)):
    		final_movie_scores.append([0, movie_index])
    	for usermovie in usermovies:
    		ratings_of_usermovie = self.ratings[usermovie[0]]
    		#print ratings_of_usermovie
    		#print (len(ratings_of_usermovie))
    		for movie_index in range(0, len(self.titles)):
    			ratings_of_movie = self.ratings[movie_index]
    			score = usermovie[1] * self.cosinesim(ratings_of_movie, ratings_of_usermovie)
    		#	if score>.5:
    	#			print self.titles[movie_index][0]+" "+str(score)
    			#print score
    			final_movie_scores[movie_index][0] += score
    	final_movie_scores = self.remove_repeat_movies(usermovies, final_movie_scores)
    	final_movie_scores.sort()
    	final_movie_scores.reverse()
    	return final_movie_scores
    	
    def getRecTitle(self):
    	rtn = self.titles[self.recs[0][1]][0]
    	self.recommendedMovies.append(self.recs[0][1])
    	#print self.recommendedMovies
    	return rtn
    	
    	
    	
    def genreResponse(self):
    	genredict = {}
    	genredict["Adventure"] = ["exciting", "exhilarating", "fast-paced"]
    	genredict["Animation"]=["beautifully rendered", "artistic", "visually breathtaking"]
    	genredict["Children"]=["child-friendly", "kid-friendly"]
    	genredict["Comedy"]=["funny", "hilarious", "zany", "fun", "smartly written"]
    	genredict["Fantasy"] = ["fantastical", "whimsical", "fanciful"]
    	genredict["Horror"]=["terrifying", "suspenseful", "macabre"]
    	genredict["Thriller"] = ["thoroughly thrilling", "gripping", "action-packed"]
    	genredict["Action"]=["surprising", "thoroughly awesome", "satisfyingly violent"]
    	genredict["Romance"]=["romantic", "sweet", "touching", "poignant"]
    	genredict["Crime"]=["interesting", "somewhat dark", "cleverly plotted"]
    	genredict["Drama"]=["complex", "elaborate", "compelling"]
    	genredict["Mystery"]=["intriguing", "riveting", "captivating"]
    	genredict["Sci-Fi"]=["geeky", "inventive"]
    	genredict["Documentary"]=["informative","illuminating"]
    	genredict["War"]=["heart-wrenching", "moving"]
    	genredict["Musical"]=["exquisitely scored", "larger-than-life"]
    	genredict["Western"]=["vigorous", "powerful"]
    	genredict["Film-Noir"]=["sophisticated", "sylish"]
    	genredict["IMAX"]=["epic"]
    	#print(self.titles[self.recs[0][1]])
    	if '(no genres listed)' in self.titles[self.recs[0][1]][1]:
    		return ""
    	genres = self.titles[self.recs[0][1]][1].split("|")
    	if len(genres) > 2:
    		randomly_picked_genre = random.choice(genres)
    		descriptor1 = random.choice(genredict[randomly_picked_genre])
    		
    		genres.remove(randomly_picked_genre)
    		randomly_picked_genre = random.choice(genres)
    		descriptor2 = random.choice(genredict[randomly_picked_genre])
    		
    		genres.remove(randomly_picked_genre)
    		randomly_picked_genre = random.choice(genres)
    		descriptor3 = random.choice(genredict[randomly_picked_genre])
    		return " This movie is %s,"% descriptor1+" %s" % descriptor2+", and %s." % descriptor3
    	elif len(genres) == 2:
    		randomly_picked_genre = random.choice(genres)
    		descriptor1 = random.choice(genredict[randomly_picked_genre])
    		
    		genres.remove(randomly_picked_genre)
    		randomly_picked_genre = random.choice(genres)
    		descriptor2 = random.choice(genredict[randomly_picked_genre])

    		return " You might like this movie, because it's is %s"% descriptor1+" and %s." % descriptor2
    	else:
    		randomly_picked_genre = random.choice(genres)
    		if randomly_picked_genre in genredict:
    			descriptor = random.choice(genredict[randomly_picked_genre])
    			return " I think this movie is %s!" % descriptor
    		return ""
    def get_quit_text(self):
    	rtn=""
        regexes1 = []
        regexes1.append("If you want more recs, just say 'yes'. Alternatively, you can tell me about more movies, or you can leave by writing ':quit'.")
        regexes1.append("Want another rec? Just say 'yes'. Or you can tell me about more movies, or type ':quit' and heartlessly abandon me, like all the others." )
        regexes1.append( "Type 'yes' for another recommendation, or ':quit' to, well, quit. Otherwise, you can tell me about more movies so I can make even better recommendations!" )
    	regexes1.append( "Please say 'yes' for another recommendation, tell me about more movies, or type ':quit' if you're done for now." )
    	regexes1.append( "You can type 'yes' for another great film rec, or ':quit' if you've already found the movie of your dreams. Alternatively, let me know your thoughts on another movie." )
    	regexes1.append( "Just type 'yes' for another great film rec, or ':quit' if you're good for now. Otherwise, talk to me about another movie." )

        rtn+= regexes1[random.randint(0, len(regexes1)-1)]
        return rtn
        
    def num_ambiguities(self, movietitle):
    	rtn=0
    	movietitle=movietitle.lower()
    	for title in self.titles:
    		if movietitle in title[0].lower():
    			rtn += 1
    		if rtn > 8:
    			return rtn
    	return rtn
    		
    def process(self, input):
      """Takes the input string from the REPL and call delegated functions
      that
        1) extract the relevant information and
        2) transform the information into a response to the user
      """
      #############################################################################
      # TODO: Implement the extraction and transformation in this method, possibly#
      # calling other functions. Although modular code is not graded, it is       #
      # highly recommended                                                        #
      #############################################################################
      lowercase_input = input.lower()
      if self.inRecMode and ("yes" in lowercase_input or "yep" in lowercase_input or "ok" in lowercase_input or "okay" in lowercase_input or "yeah" in lowercase_input or "fine" in lowercase_input or "sure" in lowercase_input or "yeah" in lowercase_input):
      	response= self.get_rec_text()

      	return response
     # if self.inRecMode:
     # 	response = self.get_quit_text()
     # 	self.goodbye()
     # 	return response
      matches = re.findall(r'\"(.+?)\"', input)
      if len(matches)==0:
      	input = self.findMovieWithoutQuotations(input)
      	matches = re.findall(r'\"(.+?)\"', input)
      if len(matches) == 0:
      	if self.inRecMode:
      		return self.get_quit_text()
      
      #CHRISTOPHER ADDED
      	response = self.arbitraryResponse(lowercase_input)
      	if response != -1:
      		return response
      	else:
      		return self.arbitraryEnd(lowercase_input)
      		
      		##############
      if len(matches) > 1:
      	response = self.get_single_movie_text()
      	return response
      
      if len(matches) == 1:
      	#if matches[0].lower().strip() == 'a' or matches[0].lower().strip() == 'an' or matches[0].lower().strip() == 'the':
      #		response = self.get_unknown_movie_text(matches[0])
      #		return response
      	check = self.checkmovie(matches[0])
      	#if check == -1:
      #		if self.startsWithArticle(matches[0]):
    #			print('cool')
   # 			check = self.checkmovie(self.deleteStartingArticle(matches[0]))  
    	#print "check below"
    	#print check    		
      	if check == -1:
      		if self.num_ambiguities(matches[0]) >8 or self.num_ambiguities(matches[0])==0:
      			#print self.num_ambiguities(matches[0])
      			response = self.get_unknown_movie_text(matches[0])
      		#elif num_ambiguities[]==1
      		else:
      			#print self.num_ambiguities(matches[0])
      			response = self.get_vague_movie_text(matches[0])
      		return response
      	#	num_ambiguities = self.num_ambiguities(matches[0])
      	#	if num_ambiguities==0:
      	#		response = 'Sorry, I don\'t know about %s. Can you tell me about some other movie?' %matches[0]
      	#	if num_ambiguities >9:
      	#		response = 'I know a ton of movies about %s. Can you be more specific?'%matches[0]
      	#	if num_ambiguities == 1:
      	#		response = 'I think you might have the title of %s wrong. Can you clarify or tell me about a different movie?'%matches[0]
      	#	else:
      	#		response = 'I know several movies that start with %s. Could you please be more specific?'%matches[0]
      	#	return response
      	if self.isInUserMovies(check):
      		response = self.get_old_movie_text(self.titles[check][0])
      		return response
      	score = self.detectSentiment(input)
      	if score > 0:
      		#response = random.choice([random.choice('You like %s! great!' % matches[0] 
      		self.user_movies.append([check,1])
      		response  = self.get_like_text(self.titles[check][0])
      		
      		if len(self.user_movies)>=5:
      			self.recs = self.recommendation(self.user_movies)
      			#print(user_movies)
      			response+= self.get_rec_text()
      			#response+= '. Try watching '+self.getRecTitle()+". Would you like another rec?"
      			self.inRecMode = True
      		else:
      			response+=self.get_prompt_text()
      		#'I liked watching %s too. Can you tell me about some more movies?' % matches[0]
      	elif score < 0:
      		self.user_movies.append([check,-1])
      		response = self.get_dislike_text(self.titles[check][0])
      		if len(self.user_movies)>=5:
      			self.recs = self.recommendation(self.user_movies)
      			response+=self.get_rec_text()
      			self.inRecMode = True
      		else:
      			response+=self.get_prompt_text()
      	else:
      		response = self.get_confused_sentiment_text(self.titles[check][0])
      	#response = 'You like %s?' % matches[0]
      	#hit = self.checkmovie(matches[0])
      	#print(hit)
      	return response
      	
      if self.is_turbo == True:
        response = 'processed %s in creative mode!!' % input
      else:
        response = 'processed %s in starter mode' % input

      return response

##################################OISHI CHANGES

    def get_vague_movie_text(self, movietitle):
    	rtn=""
    	regexes1 = []
    	regexes1.append('I know at least one movie that includes %s in its title, but I\'m not sure exactly what you\'re referring to. Could you be more specific?') 
    	regexes1.append('Huh, I know at least one film that has %s in the name, but I can\'t be certain precisely what you mean. Can you please be more specific?')
    	#regexes1.append('I recommend you try watching %s.')
    	#regexes1.append('Okay, try watching %s.')
    	#regexes1.append('I bet you would appreciate %s.')
    	#regexes1.append('Maybe you should try %s.')
    	regex1 = regexes1[random.randint(0,len(regexes1)-1)]
    	rtn+= regex1 % movietitle
    	return rtn
    	
    def get_rec_text(self):
    	rtn=""
    	regexes1 = []
    	regexes1.append('All right, you might like %s.') 
    	regexes1.append('I think you may enjoy %s.')
    	regexes1.append('I recommend you try watching %s.')
    	regexes1.append('Okay, try watching %s.')
    	regexes1.append('I bet you would appreciate %s.')
    	regexes1.append('Maybe you should try %s.')
    	regex1 = regexes1[random.randint(0,len(regexes1)-1)]
    	rtn+= regex1 % self.getRecTitle()
    	rtn+= self.genreResponse()
    	regexes2 = []
    	regexes2.append('Say "yes" if you would like another recommendation. Otherwise, you can tell me about more movies, or you can leave by saying ":quit".')
    	regexes2.append('Type "yes" if you want me to recommend another film. Alternatively, let me know your thoughts on other movies, or type ":quit" to leave.')
    #	regexes2.append('Do you want another rec (yes/no)?')
   ### 	regexes2.append('Should I find you another rec (yes/no)?')
    #	regexes2.append('Should I recommend another movie (yes/no)?')
   # 	regexes2.append('Would you care for another movie recommendation (yes/no)?')
    	regex2 = regexes2[random.randint(0,len(regexes2)-1)]
    	rtn+= ' '
    	rtn+=regex2
    	del self.recs[0]
    	return rtn

    def get_sorry_text(self):
        rtn=""
        regexes1 = []
        regexes1.append('Sorry, I don\'t understand.')
        regexes1.append( 'Um, I\'m confused.' )
        regexes1.append( 'Drat, I\'m confused.' )
        rtn+= regexes1[random.randint(0, len(regexes1)-1)]+" "
        regexes2=[]
        regexes2.append( 'Could you please tell me about a movie you\'ve seen?' )
        regexes2.append( 'Can you tell me about a movie you\'ve seen?' )
        regexes2.append( 'Would you mind telling me about a movie you\'ve seen?' )
        rtn+=regexes2[random.randint(0, len(regexes2)-1)]
        return rtn
    def get_unknown_movie_text(self, movietitle):
        rtn=""
        regexes1 = []
        regexes1.append('Sorry, can you tell me about a different movie? I unfortunately have not heard about %s.')
        regexes1.append( 'Hm, I have never heard of %s before. Maybe tell me about another movie?')
        regexes1.append( 'I don\'t know anything about %s. Can you please tell me about some other film?' )
        regexes1.append('Um, I actually don\'t know %s. How about you talk about a different movie?' )
        rtn+= regexes1[random.randint(0, len(regexes1)-1)]%movietitle
        return rtn
 
    def get_single_movie_text(self):
        rtn=""
        regexes1 = []
        regexes1.append('Sorry, can you just tell me about one movie at a time?')
        regexes1.append( 'Please tell me about just one movie at a time.')
        regexes1.append( 'Er, I\'m overwhelmed. Can you please tell me about just one movie?' )
        regexes1.append( 'Uh, I\'m rather easily confused. Can you please tell me about just one movie?' )

        rtn+= regexes1[random.randint(0, len(regexes1)-1)]
        return rtn
    def get_old_movie_text(self, movietitle):
        rtn=""
        regexes1 = []
        regexes1.append('Sorry, can you tell me about a new movie? I already heard about %s.')
        regexes1.append( 'Hm, I think I know enough about %s already. Maybe tell me about a new movie?')
        regexes1.append( 'I already heard what you think about %s. Can you please tell me about some other film?' )
        regexes1.append('Didn\'t you already tell me about %s? How about you talk about a different movie?' )
        rtn+= regexes1[random.randint(0, len(regexes1)-1)]%movietitle
        return rtn
    def get_prompt_text(self):
        rtn=""
        regexes2=[]
        regexes2.append( 'Can you please tell me about another film?' )
        regexes2.append( 'Please tell me about another movie.' )
        regexes2.append( 'Would you mind telling me about another movie?' )
        rtn+= regexes2[random.randint(0, len(regexes2)-1)]
        #print "rtn "+ rtn
        return rtn
    def get_like_text(self, movietitle):
        rtn=""
        regexes1 = []
        regexes1.append('Cool, you like %s.')
        regexes1.append( 'I\'m also a fan of %s.')
        regexes1.append( 'Ah, I liked %s too.' )
        regexes1.append( 'Yeah, I also thought %s was a good film. ' )
        regexes1.append( 'So you liked %s!' )
        rtn+= regexes1[random.randint(0, len(regexes1)-1)]%movietitle+' '
        return rtn
    def get_dislike_text(self, movietitle):
        rtn=""
        regexes1 = [] 
        regexes1.append('Oh, you didn\'t like %s.')
        regexes1.append('Yeah, I didn\'t love %s either.')
        regexes1.append('Ah, I also thought %s is kinda overrated. ')
        regexes1.append( 'Yeah, I agree %s wasn\'t all that great of film. ' )
        regexes1.append( 'So you disliked %s!' )
        rtn+= regexes1[random.randint(0, len(regexes1)-1)]%movietitle+' '
        return rtn
    def get_confused_sentiment_text(self, movietitle):
        rtn=""
        regexes1 = [] 
        regexes1.append('Er, I can\'t quite tell what you thought about %s. Did you like it or not?')
        regexes1.append('Hm. I\'m scratching my head right now, because I\'m having trouble figuring out how you feel about %s. Did you enjoy that movie, or not so much?')
        regexes1.append('Sorry, I don\'t really understand how you feel about this movie. Did you enjoy %s or not?')
        regexes1.append('Huh, you confused me. Do you care for %s or not?')
        regexes1.append('Hm, you lost me. Do you like %s or not?')
        rtn+= regexes1[random.randint(0, len(regexes1)-1)]%movietitle
        return rtn
        
############# CHRISTOPHER CHANGES BELOW


    def arbitraryResponse(self, userinput):
    	greeting_keywords = (
    	"hello", "hi", "hey","greetings", "sup", "what's up")
    	greeting_responses = (
    	"'sup?", "hey", "hi there","*nods*", "wassah do?")
    	profanity = (
    	"fuck", "bitch", "shit")
    	profanity_response = (
    	"I am unable to process such sinful words.",
    	"Why you swearin?")
    	howareyou_response = (
    	"I'm doing well in here, could you tell me about a movie you've seen?",
    	"I'm just chillin', can you describe to me a movie you've seen?",
    	"Could be better...do you know of any movies I can watch?")
    	who_responses = (
    	"whoooo?", "Youuu sound like an owl.")
    	what_responses = (
    	"You tell me.", 
    	"huh?", 
    	"hm, that's not really what I want to talk about. Let's talk about movies.")
    	whatis_responses = (
    	"You might find the answer on Wikipedia.", 
    	"I am not sure.",
    	"That is a deep question.",
    	"Beats me.",
    	"I dunno.")
    	when_responses = (
    	"Five years ago.", 
    	"I don't know. Everything comes to an end eventually.")
    	where_responses = (
    	"The moon?", 
    	"I am not sure where.")
    	why_responses = (
    	"Just because", 
    	"Why not?",
    	"You sure are a curious one.")
    	canyou_responses = (
    	"I'm not sure, can I?", 
    	"I sure can, if you tell me about a movie first.")
    	cani_responses = (
    	"You can do whatever you want if you put your mind into it.", 
    	"I don't think you can.", 
    	"You can't.",
    	"Good question.")
    	doyou_responses = (
    	"I most certainly do.",
    	"For sure.",
    	"Good question.")
    	doi_responses = (
    	"I don't know much about you",
    	"I don't think so.")
    	no_response = (
    	"c'mon now...",
    	"What if I said please?")
    	input = userinput.split()
    	for word in input:
    		if word in profanity:
    			return random.choice(profanity_response)
    	for word in input:
    		if word in greeting_keywords:
    			return random.choice(greeting_responses)
    	if len(input) > 1:
    		if input[0] + ' ' + input[1] == "what is":
    			return random.choice(whatis_responses)
    		if input[0] + ' ' + input[1] == "can you":
    			return random.choice(canyou_responses)
    		if input[0] + ' ' + input[1] == "can i":
    			return random.choice(cani_responses)
    		if input[0] + ' ' + input[1] == "do you":
    			return random.choice(doyou_responses)
    		if input[0] + ' ' + input[1] == "do i":
    			return random.choice(doi_responses)
    	if input[0] == "no":
    		return random.choice(no_response)
    	if userinput == "how are you?" or userinput == "how are you":
    		return random.choice(howareyou_response)
    	if input[0] == "who":
    		return random.choice(who_responses)
    	if input[0] == "what" or input[0] == "what's":
    		return random.choice(what_responses)
    	if input[0] == "when":
    		return random.choice(when_responses)
    	if input[0] == "where":
    		return random.choice(where_responses)
    	if input[0] == "why":
    		return random.choice(why_responses)
    	
    		
    	return -1
    	
    	
    def arbitraryEnd(self, userinput):
    	end = ("ok...how about we change the topic to a film you've watched.",
    	"Hm.. sorry to change the topic, but can you tell me about a movie you've seen?",
    	"Ok, got it.",
    	"I'm not sure what you meant.",
    	"I'd prefer we talk about movies, could you tell me about one?",
    	"Would you mind telling me about a movie you've seen?",
    	"Sorry. I don't understand. Please tell me about a movie that you've seen.")
    	return random.choice(end)

    #############################################################################
    # 3. Movie Recommendation helper functions                                  #
    #############################################################################

    def getTitleWords(self):
    	self.titleWords=set()
    	for item in self.titles[0:len(self.titles)-1]:
    		titles = item[0]
    		for word in titles.split():
    			if word != "the" and word != "a" and word != "an" and word != "'l" and word != "la" and word != "le":
    				if word[-1]==',':
    					word = word[:len(word)-1]
    				self.titleWords.add(word.lower())
    def read_data(self):
      """Reads the ratings matrix from file"""
      # This matrix has the following shape: num_movies x num_users
      # The values stored in each row i and column j is the rating for
      # movie i by user j
      self.titles, self.ratings = ratings()
      self.getTitleWords()
      
      #print self.titles
      self.binarize()
      	
      #print(len(self.titles))
      #print(len(self.ratings))
      reader = csv.reader(open('data/sentiment.txt', 'rb'))
      self.sentiment = dict(reader)
      
      #rating = csv.reader(open('data/ratings.txt', 'rb'))
      #self.rating = dict(rating)
      
      self.stemmedSentiment = {}
      for word in self.sentiment:
      	#self.stemmedSentiment.append(word,self.sentiment[word])
      	self.stemmedSentiment[self.fullStem(word)]=self.sentiment[word]
      	self.stemmedSentiment[self.fullStem("awesome")]='pos'
      del self.stemmedSentiment['thought']

      	
      
      #print self.stemmedSentiment


    def binarize(self):
    	#print self.ratings
    	#print self.ratings[1]
    	self.ratings[numpy.where(self.ratings > 2.5)] = -2  ## everything 3 and above is 1
    	self.ratings[numpy.where(self.ratings >= 0.5)] = -1 ## everything above 0 and below 3 is -1
    	self.ratings[numpy.where(self.ratings == -2)] = 1
    	#print self.ratings[1]
    	#print len(self.ratings)
    	#for user_index in range (0, len(self.ratings)):
    	#	for ratings_index in range(0, len(self.ratings[user_index])):
    	#		if self.ratings[user_index][ratings_index] >=3:
    	#			self.ratings[user_index][ratings_index]=1.0
    	#		elif self.ratings[user_index][ratings_index] >0:
    	#			self.ratings[user_index][ratings_index]=-1.0
    	#print self.ratings[1]
    	#print len(self.ratings)


    def distance(self, u, v):
      """Calculates a given distance function between vectors u and v"""
      # TODO: Implement the distance function between vectors u and v]
      # Note: you can also think of this as computing a similarity measure

      pass


    def recommend(self, u):
      """Generates a list of movies based on the input vector u using
      collaborative filtering"""
      # TODO: Implement a recommendation function that takes a user vector u
      # and outputs a list of movies recommended by the chatbot

      pass


    #############################################################################
    # 4. Debug info                                                             #
    #############################################################################

    def debug(self, input):
      """Returns debug information as a string for the input string from the REPL"""
      # Pass the debug information that you may think is important for your
      # evaluators
      debug_info = 'debug info'
      return debug_info


    #############################################################################
    # 5. Write a description for your chatbot here!                             #
    #############################################################################
    def intro(self):
      return """
      Hi, I'm Just a Rather Very Intelligent System, or Jarvis for short (dear Marvel, please do not sue me). Talk to me about movies you've seen, and I'll recommend more films you might enjoy! I'd prefer that you set off movie titles with quotation marks, but I can also try and read titles without marks, provided that you spell correctly, capitalize the first word, and don't add extraneous punctuation. Moreover, I am able to perform fine-grained sentiment extraction (i.e.- read your emotions better than a computer of average intelligence). I can also deal with misspellings in movie titles, prompt you to be more specific if you refer to movies vaguely, guide you back to the topic at hand if your mind should wander, identify movies by alternate titles, and describe the movies that I recommend, to explain why one might enjoy them.
      """


    #############################################################################
    # Auxiliary methods for the chatbot.                                        #
    #                                                                           #
    # DO NOT CHANGE THE CODE BELOW!                                             #
    #                                                                           #
    #############################################################################

    def bot_name(self):
      return self.name


#!/usr/bin/env python




#class PorterStemmer:

    #def __init__(self):


        #self.b = ""  # buffer for word to be stemmed
        #self.k = 0
        #self.k0 = 0
        #self.j = 0   # j is a general offset into the string

    def cons(self, i):
        """cons(i) is TRUE <=> b[i] is a consonant."""
        if self.b[i] == 'a' or self.b[i] == 'e' or self.b[i] == 'i' or self.b[i] == 'o' or self.b[i] == 'u':
            return 0
        if self.b[i] == 'y':
            if i == self.k0:
                return 1
            else:
                return (not self.cons(i - 1))
        return 1

    def m(self):
        """m() measures the number of consonant sequences between k0 and j.
        if c is a consonant sequence and v a vowel sequence, and <..>
        indicates arbitrary presence,

           <c><v>       gives 0
           <c>vc<v>     gives 1
           <c>vcvc<v>   gives 2
           <c>vcvcvc<v> gives 3
           ....
        """
        n = 0
        i = self.k0
        while 1:
            if i > self.j:
                return n
            if not self.cons(i):
                break
            i = i + 1
        i = i + 1
        while 1:
            while 1:
                if i > self.j:
                    return n
                if self.cons(i):
                    break
                i = i + 1
            i = i + 1
            n = n + 1
            while 1:
                if i > self.j:
                    return n
                if not self.cons(i):
                    break
                i = i + 1
            i = i + 1

    def vowelinstem(self):
        """vowelinstem() is TRUE <=> k0,...j contains a vowel"""
        for i in range(self.k0, self.j + 1):
            if not self.cons(i):
                return 1
        return 0

    def doublec(self, j):
        """doublec(j) is TRUE <=> j,(j-1) contain a double consonant."""
        if j < (self.k0 + 1):
            return 0
        if (self.b[j] != self.b[j-1]):
            return 0
        return self.cons(j)

    def cvc(self, i):
        """cvc(i) is TRUE <=> i-2,i-1,i has the form consonant - vowel - consonant
        and also if the second c is not w,x or y. this is used when trying to
        restore an e at the end of a short  e.g.

           cav(e), lov(e), hop(e), crim(e), but
           snow, box, tray.
        """
        if i < (self.k0 + 2) or not self.cons(i) or self.cons(i-1) or not self.cons(i-2):
            return 0
        ch = self.b[i]
        if ch == 'w' or ch == 'x' or ch == 'y':
            return 0
        return 1

    def ends(self, s):
        """ends(s) is TRUE <=> k0,...k ends with the string s."""
        length = len(s)
        if s[length - 1] != self.b[self.k]: # tiny speed-up
            return 0
        if length > (self.k - self.k0 + 1):
            return 0
        if self.b[self.k-length+1:self.k+1] != s:
            return 0
        self.j = self.k - length
        return 1

    def setto(self, s):
        """setto(s) sets (j+1),...k to the characters in the string s, readjusting k."""
        length = len(s)
        self.b = self.b[:self.j+1] + s + self.b[self.j+length+1:]
        self.k = self.j + length

    def r(self, s):
        """r(s) is used further down."""
        if self.m() > 0:
            self.setto(s)

    def step1ab(self):
        """step1ab() gets rid of plurals and -ed or -ing. e.g.

           caresses  ->  caress
           ponies    ->  poni
           ties      ->  ti
           caress    ->  caress
           cats      ->  cat

           feed      ->  feed
           agreed    ->  agree
           disabled  ->  disable

           matting   ->  mat
           mating    ->  mate
           meeting   ->  meet
           milling   ->  mill
           messing   ->  mess

           meetings  ->  meet
        """
        if self.b[self.k] == 's':
            if self.ends("sses"):
                self.k = self.k - 2
            elif self.ends("ies"):
                self.setto("i")
            elif self.b[self.k - 1] != 's':
                self.k = self.k - 1
        if self.ends("eed"):
            if self.m() > 0:
                self.k = self.k - 1
        elif (self.ends("ed") or self.ends("ing")) and self.vowelinstem():
            self.k = self.j
            if self.ends("at"):   self.setto("ate")
            elif self.ends("bl"): self.setto("ble")
            elif self.ends("iz"): self.setto("ize")
            elif self.doublec(self.k):
                self.k = self.k - 1
                ch = self.b[self.k]
                if ch == 'l' or ch == 's' or ch == 'z':
                    self.k = self.k + 1
            elif (self.m() == 1 and self.cvc(self.k)):
                self.setto("e")

    def step1c(self):
        """step1c() turns terminal y to i when there is another vowel in the stem."""
        if (self.ends("y") and self.vowelinstem()):
            self.b = self.b[:self.k] + 'i' + self.b[self.k+1:]

    def step2(self):
        """step2() maps double suffices to single ones.
        so -ization ( = -ize plus -ation) maps to -ize etc. note that the
        string before the suffix must give m() > 0.
        """
        if self.b[self.k - 1] == 'a':
            if self.ends("ational"):   self.r("ate")
            elif self.ends("tional"):  self.r("tion")
        elif self.b[self.k - 1] == 'c':
            if self.ends("enci"):      self.r("ence")
            elif self.ends("anci"):    self.r("ance")
        elif self.b[self.k - 1] == 'e':
            if self.ends("izer"):      self.r("ize")
        elif self.b[self.k - 1] == 'l':
            if self.ends("bli"):       self.r("ble") # --DEPARTURE--
            # To match the published algorithm, replace this phrase with
            #   if self.ends("abli"):      self.r("able")
            elif self.ends("alli"):    self.r("al")
            elif self.ends("entli"):   self.r("ent")
            elif self.ends("eli"):     self.r("e")
            elif self.ends("ousli"):   self.r("ous")
        elif self.b[self.k - 1] == 'o':
            if self.ends("ization"):   self.r("ize")
            elif self.ends("ation"):   self.r("ate")
            elif self.ends("ator"):    self.r("ate")
        elif self.b[self.k - 1] == 's':
            if self.ends("alism"):     self.r("al")
            elif self.ends("iveness"): self.r("ive")
            elif self.ends("fulness"): self.r("ful")
            elif self.ends("ousness"): self.r("ous")
        elif self.b[self.k - 1] == 't':
            if self.ends("aliti"):     self.r("al")
            elif self.ends("iviti"):   self.r("ive")
            elif self.ends("biliti"):  self.r("ble")
        elif self.b[self.k - 1] == 'g': # --DEPARTURE--
            if self.ends("logi"):      self.r("log")
        # To match the published algorithm, delete this phrase

    def step3(self):
        """step3() dels with -ic-, -full, -ness etc. similar strategy to step2."""
        if self.b[self.k] == 'e':
            if self.ends("icate"):     self.r("ic")
            elif self.ends("ative"):   self.r("")
            elif self.ends("alize"):   self.r("al")
        elif self.b[self.k] == 'i':
            if self.ends("iciti"):     self.r("ic")
        elif self.b[self.k] == 'l':
            if self.ends("ical"):      self.r("ic")
            elif self.ends("ful"):     self.r("")
        elif self.b[self.k] == 's':
            if self.ends("ness"):      self.r("")

    def step4(self):
        """step4() takes off -ant, -ence etc., in context <c>vcvc<v>."""
        if self.b[self.k - 1] == 'a':
            if self.ends("al"): pass
            else: return
        elif self.b[self.k - 1] == 'c':
            if self.ends("ance"): pass
            elif self.ends("ence"): pass
            else: return
        elif self.b[self.k - 1] == 'e':
            if self.ends("er"): pass
            else: return
        elif self.b[self.k - 1] == 'i':
            if self.ends("ic"): pass
            else: return
        elif self.b[self.k - 1] == 'l':
            if self.ends("able"): pass
            elif self.ends("ible"): pass
            else: return
        elif self.b[self.k - 1] == 'n':
            if self.ends("ant"): pass
            elif self.ends("ement"): pass
            elif self.ends("ment"): pass
            elif self.ends("ent"): pass
            else: return
        elif self.b[self.k - 1] == 'o':
            if self.ends("ion") and (self.b[self.j] == 's' or self.b[self.j] == 't'): pass
            elif self.ends("ou"): pass
            # takes care of -ous
            else: return
        elif self.b[self.k - 1] == 's':
            if self.ends("ism"): pass
            else: return
        elif self.b[self.k - 1] == 't':
            if self.ends("ate"): pass
            elif self.ends("iti"): pass
            else: return
        elif self.b[self.k - 1] == 'u':
            if self.ends("ous"): pass
            else: return
        elif self.b[self.k - 1] == 'v':
            if self.ends("ive"): pass
            else: return
        elif self.b[self.k - 1] == 'z':
            if self.ends("ize"): pass
            else: return
        else:
            return
        if self.m() > 1:
            self.k = self.j

    def step5(self):
        """step5() removes a final -e if m() > 1, and changes -ll to -l if
        m() > 1.
        """
        self.j = self.k
        if self.b[self.k] == 'e':
            a = self.m()
            if a > 1 or (a == 1 and not self.cvc(self.k-1)):
                self.k = self.k - 1
        if self.b[self.k] == 'l' and self.doublec(self.k) and self.m() > 1:
            self.k = self.k -1

    def stem(self, p, i=None, j=None):
        """In stem(p,i,j), p is a char pointer, and the string to be stemmed
        is from p[i] to p[j] inclusive. Typically i is zero and j is the
        offset to the last character of a string, (p[j+1] == '\0'). The
        stemmer adjusts the characters p[i] ... p[j] and returns the new
        end-point of the string, k. Stemming never increases word length, so
        i <= k <= j. To turn the stemmer into a module, declare 'stem' as
        extern, and delete the remainder of this file.
        """
        if i is None:
            i = 0
        if j is None:
            j = len(p) - 1
        # copy the parameters into statics
        self.b = p
        self.k = j
        self.k0 = i
        if self.k <= self.k0 + 1:
            return self.b # --DEPARTURE--

        # With this line, strings of length 1 or 2 don't go through the
        # stemming process, although no mention is made of this in the
        # published algorithm. Remove the line to match the published
        # algorithm.

        self.step1ab()
        self.step1c()
        self.step2()
        self.step3()
        self.step4()
        self.step5()
        return self.b[self.k0:self.k+1]
if __name__ == '__main__':
    Chatbot()


