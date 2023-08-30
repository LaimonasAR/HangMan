from random_word import Wordnik, RandomWords

# -------- result_wr uses API for wordnik ----


class RandomWordGenerator:
    def __init__(self, letters: int) -> None:
        self.letters = letters

    def rand_word(self) ->str:
        r = RandomWords()
        wr = Wordnik(api_key="k4xgjm1yy5l1go1arfxn476vc77vsx8bq5uhwk6qx78olhwft")
        result = r.get_random_word()
        result_wr = wr.get_random_word(
            hasDictionaryDef="true",
            includePartOfSpeech="noun",
            minLength=self.letters,
            maxLength=(self.letters),
        )
        return result_wr.lower()
