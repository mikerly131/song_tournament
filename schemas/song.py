class Song:
    last_id = 1

    def __init__(self, title: str, artist: str, clip: str):
        self.id = Song.last_id
        self.title = title
        self.artist = artist
        self.clip = clip

        Song.last_id += 1
