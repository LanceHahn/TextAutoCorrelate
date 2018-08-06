import argparse
from datetime import datetime
import sys
#import time


import nltk
# dependent on nltk



def GetArgs():
## This subroutine acquire the command line parameters passed by the user.
# args = GetArgs()

    Arg_Parser = argparse.ArgumentParser(description='Learn what word sequences are in one of two classes (0 or 1).\n A sample data entry= roses are red , pick red 0 1 <pattern><class0><class1>\n LSTM with words  embedded in word vector space and the vectors are fed to the nn.')


## Word representation space

    Arg_Parser.add_argument('--DocFile', type=str, default='/Users/lance/Documents/Personal/Advent/TextAutoCor/testDoc.txt',
                        help='text file name - text file of words')

    Arg_Parser.add_argument('--verbose', type=int, default=74,
                            help='level of descriptive text genrated [0-100]')

    Arg_Parser.add_argument('--tolerance', type=int, default=74,
                            help='level variance allowed for a match (NOT YET IMPLEMENTED)')
                            
    Arg_Parser.add_argument('--frequencyThreshold', type=int, default=2,
                            help='how frequent must an n-gram be in order to be reported')

    args = Arg_Parser.parse_args() # interpet the current command line flags

    return ( args )


def CommonLength( CompleteTokenList, StartingLocation, CandidateMatches):
# Find the longest string match that begins at StartingLocation in CompleteTokenList and the strings that start at the
# locations in CompleteTokenList that are listed in CandidateMatches.

    CurrentOffset = 0
    WordsInDoc=len(tokens)
    LongestMatch = 1
    LongestMatchLocation = CandidateMatches[0]

    for CandidateLocation in CandidateMatches: # Step through all of the locations where this n-gram is present
        if ( CandidateLocation < StartingLocation):
            Shortest_Length = min(WordsInDoc-CandidateLocation, WordsInDoc-StartingLocation)

            while (CurrentOffset < Shortest_Length) and ( CompleteTokenList[CandidateLocation+ CurrentOffset] == CompleteTokenList[StartingLocation+CurrentOffset]) :
                CurrentOffset = CurrentOffset+1
        
            if ( CurrentOffset > LongestMatch): # is this a new longest match? If so, update the record-keeping
                LongestMatch = CurrentOffset
                LongestMatchLocation = CandidateLocation

    return ( LongestMatchLocation, LongestMatch )
#

def Print_AC_Thresholded (Matrix, frequencyThreshold ):

    print ("n-gram tokens,frequency")
    for CompIndex in range ( len(Matrix) ):
        if ( Matrix[CompIndex][2]>= frequencyThreshold ):
            print ("\"",end="")
            for ngram_i in range (Matrix[CompIndex][3]):
                print (Matrix[CompIndex][0][ngram_i], end="")
                if ( ngram_i < Matrix[CompIndex][3]-1 ):
                    print (" ",end="")
            print ("\",",Matrix[CompIndex][2])


def Print_AC (Matrix ):

    print ("\n[n-gram tokens],[locations],frequency,n-gram length")
    for CompIndex in range ( len(Matrix) ):
        print ( Matrix[CompIndex][0],",",Matrix[CompIndex][1],",",Matrix[CompIndex][2],",",Matrix[CompIndex][3]  )



