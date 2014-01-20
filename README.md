countdown
=========

The countdown solver has 3 modes of operation:

1. Fully automatic.  In this mode the program will load a list of words then calculate the number of times each letter appears and then generate a weighting for each letter. This weighting is then used to determine the amount of time each letter appears in the pile.  It then builds the piles based on the weights and decides how many consonants and how many vowels should be selected for the board. It then selects the board randomly, based on the consonant and vowel limit, it then tries to solve the board, working out the longest possible word.
2. Manual board. In this mode the program will work out the longest possible word from the given letters.
3. OCR. In this mode the program will capture from a window (I use [Droid @ Screen](http://droid-at-screen.ribomation.com/)) and OCR the letters displayed, it will then pass them into the solver and return the best words available.
