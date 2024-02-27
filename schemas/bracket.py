class Bracket:
    last_id = 1

    def __init__(self, song_list: list, user_id: int, name: str, pool_size: int):
        self.id = Bracket.last_id
        self.user_id = user_id
        self.name = name
        self.song_list = song_list
        self.pool_size = pool_size
        self.seed_list = []

        Bracket.last_id += 1


class RankedBracket:
    last_id = 1

    def __init__(self, song_list: list, user: int, pool_size: int):
        self.id = Bracket.last_id
        self.user_id = user
        self.song_list = song_list
        self.pool_size = pool_size
        self.seed_list = []
        self.first_32 = []
        self.sweet_16 = []
        self.elite_8 = []
        self.final_4 = []
        self.last_2 = []
        self.champion = None

        RankedBracket.last_id += 1