def AutoCorrelateDocument( tokens, tolerance ):

    Verb = 0
    #tokens = nltk.word_tokenize( document_text )

    WordsInDoc=len(tokens)
    AC_Matrix = [ [] ]
    # a list of unique n-grams
    # 0. the n-gram
    # 1. list of locations in the document
    # 2. the frequency in the document (so far)
    # 3. length of the n-gram ( len( AC_Matrix[X][0] ))

    ## Sort by UNI-gram frequency (element 2) highest to lowest and alphabetize n-gram as second key (a..z]
    # "what will be will be"
    #  ->
    # "will",[1,3],2,1
    # "will be",[1,3],2,2
    # "be",[2,4],2,1
    # "what",[0],1,1
    
    AC_Matrix[ 0 ] = [ [tokens[0]],[0],1,1 ] # initial word, location, frequency, length, next unigram location
    for Ind in range(len(tokens)-1):

        if ( Verb > 50 ):
            print (" begin for Ind loop")
            Print_AC(AC_Matrix)
        
        CurrentInd = Ind +1
        Common_Length = 1
        if ( Verb > 50 ):
            print ( "Assessing #",CurrentInd,":", tokens[ CurrentInd] )
        Integrated = 0
        for CompIndex in range ( len(AC_Matrix) ): # search existing n-grams for match
            if ( Verb > 65 ):
                print ( tokens[ CurrentInd ] ,"?=? ", AC_Matrix[ CompIndex][0][0] )

            if ( tokens[ CurrentInd ] == AC_Matrix[ CompIndex][0][0] ): # n-gram first word match
                if ( Verb > 50 ):
                    print ( "tokens[",CurrentInd,"]=", tokens[ CurrentInd ] ,"matches ", AC_Matrix[ CompIndex][0] )
                    print ( AC_Matrix[ CompIndex][1],"AC_Matrix[ CompIndex][1].count(",CurrentInd,") =  ",AC_Matrix[ CompIndex][1].count(CurrentInd))
                
                if (  AC_Matrix[ CompIndex][1].count(CurrentInd) == 0 ): # if location missing
                    InitialLocation, Common_Length = CommonLength( tokens, CurrentInd, AC_Matrix[CompIndex][1] ) # check full length of match at location
                    if ( Verb > 50 ):
                        print ( Common_Length,"?==?", AC_Matrix[ CompIndex][3], "::",AC_Matrix[ CompIndex]) # length match
                    if ( Common_Length == AC_Matrix[ CompIndex][3] ): # length match
                        AC_Matrix[ CompIndex][2] += 1                # increment frequency of matched existing ngram
                        AC_Matrix[ CompIndex][1].append( CurrentInd) # add new location to location list
                        Integrated = 1
                        if ( Verb > 50 ):
                            print ( " updated by inc and append ",CurrentInd,",", AC_Matrix[ CompIndex] )
    

                    else: # match was longer than the registered ngram currently under consideration
                        # Does the longer match already exist in the matrix?

                        if ( Verb > 50 ):
                            print ("# Does the longer match already exist in the matrix?")
                        #for StoredIndex in range ( CompIndex, len(AC_Matrix) - CompIndex ):
                        for StoredIndex in range ( CompIndex, len(AC_Matrix) ):
                            if ( Verb > 50 ):
                                print ( Common_Length,"?==?", AC_Matrix[ CompIndex][3], ":::",AC_Matrix[ CompIndex]) # length match
                            if (  Common_Length == AC_Matrix[StoredIndex][3] ): # match on ngram length
                                if ( Verb > 50 ):
                                    print ( "Common_Length",Common_Length,"]=", AC_Matrix[StoredIndex][3] ,"matches ", AC_Matrix[ StoredIndex][3] )
                                    print ( tokens[CurrentInd:CurrentInd+Common_Length] ,"?===?", AC_Matrix[StoredIndex][0] )
                                if ( tokens[CurrentInd:CurrentInd+Common_Length] == AC_Matrix[StoredIndex][0]): # exact string match
                                    if ( Verb > 50 ):
                                        print ( tokens[CurrentInd:CurrentInd+Common_Length] ,"=yes=", AC_Matrix[StoredIndex][0] )

                                    AC_Matrix[StoredIndex][2] += 1
                                    Integrated = 1
                                    AC_Matrix[ StoredIndex][1].append( CurrentInd) # add new location to location list
                                    break
                        if ( Integrated == 0 ):
                            AC_Matrix.insert( 1+CompIndex , [tokens[CurrentInd:CurrentInd+Common_Length],[InitialLocation,CurrentInd],2,Common_Length] ) # add new long n-gram
                            Integrated = 1
                            # update unigram info
                            AC_Matrix[ CompIndex][2] += 1                # increment frequency of matched existing unigram
                            AC_Matrix[ CompIndex][1].append( CurrentInd) # add new location to the unigram location list
                            break # end search for this longer n-gram
        if Integrated == 0: # new n-gram not found in AC matrix
            AC_Matrix.append( [tokens[CurrentInd:CurrentInd+Common_Length],[CurrentInd],1,Common_Length] )

    return ( AC_Matrix )

## Main

CommandArgs = GetArgs()

print ( "Program begins at ", str(datetime.now()) )
print ("Program called with the arguments:")
print (sys.argv)
print ("Program arguments and defaults were interpeted as:")
print (CommandArgs)

tokens=[]
for line in open( CommandArgs.DocFile ):
    tokens+=nltk.word_tokenize( line )

Historgram = AutoCorrelateDocument( tokens, 0)


print ("N-grams occuring in %s at least %i times." % (CommandArgs.DocFile,  CommandArgs.frequencyThreshold))
Print_AC_Thresholded(Historgram,CommandArgs.frequencyThreshold)

print ( "Program ends at ", str(datetime.now()) )
