from rand_word import RandomWordGenerator


class Game:
    def __init__(self, letters) -> None:
        self.cor_lett = ''
        self.incor_let = ''
        self.word = RandomWordGenerator(letters)
        self.game_over = False
        
class Play(Game):
    def __init__(self, letters) -> None:
        super().__init__(letters)
        
    def play(self):
        return self.word.rand_word()
    