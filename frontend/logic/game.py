import logging
import logging.config

logging.config.fileConfig(fname="logging.conf", disable_existing_loggers=False)
logger = logging.getLogger("sLogger")

cor_lett: str = ""
incor_lett: str = ""
message = "Let's start!"


def hidden_word_handling(word:str, cor_letters:str) -> str:
    hidden_word = "_" * len(word)
    for i in range(len(word)):
        if word[i] in cor_letters:
            hidden_word = hidden_word[:i] + word[i] + hidden_word[i + 1 :]
    return hidden_word

class Game:
    def __init__(self, word:str, cor_lett:str, incor_lett:str, guess:str) -> None:
        self.word = word
        self.cor_lett = cor_lett
        self.incor_lett = incor_lett
        self.guess = guess
        self.game_over = False

    @staticmethod
    def victory_check(word:str, cor_lett:str) -> bool:
        victory_check = True
        for i in range(len(word)):
            if word[i] not in cor_lett:
                victory_check = False
                break
        return victory_check

    @staticmethod
    def checkguess(guess:str, guessed_letters:str) ->str:
        guessed = guess.lower()
        if len(guessed) != 1:
            logger.warning("Too many symbols")
            return f"Only one symbol allowed, enter again"
        elif guessed in guessed_letters:
            logger.warning("Letter already guessed")
            return f"Letter already used, enter again "
        elif guessed not in "abcdefghijklmnopqrstuvwxyz-":
            logger.warning("Not a letter entered")
            return f"Not a letter, enter again: "
        else:
            return guessed

    def play(self) -> dict:
        guessed_letters = self.cor_lett + self.incor_lett
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
                message = "Woo Hoo!"
                self.game_over = True
                logger.info("Game won")
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
                logger.info("Game lost")
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

