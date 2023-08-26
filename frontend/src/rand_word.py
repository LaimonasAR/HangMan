from random_word import Wordnik, RandomWords

# --------no API for wordnik yet ----


class RandomWordGenerator:
    def __init__(self, letters: int) -> None:
        self.letters = letters

    def rand_word(self):
        r = RandomWords()
        wr = Wordnik(api_key="k4xgjm1yy5l1go1arfxn476vc77vsx8bq5uhwk6qx78olhwft")
        result = r.get_random_word()
        result_wr = wr.get_random_word(
            hasDictionaryDef="true",
            includePartOfSpeech="noun",
            minLength=self.letters,
            maxLength=(self.letters),
        )
        return result
