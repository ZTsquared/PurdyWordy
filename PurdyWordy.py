# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string

#VOWELS = 'aeiou'
#CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
ALPHABET = "abcdefghijklmnopqrstuvwxyz*"
VOWELS = 'aaaaaaaaaeeeeeeeeeeeeiiiiiiiiioooooooouuuu'
INDIVIDUAL_VOWELS = 'aeiou'
CONSONANTS = 'bbccddddffggghhjkllllmmnnnnnnppqrrrrrrssssttttttvvwwxyyz'
INDIVIDUAL_CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7
EMPTY_HAND = {"Oops, sorry, I haven't dealt your hand yet!":1}

SCRABBLE_LETTER_VALUES = {
    '*': 0,'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

SPECIAL_CHARACTERS = ["?", "...", "*", "#", "%", "!", "!!", "&"]


# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, hand):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    
    word = word.lower()
    letter_point_score = 0
    hand_length = calculate_handlen(hand)
    hand_count_score = 7*len(word) - 3*(hand_length - len(word))
    if hand_count_score < 1:
        hand_count_score = 1
    if len(word) == 0:
        hand_count_score = 0
        
    temp_hand = hand.copy()
    for char in word:
        if temp_hand.get(char, 0) > 0:
            letter_point_score += SCRABBLE_LETTER_VALUES[char]
            temp_hand[char] = temp_hand.get(char, 0) - 1
        elif temp_hand.get("*", 0) > 0:
            temp_hand["*"] = temp_hand.get("*", 0) - 1
        else:
            print(f"SOMETHING IS WRONG - THE WORD BEING SCORED CONTAINS A '{char}' THAT IS NOT IN THE HAND")
        
        #if temp_hand.get(char, 0) < 1 and temp_hand.get("*", 0) > 0:
            #temp_hand["*"] = temp_hand.get("*", 0) - 1
        #else:
            #letter_point_score += SCRABBLE_LETTER_VALUES[char]
            #temp_hand[char] = temp_hand.get(char, 0) - 1
        
    word_score = letter_point_score * hand_count_score
    assert word_score >= 0, "scoring calculation error: score below zero"
    assert len(word) == 0 or word_score > 0, "scoring calculation error: valid word achieved zero score"
    return word_score


#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    print()
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()  
    print()                             # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))
    temp_vowels = VOWELS
    temp_consonants = CONSONANTS
    for i in range(num_vowels):
        x = random.choice(temp_vowels)
        hand[x] = hand.get(x, 0) + 1
        temp_vowels = temp_vowels.replace(x, "", 1)
    
    hand["*"] = 1
    
    for i in range(num_vowels + 1, n):    
        x = random.choice(temp_consonants)
        hand[x] = hand.get(x, 0) + 1
        temp_consonants = temp_consonants.replace(x, "", 1)
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """

#for each letter in the word remove one count of that letter
 #from the dictionary but only if the count 
 #of that letter is currently greater than 0
 
    new_hand = hand.copy()
    word = word.lower()
    for char in word:
        if char in new_hand and new_hand[char] > 0:    
            new_hand[char] = new_hand.get(char) - 1
        else:
            new_hand["*"] = new_hand.get("*") - 1
    letter_counts = new_hand.values()
    for i in letter_counts:
        assert i >= 0, "hand update error: hand contains negative values: {hand}"
    return new_hand

        
def clean_up_word(unvalidated_word, hand):
    #print("function entered - unvalidated word:" + unvalidated_word)
    word = unvalidated_word.lower()
    #print("function entered - word:" + word)
    invalid_characters = {" ", "!", "", "#", "$", "~", "%", "€",
                          "&", "/", "(", ")", "=", "?", "¿", "'",
                          "¡", "^", "´", "ç", "ñ", "¨", "´",
                          ">", "<", ";", ",", ":", ".", "_", "-",
                          "1", "2", "3", "4", "5", "6", "7", "8", "9"}
    set_of_characters_in_word = set(list(word))
    #print(set_of_characters_in_word.intersection(invalid_characters))
    while len(set_of_characters_in_word.intersection(invalid_characters)) != 0:
        without_leading_spaces = word
        original_word = word
        #print("Without leading spaces:" + without_leading_spaces)
        #print(without_leading_spaces[0] == " ")
        #print(len(without_leading_spaces))
        #print(len(without_leading_spaces) > 0)
        
        while len(without_leading_spaces) > 0 and without_leading_spaces[0] == " ":
            without_leading_spaces = without_leading_spaces.replace(" ", "", 1)
            #print("Without leading spaces:" + without_leading_spaces)
            #print (without_leading_spaces)    
        while len(set_of_characters_in_word.intersection(invalid_characters)) != 0:
            word = word.replace("ç","c")
            word = word.replace("ñ","n")
            for char in invalid_characters:
                word = word.replace(char,"") 
            set_of_characters_in_word = set(list(word))
            #print(set_of_characters_in_word.intersection(invalid_characters))3452
            #print("function running - unvalidated word:" + unvalidated_word)
            #print("function running - word:" + word)
            #print(len(word) > 0)
            #print(word == without_leading_spaces)
            #print(original_word != without_leading_spaces)
        if len(word) > 0 and original_word != without_leading_spaces and word == without_leading_spaces:
            break
            #print ("length of word:" + str(len(word)))
            #print(len(word) != 0)
        if len(word) != 0:
            verified_with_user = input(f"Did you mean '{word}'? If so, press enter. If not, re-enter your word:")
            verified_with_user = call_special_character(hand, verified_with_user, "What word would you like to play?")[0]
            if verified_with_user == "":
                verified_with_user = word
            word = verified_with_user.lower()
            #print("function running - verified with user:" + verified_with_user)
        
        while len(word) == 0:
            verified_with_user = input("How are you going to get any points if you don't play any letters? Try again:")
            verified_with_user = call_special_character(hand, verified_with_user, "What word would you like to play?")[0]
            word = verified_with_user.lower()
            #print("function running - verified with user:" + verified_with_user)
        if word == "!!":
            break
        set_of_characters_in_word = set(list(word))
        #print(set_of_characters_in_word.intersection(invalid_characters))
            
        #print("function loop restart - unvalidated word:" + unvalidated_word)
        #print("function loop restart - word:" + word)
        
    #print("function run - unvalidated word:" + unvalidated_word)
    #print("function run - word:" + word)
    
        
            
    return word


#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    

    """
    assert word not in SPECIAL_CHARACTERS, f"Special character '{word}' entered is_valid_word process"
    word = word.lower()
    wildcard_word = "placeholder_word"
    if word in word_list:
        is_valid = True
    elif len(word) <= 1:
        is_valid = False
        print ("Words must have at least 2 letters.")
    elif word not in word_list and "*" in word:
        is_valid = False
        for char in (INDIVIDUAL_VOWELS + INDIVIDUAL_CONSONANTS):
            wildcard_word = word.replace("*", char)
            if wildcard_word in word_list:
                print (f"I found the word '{wildcard_word}' for you in my dictionary")
                is_valid = True
                break
        if not is_valid:
            print ("Nice try but there is no letter in the alphabet that will turn that into a real word.")
    else:
        is_valid = False
        print ("That word is not in our dictionary.")

    if is_valid == True and wildcard_word in word_list:
        conjunction = "BUT..."
    elif is_valid == False:
        conjunction = "AND..."
    else:
        conjunction = ""


    #test print statement below, uncomment when running test
    #print(f"word in word list: {is_valid}")
    
    letters_in_word = {}
    temp_hand = hand.copy()
    #test print statement below, uncomment when running test
    #print(f"original temp hand dictionary: {temp_hand}")
    for char in word:
        if temp_hand.get(char, 0) < 1 and temp_hand.get("*", 0) > 0:
            letters_in_word["*"] = letters_in_word.get("*", 0) + 1
            temp_hand["*"] = temp_hand.get("*", 0) - 1
        else:
            letters_in_word[char] = letters_in_word.get(char, 0) + 1
            temp_hand[char] = temp_hand.get(char, 0) - 1
    #test print statements (2) below, uncomment when running test
    #print(f"letters in word dictionary: {letters_in_word}")
    #print(f"updated temp hand dictionary: {temp_hand}")
    for char in letters_in_word:
        if char not in hand:
            is_valid = False
            print(conjunction + "The letters in your hand are insufficient to form this word.")
            break
        elif letters_in_word[char] > hand[char]:
            is_valid = False
            print(conjunction + "The letters in your hand are insufficient to form this word.")
            break
    return is_valid

    
    
#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    
    return sum(hand.values())    


def calculate_letter_points(hand):
    """ 
    Returns the sum of the point values of all letters in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    
    total_letter_points = 0
    for letter in hand:
        letter_points = SCRABBLE_LETTER_VALUES[letter] * hand[letter]
        total_letter_points += letter_points
        
    return total_letter_points 


def remove_duplicates(original_list):
    """ 
    Returns a new list which inculdes all unique values from the original list
    with no duplicates.
    
    original_list: list
    returns: list
    """

    no_duplicates = original_list.copy()
    #print (f"original_list {original_list}")
    for word in original_list:
        temp_list = no_duplicates.copy()
        temp_list.remove(word)
        if word in temp_list:
            no_duplicates.remove(word)
    #print(no_duplicates)
    
    return no_duplicates
        

def can_form_word(hand, word):
    """ 
    checks if a word can be formed from the list of letters in the hand
    
    hand: dictionary {individual letter string: quantitie,}
    word: string
    returns: True False Boolean
    """
    
    word = word.lower()
    letters_are_sufficient = True
    
    letters_in_valid_word = {}
    temp_hand = hand.copy()
    #test print statement below, uncomment when running test
    #print(f"original temp hand dictionary: {temp_hand}")
    for char in word:
        if temp_hand.get(char, 0) >= 1:
            letters_in_valid_word[char] = letters_in_valid_word.get(char, 0) + 1
            temp_hand[char] = temp_hand.get(char, 0) - 1
        elif temp_hand.get("*", 0) > 0:
            letters_in_valid_word["*"] = letters_in_valid_word.get("*", 0) + 1
            temp_hand["*"] = temp_hand.get("*", 0) - 1   
        else:
            letters_are_sufficient = False
            break
    letters_in_word = {}
    for char in word:
        letters_in_word[char] = letters_in_word.get(char, 0) + 1
    #print(letters_in_valid_word)
    #print(letters_in_word)
            
    #test print statements (2) below, uncomment when running test
    #print(f"letters in word dictionary: {letters_in_word}")
    #print(f"updated temp hand dictionary: {temp_hand}")

    return (letters_are_sufficient, letters_in_word)



def find_all_valid_words_in_hand(hand, word_list):
    
    """ 
    checks all possible combinations of letters from the hand against 
    the word list to produce a list of all the valid words that can be 
    formed from the hand. Words are separated into lists by size 
    from 2 to hand_size, within which they are alphabetical
    
    hand: list of individual letter strings
    word list: list of strings
    returns: list of lists of strings
    """


    all_valid_words_in_hand = []
    for word in word_list:
        letters_are_sufficient = can_form_word(hand, word)[0]
        letters_in_word = can_form_word(hand, word)[1]
        
        if letters_are_sufficient:
            for char in letters_in_word:
                if letters_in_word.get(char, 0) > hand.get(char, 0):
                    quantity_to_replace = letters_in_word.get(char, 0) - hand.get(char, 0)
                    word = word.replace(char, "*", quantity_to_replace)
            all_valid_words_in_hand.append(word)
            
    all_valid_words_in_hand = remove_duplicates(all_valid_words_in_hand)
            
    return all_valid_words_in_hand





def display_all_valid_words_in_hand(hand, word_list):
    
    hand_length =  calculate_handlen(hand)
    
    print("Searching for valid words in your hand...")
    print()
    
    all_valid_words_in_hand = find_all_valid_words_in_hand(hand, word_list)
    for n in range (2, hand_length + 1):
        n_length_words = []
        for word in all_valid_words_in_hand:
            if len(word) == n:
                n_length_words.append(word + ", ")
        if len(n_length_words) == 0:
            print(f"No valid {n} letter words can be formed with the letters in your hand")
        else:
            print(f"The following {n} letter words can be formed with the letters in your hand:")
            print(*n_length_words,)
            print()

    return "The display_valid_combos function does not return a value"




def select_substitution_letter(hand):
    """ 
    Returns tuple of run_substitution boolean and selected letter for substitution (letter).
    
    hand: dictionary (string-> int)
    returns: tuple (boolean, string) 
    """
    run_substitution = True
    letter = input("Which letter from your hand would you like to substitute? ")
    letter = call_special_character(hand, letter, "Which letter from your hand would you like to substitute?")[0]
    while letter not in hand or hand[letter] == 0:
        if letter == "!":
            run_substitution = False
            #need to updat the user input to a word guess, or exit statement to "What word would you like to play? "
            break
        letter = input(f"You do not have any '{letter}'s in your hand.  Which letter from your hand would you like to substitute? Enter '!' to abort substitution: ")
        letter = call_special_character(hand, letter, "Which letter from your hand would you like to substitute? ")[0]

    
    #assert len(letter) == 1, "chosen substitution letter returned by the select_substitution_letter function has more than one character"
    return (run_substitution, letter)


def define_help_topics():
    help_topics_dict = {"scoring": "Scoring is calculated as follows:\n  - The Total Word Score equals the Letter Point Score multiplied by the Word Length Factor.\n  - The Letter Point Score is the sum of the values of the letters in the word, the letters having been assigned point values similar to those in scrabble.\n  - The Word Length Factor is equal to 7*(number of letters in word) - 3*(number of letters remaining in hand).\n  - If you are able to use all the letters in your hand you will earn a bonus of 50 points plus 5 times the sum of letter points in your original hand.",
                        "wildcard": "The asterisk '*' in your hand signifies a wildcard.  It can be used to signify any letter. You may use it in one of two ways:\n1 - Enter the full, correctly spelled word and the game will utilize your wildcard for you if needed.\n2 - Input the word using the '*' in place of your missing letter and the game will search for valid words for you.",
                        "substitution": "In each game you have one substitution card, which you may use at the beginning of a hand to switch out your letters.  You will select one letter in your hand and all copies of that letter will be replaces with the same number of copies of a new letter, chosen at random.",
                        "replay": "At the end of each hand you will be prompted with the option to replay the hand.  Enter '&' to replay the hand and keep the higher of the 2 scores.  If you have substituted letters during the hand you will replay the substituted hand, not the original. Once you are in replay mode you will not have the option to substitute letters."}


    help_topics = []
    for key in help_topics_dict:
        help_topics.append(key)
    
    return (help_topics_dict, help_topics)

    
    
def display_help(hand):
    
    print()
    print()
    print("      ************")
    print("Welcome to PurdyWordy Help")
    print()
    print("      ************")
    print()
    print("Here is a dictionary of keystrokes with special significance in PurdyWordy:")
    print()
    print("'?'   --  Input '?' at any time to enter this help menu")
    print()
    print("'...' --  When asked to input your word you can input '...' to display your hand")
    print()
    print("'*'   --  Signifies a wildcard vowel, it can be used to represent any one vowel 'a', 'e', 'i', 'o', or 'u'")
    print()
    print("'#'   --  Input '#' to access hints, a list of all words possible with current hand will be displayed.")
    print()
    print("'%'   --  When given the option to substitute letters in your hand,  input '%' to execute this option.") 
    print()
    print("'!'   --  Exits the 'substitute letter' option without exchanging letters")
    print()
    print("'!!'  --  Input '!!' end the hand with letters leftover and move on to next hand")
    print()
    print("'&'    -- When prompted, enter '&' to replay the previous hand")
    
    help_topics_dict = define_help_topics()[0]
    help_topics = define_help_topics()[1]
    help_topic_selected = input(f"Press enter to exit help menu, or if you would like further help please input one of the following topics {help_topics}:")
    print()
    while help_topic_selected in help_topics:
        print ()
        print (f"{help_topic_selected}:  {help_topics_dict[help_topic_selected]}")
        print()
        help_topic_selected = input(f"Press enter to exit help menu, or if you would like further help please input one of the following topics {help_topics}:")
        print() 
    print ("Welcome back to the game. Incase you need a refresher, your hand contains:")
    print()
    display_hand(hand)



        
def call_special_character(hand, input_variable, exit_prompt):
    
    run_substitution = False
    run_replay = False
    letter = "placeholder_letter"
    
    while input_variable in SPECIAL_CHARACTERS:
        if input_variable == "?":
            display_help(hand)
            input_variable = input(exit_prompt)
        elif input_variable == "...":
            display_hand(hand)
            input_variable = input(exit_prompt)
        elif input_variable == "*":
            help_topics_dict = define_help_topics()[0]
            print()
            print ("wildcard:  " + help_topics_dict["wildcard"])
            input_variable = input(exit_prompt)
        elif input_variable == "#":
            display_all_valid_words_in_hand(hand, word_list)
            input_variable = input(exit_prompt)
        elif input_variable == "%":
            if calculate_handlen(hand) == HAND_SIZE:
                select_substitution_letter_result = select_substitution_letter(hand)
                run_substitution = select_substitution_letter_result[0]
                letter = select_substitution_letter_result[1]
                if run_substitution:
                    input_variable = input(f"Please note that if you are in the process of replaying a hand the letter will not be substituted. Press enter to switch out your '{letter}'s for new letters or input '!' to cancel the substitution:")
                    if input_variable == "!":
                        run_substitution = False
                if not run_substitution:
                    print("Your hand still contains:")
                    print()
                    display_hand(hand)
                    input_variable = input("What word would you like to play? ")
            else:
                print("Sorry, the letter substitution option is only available at the beginning of a hand.")
                input_variable = input(exit_prompt)
        elif input_variable == "!":
            input_variable = input("There is nothing to cancel at the moment. If you meant give up and deal a new hand enter '!!': ")
        elif input_variable == "!!":
            break
        elif input_variable == "&":
            input_variable = input(exit_prompt)
            run_replay = True
        elif input_variable != "!!":
            input_variable = input(exit_prompt)
            print()
        elif input_variable == "":
            pass
        
        
    return (input_variable, run_substitution, run_replay, letter)
    

def play_hand(hand, word_list, unvalidated_word, letter_points_in_hand):

    """
    Allows the user to play the given hand, as follows:
        
    * at the point this function is entered the new hand has already been dealt

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    
    hand_score = 0
    hand_length = calculate_handlen(hand)
    bonus_points = 50 + 5*letter_points_in_hand
    
    if unvalidated_word == "placeholder_word":
        print()
        print("Your hand contains the following letters:")
        display_hand(hand)
    
    while len(find_all_valid_words_in_hand(hand, word_list)) > 0 and unvalidated_word != "!!": 
        if unvalidated_word == "placeholder_word":
            unvalidated_word = input("What word would you like to play?")
            call_special_character_result = call_special_character(hand, unvalidated_word, "What word would you like to play?")
            unvalidated_word = call_special_character_result[0]
            print()
        
        #print(unvalidated_word)
        if unvalidated_word == "!!":
            word = unvalidated_word
            break
        else:
            word = clean_up_word(unvalidated_word, hand)
            if word == "!!":
                break
            elif is_valid_word(word, hand, word_list):
                word_score = get_word_score(word, hand)
                hand_score += word_score
                print (f"Your word '{word}' is worth {word_score} points. So far you have earned {hand_score} points for this hand.")
                hand = update_hand(hand, word)
                hand_length = calculate_handlen(hand)
                if hand_length > 0:
                    print ("Your hand contains the following letters:")
                    print()
                if hand_length == 0:
                    print (f"Congratulations, you used all your letters!  You've earned a {bonus_points} point bonus.")
                    hand_score += bonus_points
                elif hand_length == 1:
                    display_hand(hand)
                    print()
                    print ("You do not have enough letters in your hand to form a valid word.")
                else:
                    display_hand(hand)
            elif word != "!!":
                print("Please try again. Enter '!!' to end this hand., or '...' to display the letters in your hand.")
        if word == "!!":
            hand_score = 0
            break
        unvalidated_word = "placeholder_word"
    if len(find_all_valid_words_in_hand(hand, word_list)) == 0 and calculate_handlen(hand) > 0:
        print("There are no valid words that can be formed with the letters you hand.")
    print (f"Hand complete. Your score for this hand is:\n   --- {hand_score} points ---")
    print()
    return hand_score

        
    

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    
    count = hand[letter]
    new_hand = hand.copy()
    new_hand.pop(letter)
    available_letters = VOWELS + CONSONANTS
    unavailable_letters = hand.keys()
    #print (available_letters)
    #print (unavailable_letters)
    for char in unavailable_letters:
        available_letters = available_letters.replace(char, "")
    #print (available_letters)
    new_letter = random.choice(available_letters) 
    #print (new_letter)
    for i in range(count):
        new_hand[new_letter] = new_hand.get(new_letter, 0) + 1
    assert new_hand[new_letter] == count, "something went wrong with the letter substitution, the letter drawn may already have existed in the hand"
    return new_hand
    
       
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    print()
    print()
    print("      :~~~~~~~~:")
    print("      PURDYWORDY")
    print("      :~~~~~~~~:")
    print("        by Zia")
    print()
    print ("Welcome to PurdyWordy!")
    print ()
    print ("I don't want to overload you with instructions, so lets jump right in, but if at any point you are confused about what to do just input '?' to pull up the help menu.")
    rounds = input("How many hands would you like to play? ")
    rounds = call_special_character(EMPTY_HAND, rounds, "Welcome back to the game. How many hands would you like to play? ")[0]
    print()
    
    
    while type(rounds) != int:
        try: 
            rounds = int(float(rounds))
        except:
            rounds = input("Come on...I think you know what a number is...How many hands would you like to play? ")
            rounds = call_special_character(EMPTY_HAND, rounds, "Welcome back to the game. How many hands would you like to play? ")[0]
    
    if rounds > 12:
        rounds = 12
        print("That seems a bit excessive, doesn't it? Let's call it an even dozen.")
        print()
    
    print("OK, let's play!")
    
    rounds_remaining = rounds
    #replays_available = 1
    substitutions_available = 1
    game_score = 0
    replay_mode = False
    previous_hand_score = 0
    
    while rounds_remaining > 0 or replay_mode:
        if replay_mode:
                print("Your hand contains the following letters:")
                print()
        elif rounds_remaining == rounds:
                print("Your first hand contains the following letters:")
                print()
        else:
                print(f"With {rounds_remaining} hands left to play in this game you currently have {game_score} points.  Your new hand contains:")
                print()
                
        if not replay_mode:
            hand = deal_hand(HAND_SIZE)
            letter_points_in_hand = calculate_letter_points(hand)
        display_hand(hand)
        
        unvalidated_word = "placeholder_word"
        
        run_substitution = False
        if substitutions_available > 0 and not replay_mode:
            substitute_hand_yes_no = input(f"You have {substitutions_available} substitution availible.\nInput '%' to substitute letters, '?' for help, or just go ahead and enter the word you want to play: ")
            call_special_character_result = call_special_character(hand, substitute_hand_yes_no, "Enter '%' to substitute letters, otherwise enter the word you want to play: ")
            print()
            while len(call_special_character_result[0]) == 1:
                substitute_hand_yes_no = input("Sorry, I'm not ready for your letter choice yet.  If you want to substitute letters in this hand input '%', otherwise just go ahead and enter the word you want to play: ")
                call_special_character_result = call_special_character(hand, substitute_hand_yes_no, "Enter '%' to substitute letters, otherwise go ahead and enter the word you want to play: ")
            unvalidated_word = call_special_character_result[0]
            run_substitution = call_special_character_result[1]
            letter = call_special_character_result[3]
            if run_substitution == True:
                hand = substitute_hand(hand, letter)
                letter_points_in_hand = calculate_letter_points(hand)
                substitutions_available -= 1
                print("Your updated hand contains the following letters:")
                print()
                display_hand(hand)
                unvalidated_word = input("What word would you like to play? ")
                unvalidated_word = call_special_character(hand, unvalidated_word, "What word would you like to play? ")[0]
                #your hand still contains?
        else:
            unvalidated_word = input("What word would you like to play? ")
            unvalidated_word = call_special_character(hand, unvalidated_word, "What word would you like to play? ")[0]
    
        if unvalidated_word == "!!":
            hand_score = 0
            print()
            print (f"Hand aborted with {hand_score} points.")
        else:
            hand_score = play_hand(hand, word_list, unvalidated_word, letter_points_in_hand)
        
        if run_substitution:
            letters_to_replay = "substituted"
        else:
            letters_to_replay = "original"
        
        if replay_mode == True:
            if hand_score > previous_hand_score:
                print (f"Good job, {hand_score} is better than your previous best score of {previous_hand_score} for this hand.")
                previous_hand_score = hand_score
            else:
                print (f"Too bad, you didn't improve on your previous best score of {previous_hand_score} for this hand.")
            replay_mode = False
        #print("replay mode: " + str(replay_mode))
        else:
            previous_hand_score = hand_score
        if rounds_remaining > 1:
            replay_yes_no = input (f"Input '&' to replay the hand with your {letters_to_replay} letters.  Otherwise press enter to deal the next hand.")
        else:
            replay_yes_no = input (f"Input '&' to replay the hand with your {letters_to_replay} letters.  Otherwise press enter to calculate game score.")
        print()
        replay_mode = call_special_character_result = call_special_character(hand, replay_yes_no, f"Alright! Let's see if you can improve on {previous_hand_score}. Press enter to continue.")[2]
        print()
        
        if not replay_mode:
            game_score += hand_score
            rounds_remaining -= 1
            hand_score = 0
        
    print (f"Game over! Good work, your total score for {rounds} rounds is:\n   --- {game_score} points ---")
    
    
    
    
    


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
    
    
    #comment out the play_game function above and Uncomment portions of below to test functions
    #hand = {'a': 1, 't': 1, 'p': 1, '*': 1}
    #hand = {'a': 1, 'y': 1, 't': 1, 'p': 2, 'n': 1, '*': 1}
    #unvalidated_word = "placeholder_word"
    #word = "patty"

    #input_variable ="!!"
    #print("input_variable, ", "run_substitution, ", "run_replay, ", "letter")
    #call_help_result = (call_help(hand, input_variable, "Now the function prints the call help exit_prompt. please enter something to continue the test:"))
    #print(call_help_result)
    
    #clean up word seems to work properly
    #is valid word function seems to be working properly
    #while unvalidated_word != "stop":
        #unvalidated_word = input("enter word to cleanup and check validity:")
        #word = clean_up_word(unvalidated_word, hand)
        #print("function exited - word:" + word)
        #is_valid = is_valid_word(word, hand, word_list)
        #print("is valid:" + str(is_valid))
        #print(word)
    
    #hand play function seems to be working, including call special character and !! during hand play
    #hand = deal_hand(9)
    #unvalidated_word = "placeholder_word"
    #play_hand(hand, word_list, unvalidated_word)
    
    #game play:
        #special characters seem to work during substitution
        #replay function seems to work
    #play_game(word_list)
    
    #Test hints function!
    #can_form_word is working
    #print(find_all_valid_words_in_hand(hand, word_list))
    #print(can_form_word(hand, word))
    #display_all_valid_words_in_hand(hand, word_list)
    