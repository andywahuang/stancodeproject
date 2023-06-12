"""
File: hangman.py
Name: Andy Huang
-----------------------------
This program plays hangman game.
User sees a dashed word, trying to
correctly figure the un-dashed word out
by inputting one character each round.
If the user input is correct, show the
updated word on console. Players have N_TURNS
chances to try and win this game.
"""


import random


# This constant controls the number of guess the player has.
N_TURNS = 7


def main():
    """
    The program will first show a string of '-' according to the length of the answer,
    and ask the user to guess 1 english character.
    Then it will check if the guessed character is in the answer,
    if so, it will be showed in the following line, and the left time will remain the same
    until the user guess the complete answer.
    If the guess is wrong, the left time will minus 1, until the user ran out of the 7 chance.
    """
    ans = random_word()
    left = 7
    print('The word looks like ' + ans_len(ans))
    print('You have ' + str(left) + ' wrong guesses left.')
    draw(left)
    now = ans_len(ans)
    guess = (input('Your guess: ').upper())
    while not check_format(guess):
        print('Illegal format')
        guess = (input('Your guess: ').upper())
    while left > 1:
        # This loop is used to check whether the user guess the complete answer before 1 chance left.
        if '-' in now:
            if guess in ans:
                now = check(guess, now, ans)
                print('You are correct!')
                print('The word looks like ' + now)
            else:
                print('There is no ' + guess + "'s in the word.")
                print('The word looks like ' + now)
                left -= 1
            print('You have ' + str(left) + ' guess left.')
            draw(left)
            guess = input('Your guess: ').upper()
            while not check_format(guess):
                print('Illegal format')
                guess = (input('Your guess: ').upper())
            now = check(guess, now, ans)
        # no '-' in now means all the characters are guessed, and the user win.
        else:
            print('You win!!')
            print('The word was: ' + ans)
            left = 0
            # Assign left = 0 to end the loop.
    while left == 1:
        now = check(guess, now, ans)
        if guess in ans:
            if '-' not in now:
                print('You win!!')
                print('The word was: ' + ans)
                left -= 1
                # only 1 chance left here, so minus 1, making it 0, could end the loop.
            else:
                print('You are correct!')
                print('The word looks like ' + now)
                print('You have ' + str(left) + ' guess left.')
                draw(left)
                guess = input('Your guess: ').upper()
                while not check_format(guess):
                    print('Illegal format')
                    guess = (input('Your guess: ').upper())
        else:
            left -= 1
            # After the user guess wrong in the last chance, the left will become 0 and the loop will be ended.
            print('You are completely hung : ( ')
            print('The word was: ' + ans)
            draw(left)


def draw(left):
    """
    This function will draw the situation of hangman based on how many chance left currently.
    """
    print('|-----|')  # row 1 of hangman
    print('|     |')  # row 2 of hangman
    # below are row 3 of hangman
    if left == 7:
        print('|      ')
    elif left == 0:
        print('|     ☹︎')
    else:
        print('|     O')
    # below are row 4 of hangman
    if left >= 6:
        print('|      ')
    elif left == 5:
        print('|     |')
    elif left == 4:
        print('|    /|')
    else:
        print('|    /|\\')
    # below are row 5 of hangman
    if left >= 3:
        print('|     ')
    elif left == 2:
        print('|    /')
    else:
        print('|    / \\')
    print('|     ')  # row 6 of hangman
    print('|------')  # row 7 of hangman


# |-----|
# |     |
# |     ☹︎
# |    /|\
# |    / \
# |
# |------


def check_format(guess):
    """
    This function help us check whether the user input in correct format.
    If the format is correct, it will return True, or it will return False.
    """
    if str.isalpha(guess):
        return len(guess) == 1
    return str.isalpha(guess)


def check(guess, now, ans):
    """
    This function provide the latest version of the answer situation. The return value will show the characters already
    guessed by the user, and the remains will be hide by '-' as the beginning of the program.
    """
    new = ""
    for i in range(len(ans)):
        ch = ans[i]
        if guess == ch:
            new += guess
        else:
            new += now[i]
    return new


def ans_len(ans):
    """
    This function help us get a string of '-' in the beginning of the function based on the length of the answer.
    """
    q = ""
    for i in range(len(ans)):
        q += "-"
    return q


def random_word():
    num = random.choice(range(9))
    if num == 0:
        return "NOTORIOUS"
    elif num == 1:
        return "GLAMOROUS"
    elif num == 2:
        return "CAUTIOUS"
    elif num == 3:
        return "DEMOCRACY"
    elif num == 4:
        return "BOYCOTT"
    elif num == 5:
        return "ENTHUSIASTIC"
    elif num == 6:
        return "HOSPITALITY"
    elif num == 7:
        return "BUNDLE"
    elif num == 8:
        return "REFUND"


# DO NOT EDIT CODE BELOW THIS LINE #

if __name__ == '__main__':
    main()
