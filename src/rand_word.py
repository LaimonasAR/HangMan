from random_word import Wordnik, RandomWords
#--------no API for wordnik yet ----

class RandomWordGenerator:
    def __init__(self, letters:int) -> None:
        self.letters = letters
        
    def rand_word(self):
        r = RandomWords()
        wr = Wordnik()
        result = r.get_random_word()
        result_wr = wr.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun", minLength=self.letters, maxLength=(self.letters + 5))
        return result
