from rand_word import RandomWordGenerator


class Game:
    def __init__(self, letters) -> None:
        self.cor_lett = ""
        self.incor_let = ""
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
                hidden_word = hidden_word[:i] + word[i] + hidden_word[i + 1 :]
        return hidden_word

    def play(self):
        word = self.word.rand_word()
        # return word
        hidden_word = self.hidden_word_handling(word)
        while True:
            guessed_letters = self.cor_lett + self.incor_let
            valid_guess = False
            while not valid_guess:
                guess = self.letter_input(guessed_letters)
                if len(guess)
                
            #print statement for board printing
            pass
    @staticmethod
    def input_error(error_message):
        return error_message  
    
    @staticmethod  
    def letter_input(guessed_letters):
        guess = input('Enter a letter :').lower() #this might be a problem, if not console program.
        
        if len(guess) != 1:
            return f'Only one symbol allowed, enter again'
            #error hadling + logging here
        elif guess in guessed_letters:
            return f'Letter already used, enter again '
            #error hadling + logging here
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            return f'Not a letter, enter again: '
            #error hadling + logging here
        elif guess == 'again':
            return f'Very smart, now enter a single letter '
        elif guess == 'single letter':
            return f'Now that is just briliant, play a game, will Ya? '           
        else:
            return guess
            #logging here