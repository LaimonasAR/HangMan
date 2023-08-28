from rand_word import RandomWordGenerator
from app import hangman 

class Game:
    def __init__(self, letters) -> None:
        self.cor_lett = ""
        self.incor_lett = ""
        self.word = RandomWordGenerator(letters)
        self.game_over = False


class Play(Game):
    def __init__(self, letters) -> None:
        super().__init__(letters)
        # self.incorrect_letters = ""
        # self.correct_letters = ""

    def hidden_word_handling(self, word):
        hidden_word = "_" * len(word)
        for i in range(len(word)):  # Replace blanks with correctly guessed letters.
            if word[i] in self.cor_lett:
                hidden_word = hidden_word[:i] + word[i] + hidden_word[i + 1:]
        return hidden_word

    def play(self):
        word = self.word.rand_word()
        print(word)
        # return word
        hidden_word = self.hidden_word_handling(word)
        print(hidden_word)
        while True:
            guessed_letters = self.cor_lett + self.incor_lett
            # valid_guess = False
            guess = self.letter_input(guessed_letters)
            #guess = hangman.user_input
            if len(guess) > 1:
                print(guess)
                continue
            if guess in word:
                self.cor_lett = self.cor_lett + guess
                print(guess)
                print("ok, good guess")
                hidden_word = self.hidden_word_handling(word)
                print(hidden_word)
                print("Correct letters")
                print(self.cor_lett)
                print("incorrect letters")
                print(self.incor_lett)
                victory = self.victory_check(word)
                if victory:
                    print("Woo Hoo!")
                    self.game_over = True
                    break
                else:
                    print("Go on :) ")
            else:
                self.incor_lett = self.incor_lett + guess
                print(guess)
                print("Not OK, bad guess")
                hidden_word = self.hidden_word_handling(word)
                print(hidden_word)
                print("Correct letters")
                print(self.cor_lett)
                print("incorrect letters")
                print(self.incor_lett)
                if len(self.incor_lett) == 10:
                    print("bad luck!")
                    self.game_over = True
                    break
            # while len(guess) > 1:
            #     print("wtf, dude?")
            #     guess = self.letter_input(guessed_letters)
            #     # if len(guess) > 1:
            #     print("wtf, dude?")
            #     print(guess)

    @classmethod
    def victory_check(self, word):
        victory_check = True
        for i in range(len(word)):
            if word[i] not in self.cor_lett:
                victory_check = False
                break
        return victory_check

    @classmethod
    def victory_check(self, word):
        victory_check = True
        for i in range(len(word)):
            if word[i] not in self.cor_lett:
                victory_check = False
                break
        return victory_check
    
    #PLAY AGAIN should not be here
    # @staticmethod
    # def play_again():
        
    #     play_again = input("Play again? Y/N ").lower()
        
    #     if play_again == 
        
    #     return error_message

    @staticmethod
    def letter_input(guessed_letters):
        guessing = hangman()
        guess = guessing
        # guess = input(
        #     "Enter a letter :"
        # ).lower()  # this might be a problem, if not console program.

        if len(guess) != 1 and guess == "again":
            return f"Very smart, now enter a single letter "
            # error hadling + logging here
        elif len(guess) != 1 and guess == "a letter":
            return f"Ever thought about trying Comedy? "
            # error hadling + logging here
        elif len(guess) != 1 and guess == "single letter":
            return f"Now that is just briliant, play a game, will Ya? "
            # error hadling + logging here
        elif len(guess) != 1:
            return f"Only one symbol allowed, enter again"
            # error hadling + logging here
        elif guess in guessed_letters:
            return f"Letter already used, enter again "
            # error hadling + logging here
        elif guess not in "abcdefghijklmnopqrstuvwxyz":
            return f"Not a letter, enter again: "
            # error hadling + logging here
        elif guess == "again":
            return f"Very smart, now enter a single letter "
        elif guess == "single letter":
            return f"Now that is just briliant, play a game, will Ya? "
        else:
            return guess
        #     # logging here
