class User:
    last_id = 1

    def __init__(self, name: str):
        self.id = User.last_id
        self.name = name

        User.last_id += 1