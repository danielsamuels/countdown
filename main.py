import itertools
import math
import pickle
import random
import re
import sys


class Countdown:
    vowels = 'aeiou'
    consonants = 'bcdfghjklmnpqrstvwxyz'
    words = []
    len_words = {}

    vowel_pile_size = 67
    consonant_pile_size = 74
    vowel_pile = ''
    consonant_pile = ''
    board = ''

    def __init__(self, board=None):
        try:
            self.words = pickle.load(file('pickles/words.pickle'))
            self.len_words = pickle.load(file('pickles/len_words.pickle'))
            loaded_from = 'pickle.'
        except IOError:
            # Get a list of words.
            with open('/usr/share/dict/words', 'rb') as f:
                for line in f:
                    # Ignore any which have more than 9 letters.
                    line = line.strip().lower()
                    if len(line) > 9:
                        continue

                    # Ignore any which have more than 5 vowels.
                    if self.count_vowels(line) > 5:
                        continue

                    # Ignore any which have more than 6 consonants.
                    if self.count_consonants(line) > 5:
                        continue

                    self.words.append(line)

                    try:
                        self.len_words[len(line)].append(line)
                    except KeyError:
                        self.len_words[len(line)] = [line]

            pickle.dump(self.words, file('pickles/words.pickle', 'w'))
            pickle.dump(self.len_words, file('pickles/len_words.pickle', 'w'))
            loaded_from = 'words list.'

        print 'Loaded {:,} words from {}'.format(
            len(self.words),
            loaded_from
        )

        self.build_vowel_pile()
        self.build_consonant_pile()

        print 'Generated piles.'

        if not board:
            self.generate_tiles()
        else:
            self.board = board

        self.solve()


    def count_vowels(self, word):
        return len([letter for letter in word if letter in self.vowels])

    def count_consonants(self, word):
        return len([letter for letter in word if letter in self.consonants])

    def build_vowel_pile(self):
        try:
            self.vowel_pile = pickle.load(file('pickles/vowel_pile.pickle'))
        except IOError:
            # The amount of times a single letter appears within the pile varies
            # from letter to letter according to it's frequency within natural
            # English.  As a naive implementation, we'll just base the weightings
            # off the number of occurrences within our dataset.
            #
            # For each vowel, work out how many times it appears within the word set.
            vowel_occurrences = {letter: 0.00 for letter in self.vowels}

            for word in self.words:
                for letter in self.vowels:
                    vowel_occurrences[letter] += word.count(letter)

            total = sum(vowel_occurrences.values())

            # For each of the letters, work out it's percentage value of frequency
            # within the word set and then work out how many letters of each type
            # are needed as a percentage of the pile size, then build the actual pile.
            self.vowel_pile = ''.join(
                letter * int(
                    math.ceil(
                        (self.vowel_pile_size * vowel_occurrences[letter]) / total
                    )
                )
                for letter in self.vowels
            )

            pickle.dump(self.vowel_pile, file('pickles/vowel_pile.pickle', 'w'))

    def build_consonant_pile(self):
        try:
            self.consonant_pile = pickle.load(file('pickles/consonant_pile.pickle'))
        except IOError:
            # The amount of times a single letter appears within the pile varies
            # from letter to letter according to it's frequency within natural
            # English.  As a naive implementation, we'll just base the weightings
            # off the number of occurrences within our dataset.
            #
            # For each consonant, work out how many times it appears within the word set.
            consonant_occurrences = {letter: 0.00 for letter in self.consonants}

            for word in self.words:
                for letter in self.consonants:
                    consonant_occurrences[letter] += word.count(letter)

            total = sum(consonant_occurrences.values())

            # For each of the letters, work out it's percentage value of frequency
            # within the word set and then work out how many letters of each type
            # are needed as a percentage of the pile size, then build the actual pile.
            self.consonant_pile = ''.join(
                letter * int(
                    math.ceil(
                        (self.consonant_pile_size * consonant_occurrences[letter]) / total
                    )
                )
                for letter in self.consonants
            )

            pickle.dump(self.consonant_pile, file('pickles/consonant_pile.pickle', 'w'))

    def generate_tiles(self, consonants=None, vowels=None):
        # Minimum requirements for character selections are 3 vowels and
        # 4 consonants and a total of 9 letters. This therefore means that
        # the combinations possible are:
        #
        # 3 vowels, 6 consonants.
        # 4 vowels, 5 consonants.
        # 5 vowels, 4 consonants.

        if not consonants:
            if vowels:
                consonants = 9 - vowels
            else:
                vowels = random.randint(3, 5)
                consonants = 9 - vowels

        if not vowels:
            if consonants:
                vowels = 9 - consonants
            else:
                consonants = random.randint(4, 6)
                vowels = 9 - consonants

        print 'Picking {} consonants and {} vowels.'.format(
            consonants,
            vowels,
        )

        board = ''

        # Copy the piles as we'll need to modify them.
        consonant_pile, vowel_pile = self.consonant_pile, self.vowel_pile

        # Get consonants from the pile, removing them from the pile as they
        # are chosen (once a letter is removed from a pile, it can't be picked
        # again).

        for x in range(1, consonants + 1):
            index = random.randint(0, len(consonant_pile)-1)
            board = board + consonant_pile[index]
            consonant_pile = consonant_pile[:index] + consonant_pile[index+1:]

        # Get vowels from the pile.
        for x in range(1, vowels + 1):
            index = random.randint(0, len(vowel_pile)-1)
            board = board + vowel_pile[index]
            vowel_pile = vowel_pile[:index] + vowel_pile[index+1:]

        print 'Your board: {}'.format(board.upper())
        self.board = board


    def solve(self):
        # Manipulate the board into every possible order and check if it's a
        # valid word according to the word list.
        print 'Attempting to solve {}.'.format(self.board)

        total_words = 0
        found = set()

        # 4+ consonant regex
        pattern = re.compile(r'([{consonants}]{{3,}})'.format(
            consonants=self.consonants
        ))

        for x in range(9, 6, -1):
            print 'Trying {} letter words.'.format(x)

            iteration = 0
            level_words = 0

            for word in itertools.permutations(self.board, x):
                permutation = ''.join(word)

                # You don't really get words with 3+ consonants together, so
                # just ignore those.
                consonant_test = re.search(pattern, permutation)

                if consonant_test is None and permutation not in found:
                    if permutation in self.len_words[x]:
                        print permutation

                        found.add(permutation)
                        level_words += 1
                        total_words += 1

            print '{} {} character words found.'.format(
                level_words,
                x,
            )
        print '{} words found: {}'.format(total_words, found)


if __name__ == '__main__':
    try:
        Countdown(sys.argv[1])
    except IndexError:
        Countdown()
