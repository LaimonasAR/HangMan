from logic.rand_word import RandomWordGenerator

cor_lett: str = ""
incor_lett: str = ""
# letters:int = 10
# word_func = RandomWordGenerator(letters)
# word = word_func.rand_word()
message = "Let's start!"


def hidden_word_handling(word, cor_letters):
    hidden_word = "_" * len(word)
    for i in range(len(word)):  # Replace blanks with correctly guessed letters.
        if word[i] in cor_letters:
            hidden_word = hidden_word[:i] + word[i] + hidden_word[i + 1 :]
    return hidden_word


def guess_handling():
    pass


class Game:
    def __init__(self, word, cor_lett, incor_lett, guess) -> None:
        self.word = word
        self.cor_lett = cor_lett
        self.incor_lett = incor_lett
        self.guess = guess
        self.game_over = False

    @staticmethod
    def victory_check(word, cor_lett):
        victory_check = True
        for i in range(len(word)):
            if word[i] not in cor_lett:
                victory_check = False
                break
        return victory_check

    @staticmethod
    def checkguess(guess, guessed_letters):
        guessed = guess.lower()
        if len(guessed) != 1:
            return f"Only one symbol allowed, enter again"
            # error hadling + logging here
        elif guessed in guessed_letters:
            return f"Letter already used, enter again "
            # error hadling + logging here
        elif guessed not in "abcdefghijklmnopqrstuvwxyz-":
            return f"Not a letter, enter again: "
            # error hadling + logging here
        else:
            return guessed

    def play(self):
        guessed_letters = self.cor_lett + self.incor_lett
        # guess = self.guess.lower()
        guessed = self.checkguess(self.guess, guessed_letters)
        hidden_word = hidden_word_handling(self.word, self.cor_lett)
        victory = False
        if len(guessed) > 1:
            message = guessed
            response = {
                "hidden_word": hidden_word,
                "cor_lett": self.cor_lett,
                "incor_lett": self.incor_lett,
                "message": message,
                "victory": victory,
                "game_over": self.game_over,
                "guess_status": 2,
            }
            return response
        elif guessed in self.word:
            cor_lett = self.cor_lett + self.guess
            message = "ok, good guess"
            hidden_word = hidden_word_handling(self.word, cor_lett)
            victory = self.victory_check(self.word, cor_lett)
            if victory:
                print("Woo Hoo!")
                self.game_over = True

            response = {
                "hidden_word": hidden_word,
                "cor_lett": cor_lett,
                "incor_lett": self.incor_lett,
                "message": message,
                "victory": victory,
                "game_over": self.game_over,
                "guess_status": 0,
            }
            return response
        else:
            incor_lett = self.incor_lett + guessed
            message = "Not OK, bad guess"
            hidden_word = hidden_word_handling(self.word, self.cor_lett)
            victory = False
            if len(incor_lett) == 6:
                message = ("bad luck!")
                self.game_over = True
            response = {
                "hidden_word": hidden_word,
                "cor_lett": self.cor_lett,
                "incor_lett": incor_lett,
                "message": message,
                "victory": victory,
                "game_over": self.game_over,
                "guess_status": 0,
            }
            return response

